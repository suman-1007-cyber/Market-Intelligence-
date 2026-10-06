"""Deterministic financial opportunity analysis."""

from typing import Any


def analyze(
    profitability: dict[str, Any],
    trends: dict[str, Any],
    health: dict[str, Any],
) -> dict[str, Any]:
    margin = max(
        0.0,
        min(1.0, float(
            profitability.get("operating_margin", 0.0)
        )),
    )

    trend_rate = max(
        0.0,
        min(1.0, float(
            trends.get("change_rate", 0.0)
        )),
    )

    health_score = max(
        0.0,
        min(1.0, float(
            health.get("health_score", 0.0)
        )),
    )

    opportunity_score = (
        0.35 * margin
        + 0.35 * trend_rate
        + 0.30 * health_score
    )

    opportunity_score = round(opportunity_score, 6)

    if opportunity_score >= 0.70:
        level = "HIGH"
    elif opportunity_score >= 0.40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "opportunity_score": opportunity_score,
        "opportunity_level": level,
    }
