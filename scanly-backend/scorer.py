from rules import score_rules
from url_checker import check_url
from ml.roberta.predict import predict as ml_predict

ML_WEIGHT = 0.50
RULE_WEIGHT = 0.30
URL_WEIGHT = 0.20

SAFE_MAX = 30
SUSPICIOUS_MAX = 70


def get_category(score: int) -> str:
    if score <= SAFE_MAX:
        return "Safe"
    elif score <= SUSPICIOUS_MAX:
        return "Suspicious"
    else:
        return "Scam"


def build_explanation(category, matched_keywords, url_reasons, ml_score, confidence):
    if category == "Safe":
        return "No significant scam indicators detected."

    reasons = []

    if matched_keywords:
        reasons.append(f"Scam keywords: {', '.join(matched_keywords)}")

    if url_reasons:
        reasons.extend(url_reasons)

    if ml_score > 60:
        reasons.append(f"AI model: {confidence:.0%} scam confidence")

    return " | ".join(reasons) if reasons else "Suspicious language patterns detected."


def scan(text: str) -> dict:
    # ── 1. RoBERTa ML score ─────────────────────────────
    try:
        rob_result = ml_predict(text)

        ml_score = int(rob_result["probability"] * 100)
        rob_confidence = rob_result["confidence"]
        rob_label = rob_result["label"]
        rob_ms = rob_result["inference_ms"]

    except Exception as e:
        print(f"[WARN] RoBERTa prediction failed: {e}")

        ml_score = 50
        rob_confidence = 0.5
        rob_label = "unknown"
        rob_ms = 0

    # ── 2. Rule score ──────────────────────────────────
    rule_result = score_rules(text)
    rule_score = rule_result["score"]
    matched_keywords = rule_result["matched"]

    # ── 3. URL score ───────────────────────────────────
    url_result = check_url(text)
    url_score = url_result["url_score"]
    flagged_urls = url_result["urls_found"]
    url_reasons = url_result["reasons"]

    # ── 4. Dynamic weighted final score ────────────────
    if ml_score >= 80:
        final = int(
            ml_score * 0.60 +
            rule_score * 0.25 +
            url_score * 0.15
        )

    elif ml_score <= 20:
        final = int(
            ml_score * 0.40 +
            rule_score * 0.35 +
            url_score * 0.25
        )

    else:
        final = int(
            ml_score * 0.50 +
            rule_score * 0.30 +
            url_score * 0.20
        )

    # Keyword Boost
    kw = len(matched_keywords)

    if kw >= 3:
        final = min(final + 15, 100)
    elif kw >= 2:
        final = min(final + 8, 100)

    final = min(final, 100)

    # ── 5. Category + explanation ──────────────────────
    category = get_category(final)

    explanation = build_explanation(
        category=category,
        matched_keywords=matched_keywords,
        url_reasons=url_reasons,
        ml_score=ml_score,
        confidence=rob_confidence,
    )

    # ── 6. Final Response ──────────────────────────────
    return {
        "final_score": final,
        "category": category,
        "confidence": round(rob_confidence, 4),
        "ml_score": ml_score,
        "rule_score": rule_score,
        "url_score": url_score,
        "matched_keywords": matched_keywords,
        "flagged_urls": flagged_urls,
        "url_reasons": url_reasons,
        "explanation": explanation,
        "model_version": "roberta-base-finetuned-v1",
        "model_label": rob_label,
        "inference_ms": rob_ms,
    }