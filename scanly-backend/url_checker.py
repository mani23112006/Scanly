import re
import urllib.parse

# ── URL shortener domains to flag ──────────────────
SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl",
    "ow.ly", "is.gd", "buff.ly", "short.link",
    "cutt.ly", "rb.gy"
}

# ── Suspicious TLDs (free / scammer-used) ──────────
SUSPICIOUS_TLDS = {
    ".xyz", ".tk", ".ml", ".ga", ".cf",
    ".gq", ".pw", ".top", ".click", ".link"
}

# ── Suspicious path keywords ────────────────────────
SUSPICIOUS_PATHS = [
    "verify", "login", "secure", "account",
    "banking", "update", "confirm", "signin",
    "password", "credential", "wallet", "otp"
]

# ── Regex to extract URLs from any text ────────────
URL_PATTERN = re.compile(
    r'https?://[^\s<>"{}|\\^`\[\]]+'
    r'|www\.[^\s<>"{}|\\^`\[\]]+',
    re.IGNORECASE
)


def extract_urls(text: str) -> list:
    """Find all URLs inside a text string."""
    return URL_PATTERN.findall(text)


def check_single_url(url: str) -> dict:
    """
    Analyze one URL and return a score + reasons list.

    Args:
        url: a single URL string

    Returns:
        {"score": int, "reasons": list}
    """
    score   = 0
    reasons = []

    # Make sure URL has a scheme for parsing
    if not url.startswith("http"):
        url = "http://" + url

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return {"score": 0, "reasons": ["Could not parse URL"]}

    scheme  = parsed.scheme.lower()       # http or https
    netloc  = parsed.netloc.lower()       # domain or IP
    path    = parsed.path.lower()         # /verify/account etc
    full    = url.lower()

    # ── Check 1: IP address instead of domain ──────
    ip_pattern = re.compile(
        r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
    )
    if ip_pattern.match(netloc):
        score += 30
        reasons.append("Uses IP address instead of domain name")

    # ── Check 2: HTTP not HTTPS ─────────────────────
    if scheme == "http":
        score += 25
        reasons.append("HTTP not HTTPS (no encryption)")

    # ── Check 3: Suspicious TLD ─────────────────────
    for tld in SUSPICIOUS_TLDS:
        if netloc.endswith(tld) or (tld + "/") in full:
            score += 20
            reasons.append(f"Suspicious domain extension: {tld}")
            break

    # ── Check 4: URL length > 75 characters ─────────
    if len(url) > 75:
        score += 20
        reasons.append(f"Unusually long URL ({len(url)} characters)")


    # ── Check 5: Too many subdomains (3+) ───────────
    # Remove port if present, then count dots
    domain_only = netloc.split(":")[0]
    parts = domain_only.split(".")
    if len(parts) >= 4:
        score += 15
        reasons.append(f"Too many subdomains ({len(parts) - 2} levels)")

    # ── Check 6: Suspicious path keywords ───────────
    for keyword in SUSPICIOUS_PATHS:
        if keyword in path:
            score += 15
            reasons.append(f"Suspicious path keyword: /{keyword}")
            break   # only flag once even if multiple keywords match

    # ── Check 7: URL shortener ──────────────────────
    for shortener in SHORTENERS:
        if shortener in netloc:
            score += 15
            reasons.append(f"URL shortener detected: {shortener}")
            break

    # Cap at 100
    score = min(score, 100)

    return {"score": score, "reasons": reasons}


def check_url(text: str) -> dict:
    """
    Main function — extract all URLs from text,
    score each one, return the highest score + all reasons.

    Args:
        text: full message text (may or may not contain URLs)

    Returns:
        {
            "url_score":    int,
            "urls_found":   list,
            "reasons":      list
        }
    """
    urls = extract_urls(text)

    if not urls:
        return {
            "url_score":  0,
            "urls_found": [],
            "reasons":    []
        }

    highest_score = 0
    all_reasons   = []
    all_urls      = []

    for url in urls:
        result = check_single_url(url)
        all_urls.append(url)

        if result["score"] > highest_score:
            highest_score = result["score"]

        for reason in result["reasons"]:
            if reason not in all_reasons:
                all_reasons.append(reason)

    return {
        "url_score":  highest_score,
        "urls_found": all_urls,
        "reasons":    all_reasons
    }



    