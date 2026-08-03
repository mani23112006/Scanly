"""
SCANLY — Risk Scoring Engine v2
Combines RoBERTa + Rule Engine + URL Checker into one weighted score.
Day 8 adds: timing, confidence, payment receipt detection.
"""

import time
from rules        import score_rules
from url_checker  import check_url
from ml.roberta.predict import predict as ml_predict

# ── Weights ─────────────────────────────────────────
ML_WEIGHT   = 0.50
RULE_WEIGHT = 0.30
URL_WEIGHT  = 0.20

# ── Thresholds ──────────────────────────────────────
SAFE_MAX       = 30
SUSPICIOUS_MAX = 70

# ── Model version ───────────────────────────────────
MODEL_VERSION = "roberta-base-finetuned-v1"

# ── Payment receipt whitelist ───────────────────────
# Legitimate banking/payment patterns — RoBERTa wasn't trained on these
_PAYMENT_PATTERNS = [
    "payment successful",
    "transaction id",
    "upi id",
    "powered by upi",
    "debited from account",
    "credited to account",
    "amount debited",
    "amount credited",
    "bank reference",
    "state bank of india",
    "hdfc bank",
    "icici bank",
    "axis bank",
    "bank of baroda",
    "paytm",
    "google pay",
    "phonepe",
    "razorpay",
    "rupees only",
    "payment receipt",
    "transaction successful",
    "ref no",
    "utr no",
]

def _is_payment_receipt(text: str) -> bool:
    """
    Detect if text is a legitimate payment/banking receipt.
    Returns True if 3+ payment patterns found.
    RoBERTa is unreliable on formal banking language —
    this override reduces its weight when triggered.
    """
    text_lower = text.lower()
    matches    = sum(1 for p in _PAYMENT_PATTERNS if p in text_lower)
    return matches >= 3


# ── Category mapping ────────────────────────────────
def get_category(score: int) -> str:
    if score <= SAFE_MAX:
        return "Safe"
    elif score <= SUSPICIOUS_MAX:
        return "Suspicious"
    else:
        return "Scam"

    

# ── Explanation builder ──────────────────────────────
def build_explanation(
    category: str,
    matched_keywords: list,
    url_reasons: list,
    ml_score: int,
    confidence: float,
    is_receipt: bool = False,
) -> str:
    if category == "Safe":
        if is_receipt:
            return "Appears to be a legitimate payment receipt. No scam indicators detected."
        return "No significant scam indicators detected."

    reasons = []

    if is_receipt:
        reasons.append("Note: Payment receipt detected — ML weight reduced")

    if matched_keywords:
        reasons.append(f"Scam keywords: {', '.join(matched_keywords)}")

    if url_reasons:
        reasons.extend(url_reasons)

    if ml_score > 60 and not is_receipt:
        reasons.append(f"AI model: {confidence:.0%} scam confidence")

    return " | ".join(reasons) if reasons else "Suspicious language patterns detected."


# ── Main scan function ───────────────────────────────
def scan(text: str) -> dict:
    """
    Full scoring pipeline.
    Args:   text — raw message (may include URLs)
    Returns: complete risk result dict
    """
    t0 = time.time()

    # ── 1. RoBERTa ML score ─────────────────────────
    try:
        rob_result  = ml_predict(text)
        ml_score    = int(rob_result["probability"] * 100)
        confidence  = round(rob_result["confidence"], 4)
        rob_ms      = rob_result.get("inference_ms", 0)
    except Exception as e:
        print(f"[WARN] RoBERTa failed: {e}")
        ml_score, confidence, rob_ms = 50, 0.5, 0

    # ── 2. Rule engine ──────────────────────────────
    rule_result      = score_rules(text)
    rule_score       = rule_result["score"]
    matched_keywords = rule_result["matched"]

    # ── 3. URL checker ──────────────────────────────
    url_result   = check_url(text)
    url_score    = url_result["url_score"]
    flagged_urls = url_result["urls_found"]
    url_reasons  = url_result["reasons"]

    # ── 4. Payment receipt detection ────────────────
    is_receipt = _is_payment_receipt(text)

    # ── 5. Dynamic weighted score ───────────────────
    if is_receipt:
        # RoBERTa unreliable on formal banking language
        # Shift weight heavily to rule engine (no scam keywords = safe)
        final = int(
            (ml_score   * 0.20) +
            (rule_score * 0.50) +
            (url_score  * 0.30)
        )
    elif ml_score >= 80:
        # High ML confidence → trust it more
        final = int(
            (ml_score   * 0.60) +
            (rule_score * 0.25) +
            (url_score  * 0.15)
        )
    elif ml_score <= 20:
        # ML says very safe → rules and URL matter more
        final = int(
            (ml_score   * 0.40) +
            (rule_score * 0.35) +
            (url_score  * 0.25)
        )
   

           # ── 6. Keyword boost ────────────────────────────
    kw_count = len(matched_keywords)
    if kw_count >= 3:
        final = min(final + 15, 100)
    elif kw_count >= 2:
        final = min(final + 8, 100)

    final = min(final, 100)

    # ── 7. Category + explanation ───────────────────
    category    = get_category(final)
    explanation = build_explanation(
        category, matched_keywords, url_reasons,
        ml_score, confidence, is_receipt
    )

    # ── 8. Total processing time ────────────────────
    elapsed_ms = int((time.time() - t0) * 1000)

    return {
        # Core scores
        "final_score":         final,
        "category":            category,
        "confidence":          confidence,
        "ml_score":            ml_score,
        "rule_score":          rule_score,
        "url_score":           url_score,

        # Details
        "matched_keywords":    matched_keywords,
        "flagged_urls":        flagged_urls,
        "url_reasons":         url_reasons,
        "explanation":         explanation,

        # Metadata
        "model_version":       MODEL_VERSION,
        "is_payment_receipt":  is_receipt,
        "processing_time_ms":  elapsed_ms,
        "inference_ms":        rob_ms,

    }