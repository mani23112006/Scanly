from dotenv import load_dotenv
import os
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime, timezone

from models import ScanRequest, ScanResponse, HistoryResponse, HistoryItem
from scorer import scan as run_scan
from db import scans_collection
from ml.roberta.predict import _load_model, get_model_status

# ── Rate limiter ────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── Lifespan: runs on server startup ───────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load RoBERTa model before accepting requests."""
    print("[Startup] Pre-loading RoBERTa model...")
    _load_model()
    print("[Startup] Server ready to accept requests.")
    yield
    # Shutdown cleanup (optional)
    print("[Shutdown] Server shutting down.")

# ── App ─────────────────────────────────────────────
app = FastAPI(
    title="SCANLY API",
    description="AI-powered scam detection — RoBERTa + Rules + URL Analysis",
    version="2.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ────────────────────────────────────────────
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health ──────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "SCANLY API v2.0 — RoBERTa powered", "version": "2.0.0"}

@app.get("/health")
async def health():
    status = get_model_status()
    return {
        "status":        "ok",
        "version":       "2.0.0",
        "model_loaded":  status["model_loaded"],
        "model_version": status["model_version"],
        "device":        status["device"],
    }

# ── Scan ─────────────────────────────────────────────
@app.post("/scan", response_model=ScanResponse)
@limiter.limit("10/minute")
async def scan(request: Request, body: ScanRequest):
    text = body.text
    if body.url:
        text = text + " " + body.url

    result = run_scan(text)

    # Save to MongoDB
    scan_doc = {
        "input_text":       body.text,
        "final_score":      result["final_score"],
        "category":         result["category"],
        "confidence":       result["confidence"],
        "ml_score":         result["ml_score"],
        "rule_score":       result["rule_score"],
        "url_score":        result["url_score"],
        "matched_keywords": result["matched_keywords"],
        "flagged_urls":     result.get("flagged_urls", []),
        "explanation":      result["explanation"],
        "model_version":    result.get("model_version", "roberta-base-finetuned-v1"),
        "timestamp":        datetime.now(timezone.utc).isoformat(),
    }
    try:
        scans_collection.insert_one(scan_doc)
    except Exception as e:
        print(f"[WARN] MongoDB save failed: {e}")

    return ScanResponse(
        status="success",
        input_text=body.text,
        final_score=result["final_score"],
        category=result["category"],
        ml_score=result["ml_score"],
        rule_score=result["rule_score"],
        url_score=result["url_score"],
        matched_keywords=result["matched_keywords"],
        explanation=result["explanation"],
    )

# ── History ──────────────────────────────────────────
@app.get("/history", response_model=HistoryResponse)
async def get_history(limit: int = 20):
    try:
        cursor = scans_collection.find(
            {}, {"_id": 1, "input_text": 1, "final_score": 1,
                 "category": 1, "ml_score": 1, "rule_score": 1,
                 "url_score": 1, "matched_keywords": 1,
                 "flagged_urls": 1, "explanation": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(limit)

        scans = [HistoryItem(
            id=str(doc["_id"]),
            input_text=doc.get("input_text",""),
            final_score=doc.get("final_score",0),
            category=doc.get("category","Unknown"),
            ml_score=doc.get("ml_score",0),
            rule_score=doc.get("rule_score",0),
            url_score=doc.get("url_score",0),
            matched_keywords=doc.get("matched_keywords",[]),
            flagged_urls=doc.get("flagged_urls",[]),
            explanation=doc.get("explanation",""),
            timestamp=doc.get("timestamp",""),
        ) for doc in cursor]

        return HistoryResponse(status="success", count=len(scans), scans=scans)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/history")
async def clear_history():
    try:
        r = scans_collection.delete_many({})
        return {"status":"success","deleted":r.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
