from __future__ import annotations

from typing import Any


def establish(values: list[float]) -> dict[str, Any]:
    if not values:
        raise ValueError("values must not be empty")

    numeric = [float(value) for value in values]
    return {
        "count": len(numeric),
        "mean": sum(numeric) / len(numeric),
        "minimum": min(numeric),
        "maximum": max(numeric),
        "latest": numeric[-1],
    }
