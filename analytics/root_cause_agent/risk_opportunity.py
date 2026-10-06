from __future__ import annotations

from typing import Any


def analyze(
    confidence: float,
    strongest_correlation: float,
    target_change: float,
) -> dict[str, Any]:
    confidence = max(0.0, min(1.0, float(confidence)))
    strength = max(0.0, min(1.0, abs(float(strongest_correlation))))

    risk_score = max(
        0.0,
        min(
            1.0,
            (1.0 - confidence) * 0.50
            + (1.0 - strength) * 0.50,
        ),
    )

    opportunity_score = max(
        0.0,
        min(
            1.0,
            strength * 0.60
            + confidence * 0.40
            if target_change > 0
            else 0.0,
        ),
    )

    return {
        "risk_score": risk_score,
        "opportunity_score": opportunity_score,
        "risk_level": (
            "HIGH" if risk_score >= 0.70
            else "MEDIUM" if risk_score >= 0.40
            else "LOW"
        ),
        "opportunity_level": (
            "HIGH" if opportunity_score >= 0.70
            else "MEDIUM" if opportunity_score >= 0.40
            else "LOW"
        ),
    }
