from __future__ import annotations

from typing import Any


def analyze(
    confidence: float,
    growth_rate: float,
    uncertainty: float,
) -> dict[str, Any]:
    confidence = max(0.0, min(1.0, float(confidence)))
    growth_rate = float(growth_rate)
    uncertainty = max(0.0, float(uncertainty))

    risk_score = max(
        0.0,
        min(
            1.0,
            (1.0 - confidence) * 0.60
            + min(1.0, uncertainty) * 0.40,
        ),
    )

    opportunity_score = max(
        0.0,
        min(
            1.0,
            max(0.0, min(1.0, growth_rate)) * 0.70
            + confidence * 0.30,
        ),
    )

    risk_level = (
        "HIGH" if risk_score >= 0.70
        else "MEDIUM" if risk_score >= 0.40
        else "LOW"
    )

    opportunity_level = (
        "HIGH" if opportunity_score >= 0.70
        else "MEDIUM" if opportunity_score >= 0.40
        else "LOW"
    )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "opportunity_score": opportunity_score,
        "opportunity_level": opportunity_level,
    }
