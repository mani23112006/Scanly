"""
SCANLY — Image Scan Service
Connects OCR extraction → full scoring pipeline.
Reuses scorer.py exactly as /scan/text does.
"""

import time
from datetime import datetime, timezone

from fastapi import UploadFile, HTTPException
from db import scans_collection

from ocr.extract import extract_text
from ocr.config  import (
    MAX_IMAGE_SIZE_BYTES, ALLOWED_MIME_TYPES,
    LOW_CONFIDENCE_THRESHOLD
)
from scorer import scan as run_scan


async def scan_image(file: UploadFile) -> dict:
    """
    Full image scanning pipeline:
    1. Validate file type + size
    2. Extract text via OCR
    3. Run full scoring pipeline
    4. Return merged response

    Args:
        file: FastAPI UploadFile from multipart form

    Returns:
        dict with full scan result + OCR metadata
    """
    t0 = time.time()

    # ── 1. Validate file type ───────────────────────
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Unsupported file type: '{content_type}'. "
                f"Please upload a JPG, PNG, WEBP, GIF, or BMP image."
            )
        )

    # ── 2. Read file + validate size ────────────────
    image_bytes = await file.read()
    size_mb     = len(image_bytes) / (1024 * 1024)

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=(
                f"Image too large ({size_mb:.1f}MB). "
                f"Maximum allowed size is 10MB."
            )
        )

    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=422,
            detail="Empty file received. Please upload a valid image."
        )

    # ── 3. OCR — extract text from image ────────────
    try:
        ocr_result = extract_text(image_bytes)
    except ValueError as e:
        # Image too small, corrupt, etc.
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )

    extracted_text = ocr_result["text"]
    ocr_confidence = ocr_result["confidence_avg"]
    ocr_quality    = ocr_result["quality"]
    ocr_warning    = ocr_result["warning"]
    ocr_ms         = ocr_result["ocr_ms"]


    # ── 4. Handle empty / unreadable image ──────────
    if not extracted_text.strip():
        return {
            "status":          "no_text",
            "message":         (
                ocr_warning or
                "No readable text found in the image. "
                "Please upload a clear screenshot with visible text."
            ),
            "filename":        file.filename,
            "extracted_text":  "",
            "ocr_confidence":  ocr_confidence,
            "ocr_quality":     ocr_quality,
            "ocr_lines":       0,
            "final_score":     0,
            "category":        "Safe",
            "ml_score":        0,
            "rule_score":      0,
            "url_score":       0,
            "matched_keywords": [],
            "explanation":     "No text could be extracted from the image.",
            "total_ms":        int((time.time() - t0) * 1000),
        }

    # ── 5. Run full scoring pipeline ─────────────────
    # Reuses scorer.py exactly — no separate image model needed
    try:
        score_result = run_scan(extracted_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scoring pipeline failed: {str(e)}"
        )

    total_ms = int((time.time() - t0) * 1000)

    # ── 6. Build response ────────────────────────────
    # Merge score result with OCR metadata
    response = {
        "status":          "success",
        "filename":        file.filename,
        "file_size_kb":    round(size_mb * 1024, 1),

        # OCR metadata
        "extracted_text":  extracted_text,
        "ocr_confidence":  ocr_confidence,
        "ocr_quality":     ocr_quality,
        "ocr_lines":       len(ocr_result["lines"]),
        "ocr_warning":     ocr_warning,
        "ocr_ms":          ocr_ms,

        # Scoring results (from scorer.py — same as /scan/text)
        "final_score":     score_result["final_score"],
        "category":        score_result["category"],
        "confidence":      score_result.get("confidence", 0.0),
        "ml_score":        score_result["ml_score"],
        "rule_score":      score_result["rule_score"],
        "url_score":       score_result["url_score"],
        "matched_keywords": score_result["matched_keywords"],
        "flagged_urls":    score_result.get("flagged_urls", []),
        "explanation":     score_result["explanation"],
        "model_version":   score_result.get("model_version", "roberta-base-finetuned-v1"),

        # Timing
        "inference_ms":    score_result.get("inference_ms", 0),
        "total_ms":        total_ms,
    }

    # ── 7. Low confidence warning override ──────────
    # If OCR wasn't very confident, surface that warning prominently
    if ocr_confidence < LOW_CONFIDENCE_THRESHOLD and ocr_warning:
        response["explanation"] = (
            f"⚠ Low OCR quality ({ocr_confidence:.0%} confidence) — "
            f"results may be inaccurate. " + response["explanation"]
        )

  # ── 8. Save to MongoDB ──────────────────────────
    # Image scans appear in history alongside text scans
    scan_doc = {
        "input_text":       f"[IMAGE: {file.filename}] {extracted_text[:200]}",
        "final_score":      response["final_score"],
        "category":         response["category"],
        "confidence":       response.get("confidence", 0.0),
        "ml_score":         response["ml_score"],
        "rule_score":       response["rule_score"],
        "url_score":        response["url_score"],
        "matched_keywords": response["matched_keywords"],
        "flagged_urls":     response.get("flagged_urls", []),
        "explanation":      response["explanation"],
        "scan_type":        "image",           # NEW field — easy to filter later
        "ocr_confidence":   response["ocr_confidence"],
        "model_version":    response.get("model_version", "roberta-base-finetuned-v1"),
        "timestamp":        datetime.now(timezone.utc).isoformat(),
    }
    try:
        scans_collection.insert_one(scan_doc)
    except Exception as e:
        print(f"[WARN] MongoDB save failed for image scan: {e}")
        
    return response

