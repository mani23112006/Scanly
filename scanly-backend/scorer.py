"""
SCANLY — Hybrid Risk Scoring Engine (v3)

Combines:
- RoBERTa Spam Classifier
- Rule Engine
- URL Reputation

with intelligent score fusion.
"""

import time

from rules import score_rules
from url_checker import check_url
from ml.roberta.predict import predict as ml_predict

# ==========================================================
# MODEL INFO
# ==========================================================

MODEL_VERSION = "roberta-base-finetuned-v3"

# ==========================================================
# SCORE WEIGHTS
# ==========================================================

ML_WEIGHT = 0.50
RULE_WEIGHT = 0.30
URL_WEIGHT = 0.20

# Receipt-specific weights
RECEIPT_ML_WEIGHT = 0.20
RECEIPT_RULE_WEIGHT = 0.50
RECEIPT_URL_WEIGHT = 0.30

# ==========================================================
# CATEGORY THRESHOLDS
# ==========================================================

SAFE_MAX = 30
SUSPICIOUS_MAX = 70

# ==========================================================
# PAYMENT RECEIPT WHITELIST
# ==========================================================

_PAYMENT_PATTERNS = {

    # Generic
    "payment successful",
    "payment received",
    "payment receipt",

    # Transaction
    "transaction successful",
    "transaction id",
    "transaction no",
    "transaction reference",
    "reference number",
    "txn",
    "txn id",
    "utr",
    "upi ref",

    # Debit / Credit
    "amount debited",
    "amount credited",
    "debited",
    "credited",
    "debited from account",
    "credited to account",

    # Balance
    "available balance",
    "account balance",

    # Banking
    "imps",
    "neft",
    "rtgs",

    # Salary / Cashback
    "salary credited",
    "cashback credited",

    # Wallets
    "google pay",
    "phonepe",
    "paytm",
    "bhim",

    # UPI
    "upi id",
    "powered by upi",

    # Banks
    "state bank of india",
    "hdfc bank",
    "icici bank",
    "axis bank",
    "bank of baroda",

    # References
    "bank reference",
    "account ending",
    "ending with",
    "a/c",
}

# ==========================================================
# PHISHING TERMS
# If any of these appear, receipt detection is disabled.
# ==========================================================

_PHISHING_TERMS = {

    # OTP
    "otp",
    "share otp",

    # Verification
    "verify",
    "verify now",
    "verify account",

    # Account
    "blocked",
    "account blocked",
    "suspended",
    "account suspended",

    # KYC
    "kyc",
    "update kyc",

    # Credentials
    "cvv",
    "pin",

    # Links
    "click here",

    # Urgency
    "urgent",
    "immediately",
    "within 24 hours",

    # Rewards
    "winner",
    "lottery",
    "claim now",
    "claim reward",

    # Banking
    "bank account",

    # Security
    "security alert",
}

# ==========================================================
# CRITICAL KEYWORDS
# These can force a Scam classification later.
# ==========================================================

CRITICAL_KEYWORDS = {

    "share otp",
    "account blocked",
    "account suspended",
    "verify account",
    "verify now",
    "click here",
    "update kyc",
    "cvv",
    "pin",

    # Combination keywords from rules.py
    "otp + blocked",
    "otp + verify",
    "bank + click here",
    "upi + verify",
}

# ==========================================================
# PAYMENT RECEIPT DETECTOR
# ==========================================================

def _is_payment_receipt(text: str) -> bool:
    """
    Returns True only if:
      • multiple payment indicators exist
      • NO phishing indicators exist
    """

    text = text.lower()

    payment_matches = sum(
        keyword in text
        for keyword in _PAYMENT_PATTERNS
    )

    phishing_found = any(
        keyword in text
        for keyword in _PHISHING_TERMS
    )

    return payment_matches >= 3 and not phishing_found


# ==========================================================
# CATEGORY
# ==========================================================

def get_category(score: int) -> str:

    if score <= SAFE_MAX:
        return "Safe"

    if score <= SUSPICIOUS_MAX:
        return "Suspicious"

    return "Scam"


# ==========================================================
# EXPLANATION ENGINE
# ==========================================================

def _format_keywords(matched_keywords):
    """
    Convert keyword list into a readable string.
    """
    if not matched_keywords:
        return None

    return "Matched keywords: " + ", ".join(sorted(set(matched_keywords)))


def _format_urls(flagged_urls):
    """
    Format detected URLs.
    """
    if not flagged_urls:
        return None

    return "Detected URL(s): " + ", ".join(flagged_urls)


def _format_url_reasons(url_reasons):
    """
    Format URL reputation reasons.
    """
    if not url_reasons:
        return None

    return "URL Analysis: " + "; ".join(url_reasons)


def _format_ai(ml_score, confidence):
    """
    AI explanation.
    """

    if ml_score >= 80:
        return f"AI model strongly predicts scam ({confidence:.0%} confidence)."

    if ml_score >= 50:
        return f"AI model found suspicious patterns ({confidence:.0%} confidence)."

    return None


# ==========================================================
# BUILD EXPLANATION
# ==========================================================

def build_explanation(
    category,
    matched_keywords,
    flagged_urls,
    url_reasons,
    ml_score,
    confidence,
    is_receipt=False,
):
    """
    Build a human-readable explanation for the scan result.
    """

    # -------------------------
    # Genuine payment receipt
    # -------------------------
    if is_receipt and category == "Safe":
        return (
            "This appears to be a legitimate payment notification. "
            "No phishing indicators were detected."
        )

    # -------------------------
    # Safe message
    # -------------------------
    if category == "Safe":
        return (
            "No significant scam indicators were detected."
        )

    explanation_parts = []

    # -------------------------
    # Keywords
    # -------------------------
    keyword_text = _format_keywords(matched_keywords)
    if keyword_text:
        explanation_parts.append(keyword_text)

    # -------------------------
    # URLs
    # -------------------------
    url_text = _format_urls(flagged_urls)
    if url_text:
        explanation_parts.append(url_text)

    # -------------------------
    # URL Reasons
    # -------------------------
    reason_text = _format_url_reasons(url_reasons)
    if reason_text:
        explanation_parts.append(reason_text)

    # -------------------------
    # AI
    # -------------------------
    ai_text = _format_ai(
        ml_score,
        confidence,
    )

    if ai_text:
        explanation_parts.append(ai_text)

    # -------------------------
    # Receipt override
    # -------------------------
    if is_receipt:
        explanation_parts.append(
            "Payment-related terms detected."
        )

    # -------------------------
    # Fallback
    # -------------------------
    if not explanation_parts:
        explanation_parts.append(
            "Suspicious patterns detected."
        )

    return " | ".join(explanation_parts)


# ==========================================================
# RISK FUSION ENGINE
# ==========================================================

def _has_critical_keywords(matched_keywords):
    """
    Returns True if any critical phishing keyword was detected.
    """
    return any(
        keyword in CRITICAL_KEYWORDS
        for keyword in matched_keywords
    )


def _compute_base_score(
    ml_score,
    rule_score,
    url_score,
    is_receipt,
):
    """
    Compute weighted score before applying overrides.
    """

    if is_receipt:
        return round(
            (ml_score * RECEIPT_ML_WEIGHT)
            + (rule_score * RECEIPT_RULE_WEIGHT)
            + (url_score * RECEIPT_URL_WEIGHT)
        )

    return round(
        (ml_score * ML_WEIGHT)
        + (rule_score * RULE_WEIGHT)
        + (url_score * URL_WEIGHT)
    )


def _apply_keyword_boost(score, keyword_count):
    """
    More scam indicators → slightly higher confidence.
    """

    if keyword_count >= 6:
        score += 20

    elif keyword_count >= 4:
        score += 15

    elif keyword_count >= 2:
        score += 8

    return score


def _apply_overrides(
    score,
    ml_score,
    rule_score,
    url_score,
    matched_keywords,
    is_receipt,
):
    """
    Override score for strong phishing evidence.
    """

    # --------------------------------------------------
    # Genuine payment receipt
    # --------------------------------------------------
    if is_receipt and rule_score < 20 and url_score == 0:
        return min(score, 25)

    # --------------------------------------------------
    # Critical phishing keywords
    # --------------------------------------------------
    if _has_critical_keywords(matched_keywords):
        score = max(score, 75)

    # --------------------------------------------------
    # Rule engine extremely confident
    # --------------------------------------------------
    if rule_score >= 80:
        score = max(score, 85)

    # --------------------------------------------------
    # Dangerous URL
    # --------------------------------------------------
    if url_score >= 80:
        score = max(score, 85)

    # --------------------------------------------------
    # AI extremely confident
    # --------------------------------------------------
    if ml_score >= 95:
        score = max(score, 90)

    # --------------------------------------------------
    # Multiple engines agree
    # --------------------------------------------------
    if (
        ml_score >= 60
        and rule_score >= 50
    ):
        score += 10

    if (
        rule_score >= 50
        and url_score >= 50
    ):
        score += 10

    if (
        ml_score >= 60
        and url_score >= 50
    ):
        score += 10

    return min(score, 100)


def calculate_final_score(
    ml_score,
    rule_score,
    url_score,
    matched_keywords,
    is_receipt,
):
    """
    Central risk fusion function.

    Returns
    -------
    int
        Final score between 0 and 100.
    """

    score = _compute_base_score(
        ml_score,
        rule_score,
        url_score,
        is_receipt,
    )

    score = _apply_keyword_boost(
        score,
        len(matched_keywords),
    )

    score = _apply_overrides(
        score,
        ml_score,
        rule_score,
        url_score,
        matched_keywords,
        is_receipt,
    )

    return max(0, min(score, 100))

# ==========================================================
# MAIN SCAN FUNCTION
# ==========================================================

def scan(text: str):
    """
    Main Scan Pipeline

    Flow:
        1. AI Model
        2. Rule Engine
        3. URL Checker
        4. Payment Receipt Detection
        5. Risk Fusion
        6. Category
        7. Explanation
    """

    start = time.time()

    # --------------------------------------------------
    # AI Prediction
    # --------------------------------------------------

    try:

        ml_result = ml_predict(text)

        ml_score = round(
            ml_result["probability"] * 100
        )

        confidence = ml_result["confidence"]

        inference_ms = ml_result.get(
            "inference_ms",
            0
        )

    except Exception as e:

        print(f"[RoBERTa ERROR] {e}")

        ml_score = 50
        confidence = 0.50
        inference_ms = 0

    # --------------------------------------------------
    # Rule Engine
    # --------------------------------------------------

    rule_result = score_rules(text)

    rule_score = rule_result["score"]

    matched_keywords = rule_result["matched"]

    # --------------------------------------------------
    # URL Checker
    # --------------------------------------------------

    url_result = check_url(text)

    url_score = url_result["url_score"]

    flagged_urls = url_result["urls_found"]

    url_reasons = url_result["reasons"]

    # --------------------------------------------------
    # Receipt Detection
    # --------------------------------------------------

    is_receipt = _is_payment_receipt(text)

    # --------------------------------------------------
    # Final Risk Score
    # --------------------------------------------------

    final_score = calculate_final_score(

        ml_score=ml_score,

        rule_score=rule_score,

        url_score=url_score,

        matched_keywords=matched_keywords,

        is_receipt=is_receipt,

    )

    # --------------------------------------------------
    # Category
    # --------------------------------------------------

    category = get_category(final_score)

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    explanation = build_explanation(

        category=category,

        matched_keywords=matched_keywords,

        flagged_urls=flagged_urls,

        url_reasons=url_reasons,

        ml_score=ml_score,

        confidence=confidence,

        is_receipt=is_receipt,

    )

    # --------------------------------------------------
    # Processing Time
    # --------------------------------------------------

    processing_time_ms = int(
        (time.time() - start) * 1000
    )

    # --------------------------------------------------
    # API Response
    # --------------------------------------------------

    return {

        # Overall
        "final_score": final_score,
        "category": category,
        "confidence": confidence,

        # Breakdown
        "ml_score": ml_score,
        "rule_score": rule_score,
        "url_score": url_score,

        # Details
        "matched_keywords": matched_keywords,
        "flagged_urls": flagged_urls,
        "url_reasons": url_reasons,
        "explanation": explanation,

        # Metadata
        "model_version": MODEL_VERSION,
        "is_payment_receipt": is_receipt,
        "processing_time_ms": processing_time_ms,
        "inference_ms": inference_ms,
    }