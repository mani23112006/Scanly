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
# To this — enables Hindi scam message detection:
ENABLE_HINDI  = True    # set False to skip Hindi (faster startup)
OCR_LANGUAGES = ["en", "hi"] if ENABLE_HINDI else ["en"]


AUTO_ROTATE   = True    # try to fix tilted screenshots
SHARPEN_TEXT  = True    # enhance text clarity before OCR
MIN_TEXT_CHARS = 20     # reject images with fewer than 20 chars extracted
USE_GPU          = False     # set True if CUDA available
MIN_CONFIDENCE   = 0.3      # ignore text blocks below this confidence
MIN_TEXT_LENGTH  = 10       # reject extracted text shorter than this

# ── Quality thresholds ──────────────────────────────
LOW_CONFIDENCE_THRESHOLD  = 0.4    # warn user about image quality
HIGH_CONFIDENCE_THRESHOLD = 0.7    # good quality scan