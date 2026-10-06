from __future__ import annotations

from typing import Any


def analyze(
    health: dict[str, Any],
    resources: dict[str, Any],
    cost: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": health["status"],
        "error_count": health["error_count"],
        "latency_seconds": health["latency_seconds"],
        "requests": resources["requests"],
        "total_cost": cost["total_cost"],
        "needs_attention": health["status"] != "HEALTHY",
    }
