from __future__ import annotations

from typing import Any


def aggregate(
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(events, list):
        raise TypeError("events must be a list")

    errors = sum(
        1
        for event in events
        if isinstance(event, dict)
        and event.get("event_type") == "error"
    )

    return {
        "event_count": len(events),
        "error_count": errors,
    }
