"""
SCANLY API v2.0 — Main Entry Point
Handles: app creation, middleware, routers, exception handlers, startup.
All business logic lives in api/routes/ and services/.
"""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.routes.scan    import router as scan_router
from api.routes.history import router as history_router
from ml.roberta.predict import _load_model, get_model_status
from ocr.extract        import get_ocr_status
from core.exceptions    import register_handlers
from core.logging       import get_logger
from core.timer         import start_timer, get_uptime

logger  = get_logger("scanly.main")
limiter = Limiter(key_func=get_remote_address)


# ── Startup / Shutdown ───────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SCANLY API v2.0 starting up...")
    start_timer()
    logger.info("Pre-loading RoBERTa model...")
    _load_model()
    logger.info("Server ready to accept requests.")
    yield
    logger.info("SCANLY API shutting down.")


# ── App ──────────────────────────────────────────────
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
    "http://localhost:5173,http://localhost:5174,http://localhost:5175"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routers ──────────────────────────────────────────
# prefix is set inside each router — do NOT add prefix here
app.include_router(scan_router)     # /scan/text, /scan/url, /scan/image
app.include_router(history_router)  # /history GET, /history DELETE


# ── Global exception handlers ────────────────────────
register_handlers(app)


# ── Health + Root ────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "SCANLY API v2.0 — RoBERTa + OCR powered",
        "version": "2.0.0",
        "docs":    "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    ml     = get_model_status()
    ocr    = get_ocr_status()
    uptime = get_uptime()
    return {
        "status":         "ok",
        "version":        "2.0.0",
        # ML model
        "model_loaded":   ml["model_loaded"],
        "model_version":  ml["model_version"],
        "device":         ml["device"],
        # OCR
        "ocr_loaded":     ocr["ocr_loaded"],
        "ocr_languages":  ocr["ocr_languages"],
        # Uptime
        "uptime":         uptime["uptime_human"],
        "uptime_seconds": uptime["uptime_seconds"],
        "started_at":     uptime["started_at"],
    }