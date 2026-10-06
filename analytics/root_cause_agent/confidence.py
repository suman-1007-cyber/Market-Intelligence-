from __future__ import annotations

from typing import Any


def estimate(
    validated_count: int,
    total_driver_count: int,
    strongest_correlation: float,
) -> dict[str, Any]:
    if total_driver_count <= 0:
        return {
            "confidence": 0.0,
            "basis": "NO_DRIVERS",
        }

    coverage = validated_count / total_driver_count
    strength = max(0.0, min(1.0, abs(float(strongest_correlation))))

    confidence = (
        0.40 * min(1.0, coverage)
        + 0.60 * strength
    )

    return {
        "confidence": max(0.0, min(1.0, confidence)),
        "basis": "CORRELATION_AND_VALIDATION",
    }
