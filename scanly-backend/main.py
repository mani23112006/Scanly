from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ScanRequest, ScanResponse
from rules import score_rules              # ← import rule engine

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

    # ── REAL rule score (Day 4) ────────────────────
    rule_result  = score_rules(text)
    rule_score   = rule_result["score"]
    matched_keywords = rule_result["matched"]

    # ── Still placeholder scores (Days 7-8) ────────
    fake_ml_score  = 70
    fake_url_score = 0

    # Weighted final: ML=50%, Rules=30%, URL=20%
    final_score = int(
        (fake_ml_score  * 0.5) +
        (rule_score     * 0.3) +
        (fake_url_score * 0.2)
    )

    # Cap at 100
    final_score = min(final_score, 100)

    # Category
    if final_score <= 30:
        category    = "Safe"
        explanation = "No scam indicators detected."
    elif final_score <= 70:
        category    = "Suspicious"
        explanation = f"Suspicious patterns found. Triggered by: {', '.join(matched_keywords) if matched_keywords else 'general language patterns'}."
    else:
        category    = "Scam"
        explanation = f"High risk content detected. Triggered by: {', '.join(matched_keywords)}. Do not share personal info."

    return ScanResponse(
        status="success",
        input_text=text,
        final_score=final_score,
        category=category,
        ml_score=fake_ml_score,
        rule_score=rule_score,
        url_score=fake_url_score,
        matched_keywords=matched_keywords,
        explanation=explanation
    )