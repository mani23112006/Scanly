import re
import urllib.parse

# ─────────────────────────────────────────────────────
# URL Shorteners
# ─────────────────────────────────────────────────────
SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl",
    "ow.ly", "is.gd", "buff.ly", "short.link",
    "cutt.ly", "rb.gy", "rebrand.ly"
}

# ─────────────────────────────────────────────────────
# Suspicious TLDs
# ─────────────────────────────────────────────────────
SUSPICIOUS_TLDS = {
    ".xyz", ".tk", ".ml", ".ga", ".cf",
    ".gq", ".pw", ".top", ".click",
    ".link", ".buzz", ".work", ".live"
}

# ─────────────────────────────────────────────────────
# Trusted Official Domains
# ─────────────────────────────────────────────────────
SAFE_DOMAINS = {

    # Google
    "google.com",
    "google.co.in",
    "gmail.com",
    "youtube.com",

    # Microsoft
    "microsoft.com",
    "outlook.com",
    "live.com",
    "office.com",

    # Apple
    "apple.com",
    "icloud.com",

    # Amazon
    "amazon.com",
    "amazon.in",

    # Meta
    "facebook.com",
    "instagram.com",
    "whatsapp.com",

    # X
    "x.com",
    "twitter.com",

    # LinkedIn
    "linkedin.com",

    # Git
    "github.com",
    "gitlab.com",

    # Cloud
    "aws.amazon.com",
    "azure.microsoft.com",
    "cloudflare.com",

    # Payments
    "paypal.com",
    "stripe.com",
    "razorpay.com",
    "phonepe.com",
    "paytm.com",
    "gpay.com",

    # Banks
    "sbi.co.in",
    "onlinesbi.sbi",
    "hdfcbank.com",
    "icicibank.com",
    "axisbank.com",
    "kotak.com",
    "pnbindia.in",
    "bankofbaroda.in",
    "canarabank.com",

    # Govt
    "uidai.gov.in",
    "digilocker.gov.in",
    "gst.gov.in",
    "incometax.gov.in",
    "irctc.co.in",
    "npci.org.in",

    # Others
    "netflix.com",
    "adobe.com",
    "oracle.com",
    "dropbox.com",
    "discord.com"
}

# ─────────────────────────────────────────────────────
# Suspicious keywords in domain
# ─────────────────────────────────────────────────────
DOMAIN_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "secure",
    "update",
    "signin",
    "account",
    "bank",
    "otp",
    "wallet",
    "payment",
    "confirm"
]

# ─────────────────────────────────────────────────────
# Suspicious path keywords
# ─────────────────────────────────────────────────────
PATH_KEYWORDS = [
    "verify",
    "login",
    "secure",
    "update",
    "signin",
    "password",
    "credential",
    "wallet",
    "otp",
    "confirm",
    "account"
]

# ─────────────────────────────────────────────────────
# Brand names scammers impersonate
# ─────────────────────────────────────────────────────
BRANDS = [
    "google",
    "gmail",
    "amazon",
    "paypal",
    "apple",
    "microsoft",
    "github",
    "facebook",
    "instagram",
    "linkedin",
    "netflix",
    "sbi",
    "hdfc",
    "icici",
    "axis",
    "kotak",
    "phonepe",
    "paytm",
    "gpay",
    "razorpay",
    "stripe",
    "upi"
]

URL_PATTERN = re.compile(
    r'https?://[^\s<>"{}|\\^`\[\]]+'
    r'|www\.[^\s<>"{}|\\^`\[\]]+',
    re.IGNORECASE
)


def extract_urls(text: str):
    return URL_PATTERN.findall(text)


def is_safe_domain(domain):
    return any(
        domain == d or domain.endswith("." + d)
        for d in SAFE_DOMAINS
    )


def check_single_url(url: str):

    score = 0
    reasons = []

    if not url.startswith("http"):
        url = "http://" + url

    try:
        parsed = urllib.parse.urlparse(url)
    except:
        return {
            "score": 0,
            "reasons": ["Could not parse URL"]
        }

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()

    domain = netloc.split(":")[0]

    # IP Address
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain):
        score += 30
        reasons.append("Uses IP address")

    # HTTP
    if scheme == "http":
        score += 25
        reasons.append("HTTP not HTTPS")

    # Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 20
            reasons.append(f"Suspicious TLD ({tld})")
            break

    # Long URL
    if len(url) > 75:
        score += 20
        reasons.append("Very long URL")

    # Too many subdomains
    if len(domain.split(".")) >= 4:
        score += 15
        reasons.append("Too many subdomains")



            # Safe domain
    safe = is_safe_domain(domain)

    # -------------------------------
    # Brand impersonation
    # -------------------------------
    if not safe:
        for brand in BRANDS:
            if brand in domain:
                score += 20
                reasons.append(f"Brand impersonation ({brand})")

    # -------------------------------
    # Suspicious domain keywords
    # -------------------------------
    if not safe:
        for keyword in DOMAIN_KEYWORDS:
            if keyword in domain:
                score += 10
                reasons.append(f"Domain keyword ({keyword})")

    # -------------------------------
    # Suspicious path keywords
    # -------------------------------
    for keyword in PATH_KEYWORDS:
        if keyword in path:
            score += 10
            reasons.append(f"Path keyword ({keyword})")

    # -------------------------------
    # Multiple hyphens
    # -------------------------------
    hyphen_count = domain.count("-")
    if hyphen_count >= 2:
        score += 10
        reasons.append("Multiple hyphens in domain")

    # -------------------------------
    # URL shortener
    # -------------------------------
    for shortener in SHORTENERS:
        if shortener == domain or domain.endswith("." + shortener):
            score += 15
            reasons.append(f"URL shortener ({shortener})")
            break

    # -------------------------------
    # @ symbol
    # -------------------------------
    if "@" in url:
        score += 20
        reasons.append("@ symbol in URL")

    # -------------------------------
    # Encoded URL
    # -------------------------------
    if "%" in url:
        score += 10
        reasons.append("Encoded characters")

    # -------------------------------
    # Multiple redirects
    # -------------------------------
    if "//" in path:
        score += 10
        reasons.append("Multiple redirects")

    # -------------------------------
    # Excessive dots
    # -------------------------------
    if domain.count(".") >= 4:
        score += 10
        reasons.append("Too many dots")

    score = min(score, 100)

    return {
        "score": score,
        "reasons": list(dict.fromkeys(reasons))
    }


def check_url(text: str):
    """
    Extract URLs from text and return highest score.
    """

    urls = extract_urls(text)

    if not urls:
        return {
            "url_score": 0,
            "urls_found": [],
            "reasons": []
        }

    highest_score = 0
    reasons = []

    for url in urls:

        result = check_single_url(url)

        highest_score = max(highest_score, result["score"])

        for reason in result["reasons"]:
            if reason not in reasons:
                reasons.append(reason)

    return {
        "url_score": highest_score,
        "urls_found": urls,
        "reasons": reasons
    }