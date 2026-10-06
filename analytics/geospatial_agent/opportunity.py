from __future__ import annotations

from typing import Any


def analyze(
    growth_rate: float,
    market_value: float,
    minimum_market_value: float = 0.0,
) -> dict[str, Any]:
    growth_score = max(
        0.0,
        min(1.0, float(growth_rate)),
    )

    size_score = (
        1.0
        if float(market_value) >= float(minimum_market_value)
        else 0.0
    )

    score = (
        0.70 * growth_score
        + 0.30 * size_score
    )

    level = (
        "HIGH" if score >= 0.70
        else "MEDIUM" if score >= 0.40
        else "LOW"
    )

    return {
        "growth_score": growth_score,
        "size_score": size_score,
        "opportunity_score": score,
        "opportunity_level": level,
    }
