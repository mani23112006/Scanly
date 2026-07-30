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

from fastapi import UploadFile, File
from models  import ScanRequest, ScanResponse, HistoryResponse, HistoryItem, ImageScanResponse
from services.image_scanner import scan_image as _scan_image_service
from ocr.extract import get_ocr_status

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
    ml_status  = get_model_status()
    ocr_status = get_ocr_status()
    return {
        "status":        "ok",
        "version":       "2.0.0",
        "model_loaded":  ml_status["model_loaded"],
        "model_version": ml_status["model_version"],
        "device":        ml_status["device"],
        "ocr_loaded":    ocr_status["ocr_loaded"],
        "ocr_languages": ocr_status["ocr_languages"],
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



# ── Image scan — FULL pipeline ──────────────────────
@app.post("/scan/image", response_model=ImageScanResponse)
@limiter.limit("5/minute")
async def scan_image(
    request: Request,
    file: UploadFile = File(...)
):
    """
    Upload a screenshot (WhatsApp/SMS/email/payment).
    Pipeline: OCR → RoBERTa → Rules → URL → Risk Score
    Returns same schema as /scan/text plus OCR metadata.
    """
    result = await _scan_image_service(file)
    return result

    # ── Validate file type ──────────────────────────
    content_type = file.content_type or ""
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: '{content_type}'. "
                   f"Allowed: jpg, png, webp, gif, bmp"
        )

    # ── Read + validate size ────────────────────────
    image_bytes = await file.read()
    size_mb     = len(image_bytes) / (1024 * 1024)

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Image too large ({size_mb:.1f}MB). "
                   f"Maximum allowed: 10MB"
        )

    # ── Extract text via OCR ────────────────────────
    try:
        ocr_result = extract_text(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )

    # ── Return stub response  ────────────────
    # Full scoring 
    return {
        "status":          "ocr_only",       # will be "success" on Day 5
        "filename":        file.filename,
        "file_size_kb":    round(size_mb * 1024, 1),
        "extracted_text":  ocr_result["text"],
        "ocr_lines":       ocr_result["lines"],
        "ocr_confidence":  ocr_result["confidence_avg"],
        "word_count":      ocr_result["word_count"],
        "quality":         ocr_result["quality"],
        "warning":         ocr_result["warning"],
        "ocr_ms":          ocr_result["ocr_ms"],
        "note":            "Scoring pipeline coming Day 5. OCR extraction works!"
    }
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
