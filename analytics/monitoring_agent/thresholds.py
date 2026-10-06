from __future__ import annotations

from typing import Any


def check(
    value: float,
    minimum: float | None = None,
    maximum: float | None = None,
) -> dict[str, Any]:
    value = float(value)

    below = minimum is not None and value < float(minimum)
    above = maximum is not None and value > float(maximum)

    return {
        "value": value,
        "minimum": minimum,
        "maximum": maximum,
        "breached": below or above,
        "status": "BREACH" if below or above else "NORMAL",
    }
