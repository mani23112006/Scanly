from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

# ── INPUT ──────────────────────────────────────────
class ScanRequest(BaseModel):
    text: str
    url: Optional[str] = None   # optional extra URL field

    @validator("text")
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        if len(v) > 5000:
            raise ValueError("Text too long (max 5000 characters)")
        return v.strip()

# ── SCAN OUTPUT ────────────────────────────────────
class ScanResponse(BaseModel):
    status:           str
    input_text:       str
    final_score:      int
    category:         str
    ml_score:         int
    rule_score:       int
    url_score:        int
    matched_keywords: list
    explanation:      str

# ── HISTORY ITEM ───────────────────────────────────
# Shape of one scan record returned from MongoDB
class HistoryItem(BaseModel):
    id:               Optional[str] = None
    input_text:       str
    final_score:      int
    category:         str
    ml_score:         int
    rule_score:       int
    url_score:        int
    matched_keywords: list
    flagged_urls:     list
    explanation:      str
    timestamp:        Optional[str] = None

# ── HISTORY RESPONSE ───────────────────────────────
class HistoryResponse(BaseModel):
    status: str
    count:  int
    scans:  List[HistoryItem]



# ── Image Scan Response ─────────────────────────────
# Extends ScanResponse with OCR-specific metadata
class ImageScanResponse(BaseModel):
    status:            str
    filename:          Optional[str] = None
    file_size_kb:      Optional[float] = None

    # OCR metadata
    extracted_text:    str
    ocr_confidence:    float
    ocr_quality:       str
    ocr_lines:         int
    ocr_warning:       Optional[str] = None
    ocr_ms:            int

    # Scoring (same as ScanResponse)
    final_score:       int
    category:          str
    confidence:        Optional[float] = None
    ml_score:          int
    rule_score:        int
    url_score:         int
    matched_keywords:  list
    flagged_urls:      Optional[list] = None
    explanation:       str
    model_version:     Optional[str] = None

    # Timing
    inference_ms:      Optional[int] = None
    total_ms:          Optional[int] = None

    # No-text response fields
    message:           Optional[str] = None