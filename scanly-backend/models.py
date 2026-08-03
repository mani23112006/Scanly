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
    status: str
    input_text: str
    final_score: int
    category: str

    # ── NEW fields (Day 8) ──────────────────────────
    confidence: Optional[float] = None          # RoBERTa confidence (0.0–1.0)
    model_version: Optional[str] = None         # e.g. roberta-base-finetuned-v1
    processing_time_ms: Optional[int] = None    # Total scan processing time

    # ── Existing fields ─────────────────────────────
    ml_score: int
    rule_score: int
    url_score: int
    matched_keywords: List[str]
    explanation: str


# ── HISTORY ITEM ───────────────────────────────────
class HistoryItem(BaseModel):
    id: Optional[str] = None
    input_text: str
    final_score: int
    category: str
    ml_score: int
    rule_score: int
    url_score: int
    matched_keywords: List[str]
    flagged_urls: List[str]
    explanation: str
    timestamp: Optional[str] = None


# ── HISTORY RESPONSE ───────────────────────────────
class HistoryResponse(BaseModel):
    status: str
    count: int
    scans: List[HistoryItem]


# ── IMAGE SCAN RESPONSE ────────────────────────────
class ImageScanResponse(BaseModel):
    status: str
    filename: Optional[str] = None
    file_size_kb: Optional[float] = None

    # OCR metadata
    extracted_text: str
    ocr_confidence: float
    ocr_quality: str
    ocr_lines: int
    ocr_warning: Optional[str] = None
    ocr_ms: int

    # Scoring
    final_score: int
    category: str
    confidence: Optional[float] = None
    ml_score: int
    rule_score: int
    url_score: int
    matched_keywords: List[str]
    flagged_urls: Optional[List[str]] = None
    explanation: str
    model_version: Optional[str] = None

    # Timing
    inference_ms: Optional[int] = None
    total_ms: Optional[int] = None

    # No-text response
    message: Optional[str] = None


# ── URL SCAN REQUEST ───────────────────────────────
class URLScanRequest(BaseModel):
    url: str

    @validator("url")
    def url_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("URL cannot be empty")

        v = v.strip()

        if len(v) < 4:
            raise ValueError("URL too short")

        return v


# ── URL CHECKS ─────────────────────────────────────
class URLChecks(BaseModel):
    uses_ip: bool = False
    uses_http: bool = False
    suspicious_tld: bool = False
    too_long: bool = False
    too_many_subs: bool = False
    suspicious_path: bool = False
    url_shortener: bool = False


# ── URL SCAN RESPONSE ──────────────────────────────
class URLScanResponse(BaseModel):
    status: str
    url: str
    url_score: int
    final_score: int
    category: str
    reasons: List[str]
    explanation: str