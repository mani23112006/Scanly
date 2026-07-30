# Confidence score batata hai ki EasyOCR ko apne prediction par kitna bharosa hai. MIN_CONFIDENCE = 0.3 ka matlab hai: "Jis text par 30% ya usse zyada confidence ho, sirf wahi accept karo; baaki doubtful detections ignore kar do."

"""
SCANLY — OCR Text Extraction Module
Extracts clean text from image screenshots using EasyOCR.
Singleton pattern: reader loads once, reused across all requests.
"""

import io
import re
import threading
import time

import easyocr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from ocr.config import (
    OCR_LANGUAGES, USE_GPU, MIN_CONFIDENCE,
    MAX_DIMENSION_PX, MIN_DIMENSION_PX,
    LOW_CONFIDENCE_THRESHOLD, MIN_TEXT_LENGTH
)

# ── Singleton globals ───────────────────────────────
_reader    = None
_lock      = threading.Lock()
_loaded_at = None


def _load_reader():
    """Load EasyOCR reader once. Thread-safe singleton."""
    global _reader, _loaded_at

    if _reader is not None:
        return

    with _lock:
        if _reader is not None:
            return

        t0 = time.time()
        print(f"[OCR] Loading EasyOCR reader (langs: {OCR_LANGUAGES})...")
        print("[OCR] First run downloads model ~200MB — please wait...")

        _reader = easyocr.Reader(
            OCR_LANGUAGES,
            gpu=USE_GPU,
            verbose=False,          # suppress noisy internal logs
        )

        _loaded_at = time.time()
        elapsed    = round(_loaded_at - t0, 2)
        print(f"[OCR] Reader ready in {elapsed}s ✓")


def _preprocess_image(img: Image.Image) -> Image.Image:
    """
    Preprocess image for better OCR accuracy:
    1. Convert to RGB
    2. Resize if too large (performance)
    3. Enhance contrast (helps with low-quality screenshots)
    """
    # Convert to RGB (handles RGBA, palette images, etc.)
    img = img.convert("RGB")

     # Reject images that are too small
    w, h = img.size
    if w < MIN_DIMENSION_PX or h < MIN_DIMENSION_PX:
        raise ValueError(
            f"Image too small ({w}×{h}px). "
            f"Minimum: {MIN_DIMENSION_PX}×{MIN_DIMENSION_PX}px"
        )

    # Resize if too large (keeps aspect ratio)
    if w > MAX_DIMENSION_PX or h > MAX_DIMENSION_PX:
        ratio  = min(MAX_DIMENSION_PX / w, MAX_DIMENSION_PX / h)
        new_w  = int(w * ratio)
        new_h  = int(h * ratio)
        img    = img.resize((new_w, new_h), Image.LANCZOS)
        print(f"[OCR] Resized image: {w}×{h} → {new_w}×{new_h}")

    # Enhance contrast slightly — helps with faded/dark screenshots
    img = ImageEnhance.Contrast(img).enhance(1.2)

    return img


def _clean_text(raw: str) -> str:
    """
    Clean raw OCR output:
    - Remove noise characters
    - Collapse multiple spaces/newlines
    - Strip leading/trailing whitespace
    """
    if not raw:
        return ""

    # Remove characters that are almost certainly OCR noise
    # Keep: letters, digits, spaces, common punctuation
    clean = re.sub(r"[^\w\s.,!?@/:;%#&()\-+=₹$€£¥]", " ", raw)

    # Collapse multiple spaces
    clean = re.sub(r"\s+", " ", clean)

    return clean.strip()


def extract_text(image_bytes: bytes) -> dict:
    """
    Extract text from raw image bytes.

    Args:
        image_bytes: raw bytes of the uploaded image file

    Returns:
        {
            text:           str   — cleaned joined text
            lines:          list  — individual text lines from OCR
            confidence_avg: float — average OCR confidence (0–1)
            word_count:     int   — number of words extracted
            quality:        str   — "good" / "low" / "empty"
            warning:        str   — optional quality warning message
        }
    """
    _load_reader()

    t0 = time.time()

    # ── Open + preprocess image ─────────────────────
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = _preprocess_image(img)
    except Exception as e:
        raise ValueError(f"Cannot open image: {e}")

    # Convert to numpy array for EasyOCR
    arr = np.array(img)

       # ── Run OCR ─────────────────────────────────────
    # Returns list of (bbox, text, confidence)
    results = _reader.readtext(
        arr,
        paragraph=False,      # return individual text blocks
        detail=1,             # include confidence scores
        min_size=10,          # ignore tiny text
    )

    elapsed_ms = int((time.time() - t0) * 1000)

    # ── Empty result ─────────────────────────────────
    if not results:
        return {
            "text":           "",
            "lines":          [],
            "confidence_avg": 0.0,
            "word_count":     0,
            "quality":        "empty",
            "warning":        "No text detected in the image.",
            "ocr_ms":         elapsed_ms,
        }

    # ── Filter by confidence ────────────────────────
    # Ignore very low-confidence detections (likely noise)
    filtered = [(r[1], r[2]) for r in results if r[2] >= MIN_CONFIDENCE]

    if not filtered:
        return {
            "text":           "",
            "lines":          [],
            "confidence_avg": 0.0,
            "word_count":     0,
            "quality":        "empty",
            "warning":        "Text detected but confidence too low. Try a clearer image.",
            "ocr_ms":         elapsed_ms,
        }

    lines     = [f[0] for f in filtered]
    confs     = [f[1] for f in filtered]
    conf_avg  = round(sum(confs) / len(confs), 3)

    # ── Join and clean ──────────────────────────────
    raw_text  = " ".join(lines)
    clean     = _clean_text(raw_text)
    words     = len(clean.split())

    # ── Quality assessment ──────────────────────────
    warning = None
    if conf_avg < LOW_CONFIDENCE_THRESHOLD:
        quality = "low"
        warning = f"Low OCR confidence ({conf_avg:.0%}). Results may be inaccurate. Try a clearer screenshot."
    elif len(clean) < MIN_TEXT_LENGTH:
        quality = "low"
        warning = "Very little text detected. Make sure the image is a readable screenshot."
    else:
        quality = "good"

    return {
        "text":           clean,
        "lines":          lines,
        "confidence_avg": conf_avg,
        "word_count":     words,
        "quality":        quality,
        "warning":        warning,
        "ocr_ms":         elapsed_ms,
    }

def get_ocr_status() -> dict:
    """Return OCR reader status — used by /health endpoint."""
    return {
        "ocr_loaded":    _reader is not None,
        "ocr_languages": OCR_LANGUAGES,
        "ocr_gpu":       USE_GPU,
        "loaded_at":     _loaded_at,
    }