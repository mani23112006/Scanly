"""
SCANLY — Structured Logging
Replaces all print() statements with proper logging.
Usage: from core.logging import get_logger
       logger = get_logger(__name__)
       logger.info("Scan started")
       logger.warning("Low confidence")
       logger.error("DB failed")
"""

import logging
import sys
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for any module.
    All loggers write to stdout with timestamp + level + module.

    Args:
        name: usually __name__ from the calling module

    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

      # Console handler — writes to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Format: 2024-01-15 18:30:00 [INFO] ml.roberta.predict: Model ready
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Don't propagate to root logger (avoids duplicate messages)
    logger.propagate = False

    return logger


# ── App-level logger ────────────────────────────────
# Import this directly for quick one-off logs
app_logger = get_logger("scanly")