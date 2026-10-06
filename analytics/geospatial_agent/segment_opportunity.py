from __future__ import annotations

from typing import Any


def analyze(
    profile: dict[str, Any],
    growth_rate: float = 0.0,
    risk_score: float = 0.0,
) -> dict[str, Any]:
    count = float(profile.get("count", 0))
    average_value = float(profile.get("average_value", 0.0))

    growth = max(0.0, min(1.0, float(growth_rate)))
    risk = max(0.0, min(1.0, float(risk_score)))

    value_score = 1.0 if average_value > 0 else 0.0
    scale_score = 1.0 if count > 0 else 0.0

    opportunity_score = (
        0.40 * value_score
        + 0.30 * scale_score
        + 0.30 * growth
    )

    opportunity_score = max(
        0.0,
        min(1.0, opportunity_score),
    )

    adjusted_score = opportunity_score * (1.0 - 0.50 * risk)

    return {
        "opportunity_score": opportunity_score,
        "risk_adjusted_score": adjusted_score,
        "risk_score": risk,
    }
