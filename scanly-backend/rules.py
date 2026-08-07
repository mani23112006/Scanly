"""
SCANLY Rule-Based Scam Detection Engine

Production-ready rule engine for phishing detection.

Features:
- Keyword scoring
- Multi-word phrase detection
- Safe payment whitelist
- URL heuristics
- Suspicious domains
- Combination rules
- Capital letter detection
- Punctuation detection
- Number pattern detection

Public API:

    score_rules(text) -> {
        "score": int,
        "matched": list
    }

This file intentionally contains no external dependencies.
"""

import re

# ============================================================
# SCORE LIMITS
# ============================================================

MAX_RULE_SCORE = 100

# ============================================================
# CRITICAL KEYWORDS
# These almost always indicate phishing.
# ============================================================

CRITICAL_KEYWORDS = {
    "share otp": 35,
    "otp": 30,
    "one time password": 30,
    "cvv": 35,
    "pin": 30,
    "atm pin": 35,
    "net banking password": 40,
    "internet banking password": 40,

    "account blocked": 30,
    "account suspended": 30,
    "account locked": 30,
    "verify account": 30,
    "verify your account": 30,
    "verify now": 30,
    "bank blocked": 30,

    "click here": 25,
    "login immediately": 30,
    "security alert": 25,
    "suspicious activity": 25,

    "update kyc": 30,
    "kyc expired": 30,
    "complete kyc": 30,

    "aadhaar verification": 30,
    "pan verification": 30,

    "claim reward": 25,
    "claim prize": 30,
    "lottery winner": 35,

    "income tax refund": 30,
    "tax refund": 25,

    "upi suspended": 30,
    "upi blocked": 30,
}

# ============================================================
# HIGH RISK KEYWORDS
# ============================================================

HIGH_KEYWORDS = {

    "bank": 15,
    "bank account": 20,
    "upi": 20,
    "wallet": 15,

    "credit card": 20,
    "debit card": 20,

    "kyc": 20,
    "aadhaar": 20,
    "pan": 20,

    "verify": 15,
    "verification": 15,

    "blocked": 20,
    "suspended": 20,
    "locked": 20,

    "refund": 20,

    "winner": 20,
    "prize": 20,
    "lottery": 20,

    "courier": 15,
    "delivery": 15,
    "parcel": 15,

    "urgent": 15,
    "immediately": 15,
    "act now": 15,
    "today only": 15,

    "free money": 20,
    "cash prize": 20,

    "transaction failed": 20,
    "reactivate": 15,
}

# ============================================================
# MEDIUM RISK
# ============================================================

MEDIUM_KEYWORDS = {

    "dear customer": 10,
    "confirm": 10,
    "update": 10,
    "offer": 10,
    "reward": 10,
    "free": 10,
    "limited offer": 10,
    "limited time": 10,
    "selected": 10,
    "congratulations": 10,
    "claim now": 10,
    "exclusive": 10,
    "bonus": 10,
}

# ============================================================
# SAFE PAYMENT PATTERNS
# If these appear WITHOUT phishing indicators,
# reduce false positives.
# ============================================================

SAFE_PATTERNS = [

    "payment successful",
    "transaction successful",

    "amount credited",
    "amount debited",

    "salary credited",

    "transaction id",

    "available balance",
    "account balance",

    "upi transaction",

    "imps",
    "neft",
    "rtgs",

    "credited to your account",
    "debited from your account",
]

# ============================================================
# URL SHORTENERS
# ============================================================

SHORT_URLS = [
    "bit.ly",
    "tinyurl",
    "t.co",
    "goo.gl",
    "rb.gy",
    "cutt.ly",
]

# ============================================================
# SUSPICIOUS DOMAINS
# ============================================================

SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".click",
    ".live",
    ".gq",
    ".cf",
    ".tk",
    ".ml",
]

# ============================================================
# COMBINATION RULES
# Extra score if both phrases appear.
# ============================================================

COMBINATION_RULES = {

    ("otp", "bank"): 20,
    ("otp", "blocked"): 25,
    ("otp", "verify"): 20,

    ("bank", "click here"): 20,

    ("kyc", "urgent"): 20,
    ("kyc", "verify"): 20,

    ("upi", "verify"): 20,
    ("upi", "blocked"): 20,

    ("account", "blocked"): 20,
    ("account", "suspended"): 20,

    ("refund", "click here"): 20,
}

# ============================================================
# NORMALIZE
# ============================================================

def _normalize_text(text: str) -> str:
    """
    Lowercase + collapse multiple spaces.
    """

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================================================
# FIND KEYWORDS
# Counts every keyword only once.
# ============================================================

def _find_keywords(text, keyword_dict):

    matched = []
    score = 0

    # longest phrase first
    items = sorted(
        keyword_dict.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    for phrase, points in items:

        if phrase in text:

            matched.append(phrase)
            score += points

            # remove phrase so duplicate isn't counted
            text = text.replace(phrase, " ")

    return score, matched



    # ============================================================
# SAFE PATTERN CHECK
# ============================================================

def _contains_safe_pattern(text: str) -> bool:
    """
    Returns True if the message looks like a legitimate
    payment/banking notification.
    """

    for pattern in SAFE_PATTERNS:
        if pattern in text:
            return True

    return False


# ============================================================
# PHISHING OVERRIDE
# Even if payment message is detected,
# these indicators should override whitelist.
# ============================================================

PHISHING_OVERRIDE = [
    "otp",
    "share otp",
    "verify",
    "verify account",
    "click here",
    "blocked",
    "suspended",
    "login immediately",
    "security alert",
    "update kyc",
    "cvv",
    "pin",
]


def _has_override(text: str) -> bool:

    return any(x in text for x in PHISHING_OVERRIDE)


# ============================================================
# KEYWORD SCORING
# ============================================================

def _score_keywords(text: str):

    total_score = 0
    matched = []

    for dictionary in (
        CRITICAL_KEYWORDS,
        HIGH_KEYWORDS,
        MEDIUM_KEYWORDS,
    ):

        score, words = _find_keywords(text, dictionary)

        total_score += score
        matched.extend(words)

    return total_score, matched


# ============================================================
# COMBINATION SCORING
# Example:
# OTP + BLOCKED
# KYC + VERIFY
# ============================================================

def _score_combinations(text: str):

    score = 0
    matched = []

    for combo, points in COMBINATION_RULES.items():

        if all(word in text for word in combo):

            score += points
            matched.append(" + ".join(combo))

    return score, matched


# ============================================================
# URL DETECTION
# ============================================================

def _score_urls(text: str):

    score = 0
    matched = []

    if "http://" in text or "https://" in text:

        score += 10
        matched.append("url")

    for shortener in SHORT_URLS:

        if shortener in text:

            score += 15
            matched.append(shortener)

    for tld in SUSPICIOUS_TLDS:

        if tld in text:

            score += 15
            matched.append(tld)

    return score, matched


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def _unique(values):

    seen = set()
    output = []

    for item in values:

        if item not in seen:

            seen.add(item)
            output.append(item)

    return output


# ============================================================
# BASE SCORE
# ============================================================

def _base_score(text: str):

    score = 0
    matched = []

    # ---------- Safe Payment ----------

    if _contains_safe_pattern(text) and not _has_override(text):

        return 0, []

    # ---------- Keywords ----------

    keyword_score, keyword_matches = _score_keywords(text)

    score += keyword_score
    matched.extend(keyword_matches)

    # ---------- Combination Rules ----------

    combo_score, combo_matches = _score_combinations(text)

    score += combo_score
    matched.extend(combo_matches)

    # ---------- URLs ----------

    url_score, url_matches = _score_urls(text)

    score += url_score
    matched.extend(url_matches)

    return score, _unique(matched)



# ============================================================
# CAPITAL LETTER DETECTION
# Example:
# VERIFY NOW
# FREE MONEY
# ============================================================

def _score_capitals(original_text: str):

    score = 0
    matched = []

    words = re.findall(r"\b[A-Z]{3,}\b", original_text)

    if len(words) >= 2:
        score += 10
        matched.append("multiple capital words")

    elif len(words) == 1:
        score += 5
        matched.append("capital word")

    return score, matched


# ============================================================
# EXCESSIVE PUNCTUATION
# ============================================================

def _score_punctuation(text: str):

    score = 0
    matched = []

    if "!!!" in text:
        score += 5
        matched.append("!!!")

    if "???" in text:
        score += 5
        matched.append("???")

    if "₹₹" in text:
        score += 5
        matched.append("₹₹")

    if "$$$" in text:
        score += 5
        matched.append("$$$")

    return score, matched


# ============================================================
# NUMERIC PATTERNS
# ============================================================

OTP_REGEX = re.compile(r"\b\d{4,8}\b")
PHONE_REGEX = re.compile(r"\b\d{10}\b")
AMOUNT_REGEX = re.compile(r"(₹|rs\.?|inr)\s?\d+", re.IGNORECASE)


def _score_numbers(text: str):

    score = 0
    matched = []

    otp_matches = OTP_REGEX.findall(text)

    if otp_matches:
        score += 10
        matched.append("numeric code")

    phone_matches = PHONE_REGEX.findall(text)

    if phone_matches:
        score += 5
        matched.append("phone number")

    amount_matches = AMOUNT_REGEX.findall(text)

    if amount_matches:
        score += 5
        matched.append("money amount")

    return score, matched


# ============================================================
# FINAL SCORE CALCULATOR
# ============================================================

def _calculate_score(original_text: str):

    text = _normalize_text(original_text)

    score, matched = _base_score(text)

    cap_score, cap_match = _score_capitals(original_text)
    score += cap_score
    matched.extend(cap_match)

    punct_score, punct_match = _score_punctuation(original_text)
    score += punct_score
    matched.extend(punct_match)

    number_score, number_match = _score_numbers(text)
    score += number_score
    matched.extend(number_match)

    matched = _unique(matched)

    score = min(score, MAX_RULE_SCORE)

    return score, matched


# ============================================================
# PUBLIC API
# ============================================================

def score_rules(text: str) -> dict:
    """
    Analyze text using the SCANLY rule engine.

    Returns:
    {
        "score": int (0-100),
        "matched": list[str]
    }
    """

    # -----------------------------
    # Empty input
    # -----------------------------
    if not text or not text.strip():
        return {
            "score": 0,
            "matched": []
        }

    try:

        score, matched = _calculate_score(text)

        score = max(0, min(score, MAX_RULE_SCORE))

        return {
            "score": score,
            "matched": matched
        }

    except Exception as e:

        # Never let the rule engine crash the API.
        print(f"[RuleEngine] {e}")

        return {
            "score": 0,
            "matched": []
        }