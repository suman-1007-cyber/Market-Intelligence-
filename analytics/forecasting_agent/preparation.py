from __future__ import annotations

from typing import Any, Iterable


def prepare(values: Iterable[float]) -> dict[str, Any]:
    series = [float(value) for value in values]

    if not series:
        return {
            "values": [],
            "count": 0,
            "valid": False,
            "reason": "EMPTY_SERIES",
        }

    if any(not (value == value) for value in series):
        raise ValueError("Forecast series contains NaN")

    return {
        "values": series,
        "count": len(series),
        "valid": True,
        "first": series[0],
        "last": series[-1],
        "minimum": min(series),
        "maximum": max(series),
    }
