from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ScanRequest, ScanResponse

app = FastAPI(
    title="SCANLY API",
    description="AI-based scam detection system",
    version="1.0.0"
)

# ── CORS ───────────────────────────────────────────
# Allows React (port 5173) to call this API (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── HEALTH ROUTES ──────────────────────────────────
@app.get("/")
def root():
    return {"message": "SCANLY backend is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

# ── SCAN ENDPOINT ──────────────────────────────────
@app.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    """
    Accepts a text message (and optional URL),
    returns a hardcoded risk score for now.
    Real ML + rules plug in here on Days 7-9.
    """

    text = request.text

    # ── HARDCODED LOGIC (temporary) ────────────────
    # Days 7-9 will replace this with real scores
    fake_ml_score    = 70
    fake_rule_score  = 80
    fake_url_score   = 0   # no URL checker yet

    # Weighted final score: ML=50%, Rules=30%, URL=20%
    final_score = int(
        (fake_ml_score * 0.5) +
        (fake_rule_score * 0.3) +
        (fake_url_score * 0.2)
    )

    # Determine category from score
    if final_score <= 30:
        category = "Safe"
        explanation = "No scam indicators detected."
    elif final_score <= 70:
        category = "Suspicious"
        explanation = "Some suspicious patterns found. Be cautious."
    else:
        category = "Scam"
        explanation = "High risk content detected. Do not click any links or share personal info."

    return ScanResponse(
        status="success",
        input_text=text,
        final_score=final_score,
        category=category,
        ml_score=fake_ml_score,
        rule_score=fake_rule_score,
        url_score=fake_url_score,
        matched_keywords=["placeholder — real keywords on Day 4"],
        explanation=explanation
    )