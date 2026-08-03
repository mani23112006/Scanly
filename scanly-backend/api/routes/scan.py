"""
===========================================================
SCANLY — Scan Routes
===========================================================

Purpose
-------
This file contains all scanning-related API endpoints.

Endpoints
---------
POST /scan/text
    • Scan plain text for scam indicators.
    • Pipeline:
      RoBERTa → Rule Engine → URL Checker → Final Score

POST /scan/image
    • Scan screenshots/images.
    • Pipeline:
      OCR → RoBERTa → Rule Engine → URL Checker → Final Score

POST /scan/url
    • Analyse a single URL.
    • Uses rule-based URL analysis only (no ML model).

Why this file?
--------------
Instead of putting every endpoint inside main.py,
all scan routes are organized here using FastAPI APIRouter.

Benefits:
✓ Cleaner project structure
✓ Easier maintenance
✓ Modular routing
✓ Production-ready organization
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Request, UploadFile, File
from slowapi import Limiter
from slowapi.util import get_remote_address

from models import (
    ScanRequest,
    ScanResponse,
    ImageScanResponse,
    URLScanRequest,
    URLScanResponse,
)

from scorer import scan as run_scan
from services.image_scanner import scan_image as _image_service
from services.url_scanner import scan_url_only

from db import scans_collection

from core.logging import get_logger
from core.exceptions import ModelNotLoadedError


# --------------------------------------------------------
# Router
# --------------------------------------------------------

router = APIRouter(
    prefix="/scan",
    tags=["Scanning"],
)

limiter = Limiter(
    key_func=get_remote_address,
)

logger = get_logger(__name__)


# --------------------------------------------------------
# Helper: Save Scan History
# --------------------------------------------------------

def _save_to_db(
    input_text: str,
    result: dict,
    scan_type: str = "text",
):
    """
    Save completed scan into MongoDB.

    Any database failure is logged but does NOT
    stop the API response.
    """

    try:

        doc = {
            "input_text": input_text,
            "final_score": result.get("final_score", 0),
            "category": result.get("category", "Unknown"),
            "confidence": result.get("confidence", 0.0),
            "ml_score": result.get("ml_score", 0),
            "rule_score": result.get("rule_score", 0),
            "url_score": result.get("url_score", 0),
            "matched_keywords": result.get(
                "matched_keywords",
                [],
            ),
            "flagged_urls": result.get(
                "flagged_urls",
                [],
            ),
            "explanation": result.get(
                "explanation",
                "",
            ),
            "model_version": result.get(
                "model_version",
                "roberta-base-finetuned-v1",
            ),
            "scan_type": scan_type,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        scans_collection.insert_one(doc)

        logger.info(
            f"Saved {scan_type} scan "
            f"to MongoDB "
            f"(score={result.get('final_score')})"
        )

    except Exception as e:

        logger.warning(
            f"Failed to save scan history: {e}"
        )


# --------------------------------------------------------
# POST /scan/text
# --------------------------------------------------------

@router.post(
    "/text",
    response_model=ScanResponse,
)
@limiter.limit("10/minute")
async def scan_text(
    request: Request,
    body: ScanRequest,
):
    """
    Scan a text message.

    Pipeline:
    RoBERTa
        ↓
    Rule Engine
        ↓
    URL Checker
        ↓
    Final Weighted Score
    """

    logger.info(
        f"Text scan request "
        f"({len(body.text)} characters)"
    )

    text = body.text

    if body.url:
        text += " " + body.url

    try:

        result = run_scan(text)

    except Exception as e:

        logger.error(
            f"Scoring pipeline failed: {e}"
        )

        raise ModelNotLoadedError()

    _save_to_db(
        body.text,
        result,
        scan_type="text",
    )

    return ScanResponse(
    status="success",
   input_text=body.text,
    final_score=result["final_score"],
    category=result["category"],

    # New fields
    confidence=result.get("confidence"),
    model_version=result.get("model_version"),
    processing_time_ms=result.get("processing_time_ms"),

    # Existing fields
    ml_score=result["ml_score"],
    rule_score=result["rule_score"],
    url_score=result["url_score"],
    matched_keywords=result["matched_keywords"],
    explanation=result["explanation"],
)


# --------------------------------------------------------
# POST /scan/image
# --------------------------------------------------------

@router.post(
    "/image",
    response_model=ImageScanResponse,
)
@limiter.limit("5/minute")
async def scan_image(
    request: Request,
    file: UploadFile = File(...),
):
    """
    Scan an uploaded screenshot.

    Pipeline:
    OCR
        ↓
    RoBERTa
        ↓
    Rule Engine
        ↓
    URL Checker
        ↓
    Final Score
    """

    logger.info(
        f"Image scan request: "
        f"{file.filename} "
        f"({file.content_type})"
    )

    result = await _image_service(file)

    return result


# --------------------------------------------------------
# POST /scan/url
# --------------------------------------------------------

@router.post(
    "/url",
    response_model=URLScanResponse,
)
@limiter.limit("20/minute")
async def scan_url(
    request: Request,
    body: URLScanRequest,
):
    """
    Analyse a single URL.

    This endpoint performs only URL analysis.
    No ML model is used.
    """

    logger.info(
        f"URL scan request: {body.url[:60]}"
    )

    result = scan_url_only(body.url)

    return URLScanResponse(**result)