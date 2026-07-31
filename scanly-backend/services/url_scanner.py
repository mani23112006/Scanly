"""
SCANLY — URL Scan Service
Dedicated URL-only scanning endpoint.
Reuses url_checker.py — no duplicate logic.
"""

import re
from url_checker import check_url, check_single_url


def _extract_urls_from_text(text: str) -> list:
    """Pull all URLs out of a text string."""
    pattern = re.compile(
        r'https?://[^\s<>"{}|\\^`\[\]]+'
        r'|www\.[^\s<>"{}|\\^`\[\]]+',
        re.IGNORECASE
    )
    return pattern.findall(text)


def _ensure_scheme(url: str) -> str:
    """Add https:// if URL has no scheme."""
    url = url.strip()
    if not url.startswith(("http://", "https://", "www.")):
        url = "https://" + url
    elif url.startswith("www."):
        url = "https://" + url
    return url


def scan_url_only(url: str) -> dict:
    """
    Analyse a single URL and return full phishing report.

    Args:
        url: raw URL string (scheme optional)

    Returns:
        Full URL risk report
    """
    url = _ensure_scheme(url)

    # Run single-URL analysis
    result = check_single_url(url)
    score  = result["score"]
    reasons = result["reasons"]

    # Map score to category
    if score >= 71:
        category = "Scam"
    elif score >= 31:
        category = "Suspicious"
    else:
        category = "Safe"

    # Build human-readable explanation
    if reasons:
        explanation = " | ".join(reasons)
    else:
        explanation = "No phishing indicators detected. URL appears clean."

    return {
        "status":       "success",
        "url":          url,
        "url_score":    score,
        "final_score":  score,
        "category":     category,
        "reasons":      reasons,
        "explanation":  explanation,
        "checks": {
            "uses_ip":          any("IP address" in r for r in reasons),
            "uses_http":        any("HTTP not HTTPS" in r for r in reasons),
            "suspicious_tld":   any("extension" in r for r in reasons),
            "too_long":         any("long URL" in r for r in reasons),
            "too_many_subs":    any("subdomain" in r for r in reasons),
            "suspicious_path":  any("path keyword" in r for r in reasons),
            "url_shortener":    any("shortener" in r for r in reasons),
        }
    }


def scan_multiple_urls(text: str) -> dict:
    """
    Extract all URLs from a text and analyse each one.
    Returns the highest-risk URL's result + all URL details.

    Used internally by scorer.py — not directly exposed as endpoint.
    """
    urls = _extract_urls_from_text(text)

    if not urls:
        return {
            "status":      "no_urls",
            "url_score":   0,
            "urls_found":  [],
            "highest_url": None,
            "all_results": [],
            "explanation": "No URLs found in the text.",
        }

    all_results    = []
    highest_score  = 0
    highest_result = None

    for url in urls:
        result = scan_url_only(url)
        all_results.append(result)
        if result["url_score"] > highest_score:
            highest_score  = result["url_score"]
            highest_result = result

    return {
        "status":      "success",
        "url_score":   highest_score,
        "urls_found":  urls,
        "highest_url": highest_result,
        "all_results": all_results,
        "explanation": highest_result["explanation"] if highest_result else "",
    }