"""
SCANLY API v2.0 — Main Entry Point

Responsibilities
----------------
1. Create FastAPI app
2. Configure middleware
3. Register routers
4. Register exception handlers
5. Pre-load ML model
6. Track server uptime
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

load_dotenv()

# Routers
from api.routes.scan import router as scan_router
from api.routes.history import router as history_router

# ML / OCR
from ml.roberta.predict import _load_model, get_model_status
from ocr.extract import get_ocr_status

# Core
from core.exceptions import register_handlers
from core.logging import get_logger
from core.timer import start_timer, get_uptime

logger = get_logger("scanly.main")


# ────────────────────────────────────────────────────
# Startup / Shutdown
# ────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SCANLY API v2.0 starting up...")

    # Start uptime timer
    start_timer()

    # Pre-load RoBERTa
    logger.info("Pre-loading RoBERTa model...")
    _load_model()

    logger.info("Server ready to accept requests.")

    yield

    logger.info("SCANLY API shutting down.")


# ────────────────────────────────────────────────────
# Rate Limiter
# ────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="SCANLY API",
    description="AI-powered scam detection — RoBERTa + Rules + URL + OCR",
    version="2.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


# ────────────────────────────────────────────────────
# CORS
# ────────────────────────────────────────────────────
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ────────────────────────────────────────────────────
# Routers
# ────────────────────────────────────────────────────
app.include_router(scan_router)
app.include_router(history_router)


# ────────────────────────────────────────────────────
# Exception Handlers
# ────────────────────────────────────────────────────
register_handlers(app)


# ────────────────────────────────────────────────────
# Root Endpoint
# ────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "SCANLY API v2.0",
        "version": "2.0.0",
        "docs": "/docs",
    }


# ────────────────────────────────────────────────────
# Health Endpoint
# ────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    ml = get_model_status()
    ocr = get_ocr_status()
    uptime = get_uptime()

    return {
        "status": "ok",
        "version": "2.0.0",

        # ML Model
        "model_loaded": ml["model_loaded"],
        "model_version": ml["model_version"],
        "device": ml["device"],

        # OCR
        "ocr_loaded": ocr["ocr_loaded"],
        "ocr_languages": ocr["ocr_languages"],

        # Server Uptime
        "uptime": uptime["uptime_human"],
        "uptime_seconds": uptime["uptime_seconds"],
        "started_at": uptime["started_at"],
    }