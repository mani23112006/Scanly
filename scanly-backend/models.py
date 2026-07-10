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