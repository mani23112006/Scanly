"""
SCANLY API v2.0 — Main Entry Point
This file only:
  1. Creates the FastAPI app
  2. Adds middleware (CORS, rate limiting)
  3. Registers routers
  4. Registers exception handlers
  5. Pre-loads ML model on startup

All business logic lives in api/routes/ and services/.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

load_dotenv()

from api.routes.scan    import router as scan_router
from api.routes.history import router as history_router
from ml.roberta.predict import _load_model, get_model_status
from ocr.extract        import get_ocr_status
from core.exceptions    import register_handlers
from core.logging       import get_logger

logger = get_logger("scanly.main")


# ── Startup / Shutdown ──────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SCANLY API v2.0 starting up...")
    logger.info("Pre-loading RoBERTa model...")
    _load_model()
    logger.info("Server ready to accept requests.")
    yield
    logger.info("SCANLY API shutting down.")


# ── App ─────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="SCANLY API",
    description="AI-powered scam detection — RoBERTa + Rules + URL + Image OCR",
    version="2.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ─────────────────────────────────────────────
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────
app.include_router(scan_router)       # /scan/text, /scan/url, /scan/image
app.include_router(history_router)    # /history GET, /history DELETE

# ── Exception handlers ───────────────────────────────
register_handlers(app)


# ── Health + Root ────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {"message": "SCANLY API v2.0", "version": "2.0.0", "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health():
    ml  = get_model_status()
    ocr = get_ocr_status()
    return {
        "status":        "ok",
        "version":       "2.0.0",
        "model_loaded":  ml["model_loaded"],
        "model_version": ml["model_version"],
        "device":        ml["device"],
        "ocr_loaded":    ocr["ocr_loaded"],
        "ocr_languages": ocr["ocr_languages"],
    }