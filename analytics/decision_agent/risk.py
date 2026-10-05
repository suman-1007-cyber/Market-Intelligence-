"""Deterministic decision risk analysis."""

from typing import Any


def analyze(
    ranked: list[dict[str, Any]],
    risk_factors: dict[str, float] | None = None,
) -> dict[str, Any]:
    factors = risk_factors or {}

    normalized = {
        str(name): max(0.0, min(1.0, float(value)))
        for name, value in factors.items()
    }

    if normalized:
        risk_score = sum(normalized.values()) / len(normalized)
    else:
        risk_score = 0.0

    if risk_score >= 0.70:
        level = "HIGH"
    elif risk_score >= 0.40:
        level = "MEDIUM"
    else:
        level = "LOW"

    margin = None

    if len(ranked) >= 2:
        margin = (
            float(ranked[0]["score"])
            - float(ranked[1]["score"])
        )

    return {
        "risk_score": round(risk_score, 6),
        "risk_level": level,
        "factors": normalized,
        "decision_margin": margin,
        "requires_review": level == "HIGH",
    }
