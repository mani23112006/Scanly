# This file is a centralized error handling system for your FastAPI backend.

# exceptions.py centralizes error handling in the backend. It defines custom exceptions and global exception handlers so every API returns a consistent JSON error response instead of crashing or returning different formats. It also logs errors, making debugging and monitoring much easier.

"""
SCANLY — Custom Exceptions + Global Error Handlers+handling RateLimitExceeded

Ensures all API errors return consistent JSON format.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from core.logging import get_logger

logger = get_logger(__name__)


# --------------------------------------------------
# Base Exception
# --------------------------------------------------

class SCANLYException(Exception):
    """
    Base exception for all SCANLY errors.
    """

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# --------------------------------------------------
# Custom Exceptions
# --------------------------------------------------

class ModelNotLoadedError(SCANLYException):
    """
    Raised when ML model is not loaded.
    """

    def __init__(self):
        super().__init__(
            "ML model not loaded. Server may still be starting up. "
            "Please retry in a few seconds.",
            status_code=503,
        )


class OCRFailedError(SCANLYException):
    """
    Raised when OCR processing fails.
    """

    def __init__(self, reason: str = ""):
        super().__init__(
            f"Image processing failed. {reason}".strip(),
            status_code=422,
        )


class InvalidImageError(SCANLYException):
    """
    Raised when uploaded image is invalid.
    """

    def __init__(self, reason: str = ""):
        super().__init__(
            f"Invalid image. {reason}".strip(),
            status_code=422,
        )


# --------------------------------------------------
# Error Response Builder
# --------------------------------------------------

def _error_response(
    status_code: int,
    message: str,
    error_type: str = "error",
) -> JSONResponse:

    return JSONResponse(
        status_code=status_code,
        content={
            "status": error_type,
            "error": message,
            "code": status_code,
        },
    )


# --------------------------------------------------
# Register Exception Handlers
# --------------------------------------------------

def register_handlers(app: FastAPI):
    """
    Register all exception handlers.
    """

    @app.exception_handler(SCANLYException)
    async def scanly_exception_handler(
        request: Request,
        exc: SCANLYException,
    ):
        logger.error(
            f"SCANLY error [{exc.status_code}]: {exc.message}"
        )

        return _error_response(
            exc.status_code,
            exc.message,
            "scanly_error",
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        logger.warning(
            f"HTTP {exc.status_code}: {exc.detail}"
        )

        return _error_response(
            exc.status_code,
            str(exc.detail),
            "http_error",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):

        errors = []

        for error in exc.errors():
            field = " → ".join(
                str(loc) for loc in error["loc"]
            )

            msg = error["msg"]

            errors.append(
                f"{field}: {msg}"
            )

        message = " | ".join(errors)

        logger.warning(
            f"Validation error: {message}"
        )

        return _error_response(
            422,
            message,
            "validation_error",
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(
        request: Request,
        exc: RateLimitExceeded,
    ):

        logger.warning(
            f"Rate limit exceeded: {request.url.path}"
        )

        return _error_response(
            429,
            "Too many requests. Please wait a minute and try again.",
            "rate_limit_error",
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):

        logger.error(
            f"Unhandled exception: {type(exc).__name__}: {exc}"
        )

        return _error_response(
            500,
            "An unexpected error occurred. Please try again.",
            "server_error",
        )