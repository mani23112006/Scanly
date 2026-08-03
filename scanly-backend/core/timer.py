"""
SCANLY — Server Timer
Tracks server startup time to calculate uptime.
Import start_timer() in main.py lifespan,
then call get_uptime() from /health endpoint.
"""

import time
from datetime import datetime, timezone

_start_time: float = None


def start_timer():
    """Call this once at server startup."""
    global _start_time
    _start_time = time.time()


def get_uptime() -> dict:
    """
    Return server uptime info.

    Returns:
        {
            uptime_seconds: int,
            uptime_human:   str  (e.g. "2h 15m 30s"),
            started_at:     str  (ISO timestamp)
        }
    """
    if _start_time is None:
        return {
            "uptime_seconds": 0,
            "uptime_human":   "not started",
            "started_at":     None,
        }

    elapsed   = int(time.time() - _start_time)
    hours     = elapsed // 3600
    minutes   = (elapsed % 3600) // 60
    seconds   = elapsed % 60

    if hours > 0:
        human = f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        human = f"{minutes}m {seconds}s"
    else:
        human = f"{seconds}s"

    started_at = datetime.fromtimestamp(
        _start_time, tz=timezone.utc
    ).isoformat()

    return {
        "uptime_seconds": elapsed,
        "uptime_human":   human,
        "started_at":     started_at,
    }


def time_function(func):
    """
    Decorator: measure how long a function takes.
    Usage:
        @time_function
        def my_function(): ...
    """
    def wrapper(*args, **kwargs):
        t0     = time.time()
        result = func(*args, **kwargs)
        ms     = int((time.time() - t0) * 1000)
        return result, ms
    return wrapper