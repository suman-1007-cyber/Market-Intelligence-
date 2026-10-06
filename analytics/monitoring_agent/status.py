from __future__ import annotations

from typing import Any


def summarize(
    alerts: list[dict[str, Any]],
    fresh: bool,
) -> dict[str, Any]:
    if not fresh:
        status = "STALE"
    elif alerts:
        status = "ALERT"
    else:
        status = "HEALTHY"

    return {
        "status": status,
        "alert_count": len(alerts),
        "fresh": bool(fresh),
    }
