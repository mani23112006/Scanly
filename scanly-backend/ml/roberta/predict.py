"""
SCANLY — RoBERTa Inference Module
Loads the fine-tuned model once and caches it in memory.
All subsequent predictions use the cached model → fast inference.
"""

import os
import time
import threading
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

from ml.roberta.config import (
    SAVE_DIR, MAX_LENGTH,
    CONFIDENCE_THRESHOLD, MODEL_VERSION
)

# ── Singleton globals ───────────────────────────────
# Module-level variables — shared across all requests
_model     = None
_tokenizer = None
_lock      = threading.Lock()        # prevents double-loading on concurrent requests
_loaded_at = None                    # tracks when model was loaded

# ── Loader ──────────────────────────────────────────
def _load_model():
    """Load model + tokenizer once. Thread-safe singleton."""
    global _model, _tokenizer, _loaded_at

    if _model is not None:
        return   # already loaded — skip immediately

    with _lock:
        if _model is not None:
            return   # double-check after acquiring lock (another thread may have loaded)

        if not os.path.exists(SAVE_DIR):
            raise FileNotFoundError(
                f"RoBERTa model not found at: {SAVE_DIR}\n"
                "Run ml/roberta/train_roberta.py first to generate saved_model/"
            )

        t0 = time.time()
        print(f"[RoBERTa] Loading model from {SAVE_DIR}...")

        _tokenizer = RobertaTokenizer.from_pretrained(SAVE_DIR)
        _model     = RobertaForSequenceClassification.from_pretrained(SAVE_DIR)
        _model.eval()   # set to inference mode (disables dropout)

        print("id2label :", _model.config.id2label)
        print("label2id :", _model.config.label2id)

         
        # Use GPU if available
        if torch.cuda.is_available():
            _model = _model.cuda()
            print("[RoBERTa] Running on GPU")
        else:
            print("[RoBERTa] Running on CPU")

        _loaded_at = time.time()
        elapsed = round(_loaded_at - t0, 2)
        print(f"[RoBERTa] Model ready in {elapsed}s ✓")



# ── Predict ─────────────────────────────────────────
def predict(text: str) -> dict:
    """
    Run RoBERTa inference on a single text string.

    Args:
        text: raw message text (will be truncated to MAX_LENGTH tokens)

    Returns:
        {
            label:       "spam" or "ham"
            probability: float 0.0–1.0  (spam probability)
            confidence:  float 0.0–1.0  (max of ham or spam prob)
            ham_prob:    float 0.0–1.0
            spam_prob:   float 0.0–1.0
            inference_ms: int  (milliseconds taken)
        }
    """
    _load_model()

    if not text or not text.strip():
        return {
            "label":        "ham",
            "probability":  0.0,
            "confidence":   1.0,
            "ham_prob":     1.0,
            "spam_prob":    0.0,
            "inference_ms": 0
        }

    t0     = time.time()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Tokenize
    inputs = _tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH,
        padding=True,
    ).to(device)

    # Inference — no_grad() disables gradient tracking (faster + less memory)
    with torch.no_grad():
        logits = _model(**inputs).logits           # raw scores
        probs  = torch.softmax(logits, dim=-1)[0]  # convert to probabilities

    ham_prob  = float(probs[0])   # index 0 = ham
    spam_prob = float(probs[1])   # index 1 = spam
    label     = "spam" if spam_prob >= CONFIDENCE_THRESHOLD else "ham"
    confidence = max(ham_prob, spam_prob)
    elapsed    = int((time.time() - t0) * 1000)

    return {
        "label":        label,
        "probability":  round(spam_prob, 4),
        "confidence":   round(confidence, 4),
        "ham_prob":     round(ham_prob, 4),
        "spam_prob":    round(spam_prob, 4),
        "inference_ms": elapsed,
    }


def get_model_status() -> dict:
    """Return model loading status — used by /health endpoint."""
    return {
        "model_loaded":  _model is not None,
        "model_version": MODEL_VERSION,
        "save_dir":      SAVE_DIR,
        "device":        "cuda" if torch.cuda.is_available() else "cpu",
        "loaded_at":     _loaded_at,
    }
