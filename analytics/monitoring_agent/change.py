from __future__ import annotations

from typing import Any


def detect(previous: float, current: float) -> dict[str, Any]:
    previous = float(previous)
    current = float(current)
    absolute = current - previous
    rate = absolute / previous if previous != 0 else 0.0

    if absolute > 0:
        direction = "UP"
    elif absolute < 0:
        direction = "DOWN"
    else:
        direction = "FLAT"

    return {
        "previous": previous,
        "current": current,
        "change": absolute,
        "change_rate": rate,
        "direction": direction,
    }
