from __future__ import annotations

from typing import Any, Iterable


def estimate(errors: Iterable[float]) -> dict[str, Any]:
    values = [abs(float(error)) for error in errors]

    if not values:
        return {
            "confidence": 0.0,
            "mean_absolute_error": 0.0,
            "uncertainty": 0.0,
        }

    uncertainty = sum(values) / len(values)
    confidence = 1.0 / (1.0 + uncertainty)

    return {
        "confidence": max(0.0, min(1.0, confidence)),
        "mean_absolute_error": uncertainty,
        "uncertainty": uncertainty,
    }
