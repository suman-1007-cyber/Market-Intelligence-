"""Deterministic pricing opportunity analysis."""

from typing import Any


def analyze(
    optimization: dict[str, Any],
    competitive_analysis: dict[str, Any],
    elasticity: dict[str, Any],
) -> dict[str, Any]:
    candidates = optimization.get("candidates", [])

    if not candidates:
        raise ValueError("Optimization candidates are required.")

    current_price = float(
        optimization.get("current_price", 0.0)
    )
    recommended_price = float(
        optimization.get("recommended_price", current_price)
    )

    if current_price == 0:
        optimization_gain = 0.0
    else:
        optimization_gain = (
            recommended_price - current_price
        ) / current_price

    optimization_score = max(
        0.0,
        min(1.0, abs(optimization_gain)),
    )

    gap_rate = competitive_analysis.get("price_gap_rate")
    competitive_score = (
        max(0.0, min(1.0, abs(float(gap_rate))))
        if gap_rate is not None
        else 0.0
    )

    elasticity_value = abs(
        float(elasticity.get("elasticity", 0.0))
    )

    elasticity_score = max(
        0.0,
        min(1.0, elasticity_value / 2.0),
    )

    opportunity_score = (
        0.40 * optimization_score
        + 0.30 * competitive_score
        + 0.30 * elasticity_score
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
        "optimization_gain_rate": round(
            optimization_gain,
            6,
        ),
    }
