"""Deterministic financial risk detection."""

from typing import Any


def analyze(
    profitability: dict[str, Any],
    cashflow: dict[str, Any],
    ratios: dict[str, Any],
) -> dict[str, Any]:
    margin = float(profitability.get("operating_margin", 0.0))
    net_cash = float(cashflow.get("net_cash_flow", 0.0))
    debt_to_equity = ratios.get("debt_to_equity")

    margin_risk = max(0.0, min(1.0, -margin))
    cash_risk = 1.0 if net_cash < 0 else 0.0

    if debt_to_equity is None:
        debt_risk = 0.0
    else:
        debt_risk = max(
            0.0,
            min(1.0, float(debt_to_equity) / 2.0),
        )

    risk_score = (
        0.35 * margin_risk
        + 0.35 * cash_risk
        + 0.30 * debt_risk
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
