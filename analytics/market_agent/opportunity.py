"""Deterministic market opportunity analysis."""

from typing import Any


def analyze(
    market_growth: float,
    market_size: float,
    competition_level: float = 0.5,
    trend_strength: float = 0.5,
) -> dict[str, Any]:
    size = float(market_size)
    growth = float(market_growth)
    competition = max(0.0, min(1.0, float(competition_level)))
    trend = max(0.0, min(1.0, float(trend_strength)))

    if size < 0:
        raise ValueError("Market size cannot be negative")

    growth_score = max(0.0, min(1.0, growth))

    opportunity_score = (
        0.40 * growth_score
        + 0.30 * trend
        + 0.30 * (1.0 - competition)
    )

    if opportunity_score >= 0.70:
        classification = "HIGH"
    elif opportunity_score >= 0.40:
        classification = "MEDIUM"
    else:
        classification = "LOW"

    return {
        "market_size": size,
        "market_growth": growth,
        "competition_level": competition,
        "trend_strength": trend,
        "opportunity_score": round(opportunity_score, 6),
        "classification": classification,
    }
