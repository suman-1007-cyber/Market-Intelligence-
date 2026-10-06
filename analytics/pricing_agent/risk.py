"""Deterministic pricing risk detection."""

from typing import Any


def analyze(
    price_analysis: dict[str, Any],
    competitive_analysis: dict[str, Any],
    discount_analysis: dict[str, Any],
) -> dict[str, Any]:
    margin_rate = float(
        price_analysis.get("margin_rate", 0.0)
    )

    gap_rate = competitive_analysis.get("price_gap_rate")
    discount_rate = float(
        discount_analysis.get("discount_rate", 0.0)
    )

    margin_risk = (
        max(0.0, min(1.0, -margin_rate))
        if margin_rate < 0
        else 0.0
    )

    competitive_risk = 0.0
    if gap_rate is not None:
        competitive_risk = max(
            0.0,
            min(1.0, float(gap_rate)),
        )

    discount_risk = max(
        0.0,
        min(1.0, discount_rate),
    )

    risk_score = (
        0.40 * margin_risk
        + 0.35 * competitive_risk
        + 0.25 * discount_risk
    )

    risk_score = round(risk_score, 6)

    if risk_score >= 0.70:
        level = "HIGH"
    elif risk_score >= 0.40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "requires_review": level == "HIGH",
    }
