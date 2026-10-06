"""Deterministic customer opportunity detection."""

from typing import Any


def analyze(
    behavior: dict[str, Any],
    segment: str = "MEDIUM_VALUE",
) -> dict[str, Any]:
    revenue_change = float(
        behavior.get("revenue_change", 0.0)
    )

    growth_score = max(
        0.0,
        min(1.0, revenue_change),
    )

    segment_score = {
        "HIGH_VALUE": 1.0,
        "MEDIUM_VALUE": 0.6,
        "LOW_VALUE": 0.3,
    }.get(segment, 0.5)

    opportunity_score = (
        0.60 * growth_score
        + 0.40 * segment_score
    )

    if opportunity_score >= 0.70:
        level = "HIGH"
    elif opportunity_score >= 0.40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "opportunity_score": round(
            opportunity_score,
            6,
        ),
        "opportunity_level": level,
        "segment": segment,
    }
