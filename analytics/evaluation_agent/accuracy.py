from __future__ import annotations

from typing import Any


def calculate(scores: list[float]) -> dict[str, Any]:
    if not scores:
        return {
            "count": 0,
            "accuracy": 0.0,
        }

    numeric = [float(value) for value in scores]

    return {
        "count": len(numeric),
        "accuracy": sum(numeric) / len(numeric),
    }
