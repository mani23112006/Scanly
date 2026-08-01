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
    