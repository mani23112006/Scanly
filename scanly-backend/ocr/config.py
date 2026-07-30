"""
OCR configuration — file limits, supported types, image constraints.
"""

# ── File validation ─────────────────────────────────
MAX_IMAGE_SIZE_MB = 10
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/bmp",
    "image/tiff",
}

ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png",
    ".webp", ".gif", ".bmp", ".tiff"
}

# ── Image preprocessing ─────────────────────────────
MAX_DIMENSION_PX = 4000     # resize if width or height exceeds this
MIN_DIMENSION_PX = 50       # reject images smaller than this
OCR_DPI = 200               # target DPI for best OCR accuracy

# ── OCR settings ────────────────────────────────────
OCR_LANGUAGES    = ["en"]   # add "hi" for Hindi support later
USE_GPU          = False     # set True if CUDA available
MIN_CONFIDENCE   = 0.3      # ignore text blocks below this confidence
MIN_TEXT_LENGTH  = 10       # reject extracted text shorter than this

# ── Quality thresholds ──────────────────────────────
LOW_CONFIDENCE_THRESHOLD  = 0.4    # warn user about image quality
HIGH_CONFIDENCE_THRESHOLD = 0.7    # good quality scan