from __future__ import annotations

from typing import Any


def assess(
    error_count: int,
    latency_seconds: float,
    max_latency_seconds: float,
) -> dict[str, Any]:
    error_count = max(0, int(error_count))
    latency_seconds = max(0.0, float(latency_seconds))
    max_latency_seconds = max(0.0, float(max_latency_seconds))

    if error_count > 0:
        status = "DEGRADED"
    elif latency_seconds > max_latency_seconds:
        status = "SLOW"
    else:
        status = "HEALTHY"

    return {
        "status": status,
        "error_count": error_count,
        "latency_seconds": latency_seconds,
    }
