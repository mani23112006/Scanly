from pydantic import BaseModel, validator
from typing import Optional

# ── INPUT ──────────────────────────────────────────
# This defines what the frontend must send
class ScanRequest(BaseModel):
    text: str                        # required — the message to scan
    url: Optional[str] = None        # optional — a URL to check

    @validator("text")
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        if len(v) > 5000:
            raise ValueError("Text too long (max 5000 characters)")
        return v.strip()

# ── OUTPUT ─────────────────────────────────────────
# This defines what the backend sends back
class ScanResponse(BaseModel):
    status: str                      # "success" or "error"
    input_text: str                  # the original text (trimmed)
    final_score: int                 # 0–100 risk score
    category: str                    # "Safe" / "Suspicious" / "Scam"
    ml_score: int                    # placeholder today
    rule_score: int                  # placeholder today
    url_score: int                   # placeholder today
    matched_keywords: list           # keywords that triggered rules
    explanation: str                 # human-readable reason