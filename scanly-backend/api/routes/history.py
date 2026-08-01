"""
===========================================================
SCANLY — History Routes
===========================================================

Purpose
-------
This file contains all scan history related API endpoints.

Endpoints
---------
GET /history
    • Returns the most recent scan history.
    • Includes both text scans and image scans.
    • Results are sorted from newest to oldest.

DELETE /history
    • Deletes all scan history from MongoDB.

Why this file?
--------------
Instead of placing history endpoints inside main.py,
they are organized into a dedicated router.

Benefits
--------
✓ Cleaner project structure
✓ Modular routing
✓ Easier maintenance
✓ Better scalability
✓ Production-ready organization
"""

from fastapi import APIRouter, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from models import HistoryResponse, HistoryItem
from db import scans_collection
from core.logging import get_logger


# --------------------------------------------------------
# Router Configuration
# --------------------------------------------------------

router = APIRouter(
    prefix="/history",
    tags=["History"],
)

limiter = Limiter(
    key_func=get_remote_address,
)

logger = get_logger(__name__)


# --------------------------------------------------------
# GET /history
# --------------------------------------------------------

@router.get(
    "",
    response_model=HistoryResponse,
)
async def get_history(limit: int = 20):
    """
    Fetch the latest scan history.

    Returns the newest scan records first.

    Supports:
    • Text scans
    • Image scans
    • URL scans (if stored)
    """

    logger.info(f"History request received (limit={limit})")

    try:

        cursor = (
            scans_collection.find(
                {},
                {
                    "_id": 1,
                    "input_text": 1,
                    "final_score": 1,
                    "category": 1,
                    "ml_score": 1,
                    "rule_score": 1,
                    "url_score": 1,
                    "matched_keywords": 1,
                    "flagged_urls": 1,
                    "explanation": 1,
                    "timestamp": 1,
                    "scan_type": 1,
                },
            )
            .sort("timestamp", -1)
            .limit(limit)
        )

        scans = []

        for doc in cursor:

            scans.append(
                HistoryItem(
                    id=str(doc["_id"]),
                    input_text=doc.get("input_text", ""),
                    final_score=doc.get("final_score", 0),
                    category=doc.get("category", "Unknown"),
                    ml_score=doc.get("ml_score", 0),
                    rule_score=doc.get("rule_score", 0),
                    url_score=doc.get("url_score", 0),
                    matched_keywords=doc.get(
                        "matched_keywords",
                        [],
                    ),
                    flagged_urls=doc.get(
                        "flagged_urls",
                        [],
                    ),
                    explanation=doc.get(
                        "explanation",
                        "",
                    ),
                    timestamp=doc.get(
                        "timestamp",
                        "",
                    ),
                )
            )

        logger.info(
            f"Returned {len(scans)} history records"
        )

        return HistoryResponse(
            status="success",
            count=len(scans),
            scans=scans,
        )

    except Exception as e:

        logger.error(
            f"History fetch failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# --------------------------------------------------------
# DELETE /history
# --------------------------------------------------------

@router.delete("")
async def clear_history():
    """
    Delete all scan history from MongoDB.
    """

    logger.info("Clearing scan history")

    try:

        result = scans_collection.delete_many({})

        logger.info(
            f"Deleted {result.deleted_count} scan records"
        )

        return {
            "status": "success",
            "deleted": result.deleted_count,
            "message": (
                f"Deleted {result.deleted_count} "
                "scan records"
            ),
        }

    except Exception as e:

        logger.error(
            f"History clear failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )