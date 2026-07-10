from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ScanRequest, ScanResponse
from scorer import scan as run_scan        # ← single import now

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
    """
    Accepts text input, returns full risk analysis.
    All scoring logic is handled by scorer.py.
    """
    result = run_scan(request.text)

    return ScanResponse(
        status="success",
        input_text=request.text,
        final_score=result["final_score"],
        category=result["category"],
        ml_score=result["ml_score"],
        rule_score=result["rule_score"],
        url_score=result["url_score"],
        matched_keywords=result["matched_keywords"],
        explanation=result["explanation"]
    )