"""
SCANLY — OCR Text Extraction Module
Extracts clean text from image screenshots using EasyOCR.

Features
--------
✓ Singleton EasyOCR reader
✓ English + Hindi OCR
✓ Auto image rotation (EXIF)
✓ Resize oversized images
✓ Sharpen blurry text
✓ Contrast & brightness enhancement
✓ Confidence filtering
✓ OCR quality assessment
"""

import io
import re
import threading
import time

import easyocr
import numpy as np
from PIL import (
    Image,
    ImageEnhance,
    ImageFilter,
)

from ocr.config import (
    OCR_LANGUAGES,
    USE_GPU,
    MIN_CONFIDENCE,
    MAX_DIMENSION_PX,
    MIN_DIMENSION_PX,
    LOW_CONFIDENCE_THRESHOLD,
    MIN_TEXT_LENGTH,
    AUTO_ROTATE,
    SHARPEN_TEXT,
    MIN_TEXT_CHARS,
)

# --------------------------------------------------
# Singleton globals
# --------------------------------------------------

_reader = None
_lock = threading.Lock()
_loaded_at = None


def _load_reader():
    """
    Load EasyOCR reader once.
    Thread-safe singleton.
    """
    global _reader, _loaded_at

    if _reader is not None:
        return

    with _lock:

        if _reader is not None:
            return

        start = time.time()

        print(f"[OCR] Loading EasyOCR reader (langs={OCR_LANGUAGES})...")
        print("[OCR] First startup may download OCR models...")

        _reader = easyocr.Reader(
            OCR_LANGUAGES,
            gpu=USE_GPU,
            verbose=False,
        )

        _loaded_at = time.time()

        print(
            f"[OCR] Reader ready in "
            f"{round(_loaded_at-start,2)}s ✓"
        )


def _preprocess_image(img: Image.Image) -> Image.Image:
    """
    Enhanced preprocessing.

    Steps
    -----
    1. RGB conversion
    2. Auto rotation
    3. Size validation
    4. Resize large images
    5. Sharpen text
    6. Improve contrast
    7. Improve brightness
    """

    img = img.convert("RGB")

    # -----------------------------
    # Auto rotate phone images
    # -----------------------------

    if AUTO_ROTATE:
        try:
            from PIL import ExifTags

            exif = img._getexif()

            if exif:

                for tag, value in exif.items():

                    if ExifTags.TAGS.get(tag) == "Orientation":

                        rotations = {
                            3: 180,
                            6: 270,
                            8: 90,
                        }

                        if value in rotations:
                            img = img.rotate(
                                rotations[value],
                                expand=True,
                            )

                        break

        except Exception:
            pass

    # -----------------------------
    # Validate size
    # -----------------------------

    w, h = img.size

    if (
        w < MIN_DIMENSION_PX
        or h < MIN_DIMENSION_PX
    ):
        raise ValueError(
            f"Image too small ({w}×{h}px). "
            f"Minimum size: "
            f"{MIN_DIMENSION_PX}×{MIN_DIMENSION_PX}px"
        )

    # -----------------------------
    # Resize oversized image
    # -----------------------------

    if (
        w > MAX_DIMENSION_PX
        or h > MAX_DIMENSION_PX
    ):

        ratio = min(
            MAX_DIMENSION_PX / w,
            MAX_DIMENSION_PX / h,
        )

        new_w = int(w * ratio)
        new_h = int(h * ratio)

        img = img.resize(
            (new_w, new_h),
            Image.LANCZOS,
        )

        print(
            f"[OCR] Resized image: "
            f"{w}×{h} → {new_w}×{new_h}"
        )

    # -----------------------------
    # Sharpen text
    # -----------------------------

    if SHARPEN_TEXT:
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.SHARPEN)

    # -----------------------------
    # Improve contrast
    # -----------------------------

    img = ImageEnhance.Contrast(
        img
    ).enhance(1.3)

    # -----------------------------
    # Slight brightness boost
    # -----------------------------

    img = ImageEnhance.Brightness(
        img
    ).enhance(1.05)

    return img


def _clean_text(raw: str) -> str:
    """
    Clean OCR output.
    """

    if not raw:
        return ""

    clean = re.sub(
        r"[^\w\s.,!?@/:;%#&()\-+=₹$€£¥]",
        " ",
        raw,
    )

    clean = re.sub(
        r"\s+",
        " ",
        clean,
    )

    return clean.strip()


def extract_text(image_bytes: bytes) -> dict:
    """
    Extract text from image bytes.
    """

    _load_reader()

    start = time.time()

    try:
        img = Image.open(
            io.BytesIO(image_bytes)
        )

        img = _preprocess_image(img)

    except Exception as e:
        raise ValueError(
            f"Cannot open image: {e}"
        )

    arr = np.array(img)

    results = _reader.readtext(
        arr,
        paragraph=False,
        detail=1,
        min_size=10,
    )

    elapsed_ms = int(
        (time.time() - start) * 1000
    )
        # --------------------------------------------------
    # Empty OCR result
    # --------------------------------------------------

    if not results:
        return {
            "text": "",
            "lines": [],
            "confidence_avg": 0.0,
            "word_count": 0,
            "quality": "empty",
            "warning": "No text detected in the image.",
            "ocr_ms": elapsed_ms,
        }

    # --------------------------------------------------
    # Filter low-confidence detections
    # --------------------------------------------------

    filtered = [
        (text, conf)
        for _, text, conf in results
        if conf >= MIN_CONFIDENCE
    ]

    if not filtered:
        return {
            "text": "",
            "lines": [],
            "confidence_avg": 0.0,
            "word_count": 0,
            "quality": "empty",
            "warning": (
                "Text detected but confidence was too low. "
                "Try a clearer image."
            ),
            "ocr_ms": elapsed_ms,
        }

    # --------------------------------------------------
    # Extract lines & confidence
    # --------------------------------------------------

    lines = [text for text, _ in filtered]
    confidences = [conf for _, conf in filtered]

    confidence_avg = round(
        sum(confidences) / len(confidences),
        3,
    )

    # --------------------------------------------------
    # Join & clean text
    # --------------------------------------------------

    raw_text = " ".join(lines)

    clean = _clean_text(raw_text)

    word_count = len(clean.split())

    # --------------------------------------------------
    # Quality Assessment
    # --------------------------------------------------

    warning = None

    if confidence_avg < LOW_CONFIDENCE_THRESHOLD:

        quality = "low"

        warning = (
            f"Low OCR confidence ({confidence_avg:.0%}). "
            "Results may be inaccurate. "
            "Try a clearer screenshot."
        )

    elif len(clean) < MIN_TEXT_LENGTH:

        quality = "low"

        warning = (
            "Very little text detected. "
            "Make sure the image is a readable screenshot."
        )

    else:

        quality = "good"

    # --------------------------------------------------
    # Reject extremely short OCR output
    # --------------------------------------------------

    if len(clean) < MIN_TEXT_CHARS and quality != "empty":

        quality = "low"

        warning = (
            f"Only {len(clean)} characters extracted. "
            "Image may not be a text screenshot. "
            "Try a clearer image with more visible text."
        )

    # --------------------------------------------------
    # Return OCR result
    # --------------------------------------------------

    return {
        "text": clean,
        "lines": lines,
        "confidence_avg": confidence_avg,
        "word_count": word_count,
        "quality": quality,
        "warning": warning,
        "ocr_ms": elapsed_ms,
    }


def get_ocr_status() -> dict:
    """
    Return OCR reader status.
    Used by /health endpoint.
    """

    return {
        "ocr_loaded": _reader is not None,
        "ocr_languages": OCR_LANGUAGES,
        "ocr_gpu": USE_GPU,
        "loaded_at": _loaded_at,
    }