"""Deterministic customer risk detection."""

from typing import Any


def analyze(
    behavior: dict[str, Any],
    churn_rate: float = 0.0,
) -> dict[str, Any]:
    revenue_change = float(
        behavior.get("revenue_change", 0.0)
    )

    decline_risk = max(
        0.0,
        min(1.0, -revenue_change),
    )

    churn_risk = max(
        0.0,
        min(1.0, float(churn_rate)),
    )

    risk_score = (
        0.60 * decline_risk
        + 0.40 * churn_risk
    )

    if risk_score >= 0.70:
        level = "HIGH"
    elif risk_score >= 0.40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": round(risk_score, 6),
        "risk_level": level,
        "decline_risk": round(
            decline_risk,
            6,
        ),
        "churn_risk": round(
            churn_risk,
            6,
        ),
    }
