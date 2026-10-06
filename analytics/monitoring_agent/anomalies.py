from __future__ import annotations

from typing import Any


def detect(values: list[float], threshold: float = 2.0) -> dict[str, Any]:
    if not values:
        return {"anomalies": [], "count": 0}

    numeric = [float(value) for value in values]
    mean = sum(numeric) / len(numeric)

    variance = sum((value - mean) ** 2 for value in numeric) / len(numeric)
    std = variance ** 0.5

    if std == 0:
        indexes = []
    else:
        indexes = [
            index
            for index, value in enumerate(numeric)
            if abs(value - mean) / std > float(threshold)
        ]

    return {
        "anomalies": indexes,
        "count": len(indexes),
        "mean": mean,
        "std": std,
    }
