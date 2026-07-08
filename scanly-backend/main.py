from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ScanRequest, ScanResponse
from rules import score_rules
from url_checker import check_url              # ← NEW import

app = FastAPI(
    title="SCANLY API",
    description="AI-based scam detection system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SCANLY backend is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    text = request.text

    # ── Rule score (Day 4) — REAL ──────────────────
    rule_result      = score_rules(text)
    rule_score       = rule_result["score"]
    matched_keywords = rule_result["matched"]

    # ── URL score (Day 5) — REAL ───────────────────
    url_result  = check_url(text)
    url_score   = url_result["url_score"]
    url_reasons = url_result["reasons"]
    urls_found  = url_result["urls_found"]

    # ── ML score (Day 7) — still placeholder ───────
    fake_ml_score = 70

    # ── Weighted final score ────────────────────────
    # ML=50%, Rules=30%, URL=20%
    final_score = int(
        (fake_ml_score * 0.5) +
        (rule_score    * 0.3) +
        (url_score     * 0.2)
    )
    final_score = min(final_score, 100)

    # ── Category ────────────────────────────────────
    if final_score <= 30:
        category    = "Safe"
        explanation = "No scam indicators detected."
    elif final_score <= 70:
        category    = "Suspicious"
        explanation = "Suspicious patterns detected. Be cautious."
    else:
        category    = "Scam"
        explanation = "High risk content. Do not share personal info."

    # ── Build explanation from all signals ──────────
    all_reasons = []
    if matched_keywords:
        all_reasons.append(f"Keywords: {', '.join(matched_keywords)}")
    if url_reasons:
        all_reasons.extend(url_reasons)
    if all_reasons:
        explanation += " Reason(s): " + " | ".join(all_reasons)

    return ScanResponse(
        status="success",
        input_text=text,
        final_score=final_score,
        category=category,
        ml_score=fake_ml_score,
        rule_score=rule_score,
        url_score=url_score,
        matched_keywords=matched_keywords,
        explanation=explanation
    )