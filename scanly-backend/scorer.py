from rules import score_rules
from url_checker import check_url
from ml.train import predict as ml_predict

# ── Scoring weights ─────────────────────────────────
ML_WEIGHT   = 0.50   # 50%
RULE_WEIGHT = 0.30   # 30%
URL_WEIGHT  = 0.20   # 20%

# ── Category thresholds ─────────────────────────────
SAFE_MAX       = 30
SUSPICIOUS_MAX = 70


def get_category(score: int) -> str:
    """Map a 0–100 score to a risk category."""
    if score <= SAFE_MAX:
        return "Safe"
    elif score <= SUSPICIOUS_MAX:
        return "Suspicious"
    else:
        return "Scam"


def build_explanation(
    category: str,
    matched_keywords: list,
    url_reasons: list,
    ml_score: int
) -> str:
    """Build a human-readable explanation of why this was flagged."""

    if category == "Safe":
        return "No significant scam indicators detected."

    reasons = []

    if matched_keywords:
        reasons.append(
            f"Scam keywords found: {', '.join(matched_keywords)}"
        )

    if url_reasons:
        for r in url_reasons:
            reasons.append(r)

    if ml_score > 60:
        reasons.append(
            f"AI model flagged this as {ml_score}% likely to be a scam"
        )

    if not reasons:
        return "Suspicious language patterns detected."

    return " | ".join(reasons)


def scan(text: str) -> dict:
    """
    Main scoring function — runs all 3 detectors,
    combines scores with weighted formula, returns full result.

    Args:
        text: raw input message (may contain URLs)

    Returns:
        {
            final_score:      int   (0–100),
            category:         str   ("Safe" / "Suspicious" / "Scam"),
            ml_score:         int   (0–100),
            rule_score:       int   (0–100),
            url_score:        int   (0–100),
            matched_keywords: list,
            flagged_urls:     list,
            url_reasons:      list,
            explanation:      str
        }
    """
    
    # ── 1. ML Score ─────────────────────────────────
    try:
        ml_probability = ml_predict(text)
        ml_score = int(ml_probability * 100)
    except Exception as e:
        print(f"[WARN] ML prediction failed: {e}")
        ml_score = 50   # neutral fallback

    # ── 2. Rule Score ────────────────────────────────
    rule_result      = score_rules(text)
    rule_score       = rule_result["score"]
    matched_keywords = rule_result["matched"]

    # ── 3. URL Score ─────────────────────────────────
    url_result   = check_url(text)
    url_score    = url_result["url_score"]
    flagged_urls = url_result["urls_found"]
    url_reasons  = url_result["reasons"]

    # ── 4. Weighted Final Score ──────────────────────
    final_score = (
        (ml_score   * ML_WEIGHT) +
        (rule_score * RULE_WEIGHT) +
        (url_score  * URL_WEIGHT)
    )
    final_score = min(int(final_score), 100)

    # ── 5. Category + Explanation ────────────────────
    category    = get_category(final_score)
    explanation = build_explanation(
        category, matched_keywords, url_reasons, ml_score
    )

    return {
        "final_score":      final_score,
        "category":         category,
        "ml_score":         ml_score,
        "rule_score":       rule_score,
        "url_score":        url_score,
        "matched_keywords": matched_keywords,
        "flagged_urls":     flagged_urls,
        "url_reasons":      url_reasons,
        "explanation":      explanation
    }


# ── Quick test — run directly ────────────────────────
if __name__ == "__main__":
    test_cases = [
        "Hey, are we meeting at 5pm today?",
        "Your account is blocked. OTP: 4829. Click http://bit.ly/free",
        "You won a prize! Verify account at http://192.168.1.1/login",
        "Congratulations! Lottery winner. Free money. Claim now urgently.",
        "Please send me the project report by tomorrow morning."
    ]

    print("=" * 60)
    print("SCANLY Scorer — Full Pipeline Test")
    print("=" * 60)

    for text in test_cases:
        result = scan(text)
        emoji = {"Safe": "🟢", "Suspicious": "🟡", "Scam": "🔴"}
        print(f"\nInput    : {text[:55]}...")
        print(f"Result   : {emoji[result['category']]} {result['category']} — Score: {result['final_score']}")
        print(f"ML       : {result['ml_score']}  Rules: {result['rule_score']}  URL: {result['url_score']}")
        print(f"Keywords : {result['matched_keywords']}")
        print(f"URLs     : {result['flagged_urls']}")
        print(f"Explain  : {result['explanation'][:80]}...")
        print("-" * 60)