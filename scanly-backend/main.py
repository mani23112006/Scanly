from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from models import ScanRequest, ScanResponse, HistoryResponse, HistoryItem
from scorer import scan as run_scan
from db import scans_collection

app = FastAPI(
    title="SCANLY API",
    description="AI-powered scam detection — ML + Rules + URL Analysis",
    version="1.0.0"
)

# ── CORS ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── HEALTH ROUTES ──────────────────────────────────
@app.get("/")
async def root():
    return {"message": "SCANLY backend is running!", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

# ── SCAN ENDPOINT ──────────────────────────────────
@app.post("/scan", response_model=ScanResponse)
async def scan(request: ScanRequest):
    """
    Main scan endpoint.
    Accepts text (+ optional url), runs full AI analysis,
    saves result to MongoDB, returns risk JSON.
    """
    text = request.text

    # If user passed a separate URL field, append it to text
    # so url_checker picks it up automatically
    if request.url:
        text = text + " " + request.url

    # ── Run full scoring pipeline ───────────────────
    result = run_scan(text)

    # ── Save to MongoDB ─────────────────────────────
    scan_doc = {
        "input_text":       request.text,
        "final_score":      result["final_score"],
        "category":         result["category"],
        "ml_score":         result["ml_score"],
        "rule_score":       result["rule_score"],
        "url_score":        result["url_score"],
        "matched_keywords": result["matched_keywords"],
        "flagged_urls":     result.get("flagged_urls", []),
        "explanation":      result["explanation"],
        "timestamp":        datetime.now(timezone.utc).isoformat()
    }

    try:
        scans_collection.insert_one(scan_doc)
    except Exception as e:
        # Don't crash the API if MongoDB is down — just log it
        print(f"[WARN] Could not save to MongoDB: {e}")

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


# ── HISTORY ENDPOINT ───────────────────────────────
@app.get("/history", response_model=HistoryResponse)
async def get_history(limit: int = 20):
    """
    Fetch the last N scan results from MongoDB.
    Default: last 20 scans. Pass ?limit=50 for more.
    """
    try:
        # Sort by timestamp descending (newest first)
        cursor = scans_collection.find(
            {},
            {"_id": 1, "input_text": 1, "final_score": 1,
             "category": 1, "ml_score": 1, "rule_score": 1,
             "url_score": 1, "matched_keywords": 1,
             "flagged_urls": 1, "explanation": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(limit)

        scans = []
        for doc in cursor:
            scans.append(HistoryItem(
                id=str(doc["_id"]),
                input_text=doc.get("input_text", ""),
                final_score=doc.get("final_score", 0),
                category=doc.get("category", "Unknown"),
                ml_score=doc.get("ml_score", 0),
                rule_score=doc.get("rule_score", 0),
                url_score=doc.get("url_score", 0),
                matched_keywords=doc.get("matched_keywords", []),
                flagged_urls=doc.get("flagged_urls", []),
                explanation=doc.get("explanation", ""),
                timestamp=doc.get("timestamp", "")
            ))

        return HistoryResponse(
            status="success",
            count=len(scans),
            scans=scans
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch history: {str(e)}"
        )

# ── DELETE HISTORY (bonus) ─────────────────────────
@app.delete("/history")
async def clear_history():
    """Clear all scan history from MongoDB."""
    try:
        result = scans_collection.delete_many({})
        return {
            "status": "success",
            "deleted": result.deleted_count,
            "message": f"Deleted {result.deleted_count} scan records"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not clear history: {str(e)}"
        )