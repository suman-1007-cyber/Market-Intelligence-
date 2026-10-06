from __future__ import annotations

from typing import Any


def evaluate(
    available: bool,
    error_rate: float = 0.0,
    latency_seconds: float = 0.0,
) -> dict[str, Any]:
    error_rate = max(0.0, min(1.0, float(error_rate)))
    latency_seconds = max(0.0, float(latency_seconds))

    healthy = bool(available) and error_rate < 0.50

    return {
        "available": bool(available),
        "error_rate": error_rate,
        "latency_seconds": latency_seconds,
        "healthy": healthy,
    }
