from __future__ import annotations

from typing import Any


def analyze(
    growth_rate: float,
    volatility: float,
    concentration: float,
) -> dict[str, Any]:
    growth_risk = max(0.0, min(1.0, -float(growth_rate)))
    volatility_score = max(0.0, min(1.0, float(volatility)))
    concentration_score = max(0.0, min(1.0, float(concentration)))

    score = (
        0.40 * growth_risk
        + 0.30 * volatility_score
        + 0.30 * concentration_score
    )

    level = (
        "HIGH" if score >= 0.70
        else "MEDIUM" if score >= 0.40
        else "LOW"
    )

    return {
        "growth_risk": growth_risk,
        "volatility_score": volatility_score,
        "concentration_score": concentration_score,
        "risk_score": score,
        "risk_level": level,
    }
