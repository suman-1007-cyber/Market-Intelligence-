"""Deterministic financial health analysis."""

from typing import Any


def analyze(
    profitability: dict[str, Any],
    cashflow: dict[str, Any],
    ratios: dict[str, Any],
) -> dict[str, Any]:
    margin = float(profitability.get("operating_margin", 0.0))
    net_cash = float(cashflow.get("net_cash_flow", 0.0))
    debt_to_equity = ratios.get("debt_to_equity")

    score = 0.0

    if margin > 0:
        score += 0.4
    if net_cash >= 0:
        score += 0.3
    if debt_to_equity is not None and debt_to_equity <= 1.0:
        score += 0.3

    score = round(score, 6)

    if score >= 0.7:
        status = "HEALTHY"
    elif score >= 0.4:
        status = "MODERATE"
    else:
        status = "WEAK"

    return {
        "health_score": score,
        "status": status,
    }
