from __future__ import annotations

from typing import Any


def compare(
    previous: float,
    current: float,
) -> dict[str, Any]:
    previous = float(previous)
    current = float(current)

    change = current - previous

    if change > 0:
        direction = "IMPROVED"
    elif change < 0:
        direction = "REGRESSED"
    else:
        direction = "UNCHANGED"

    return {
        "previous": previous,
        "current": current,
        "change": change,
        "direction": direction,
    }
