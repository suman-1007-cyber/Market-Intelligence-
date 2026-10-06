"""Deterministic financial ratio engine."""

from typing import Any


def analyze(
    revenue: float,
    profit: float,
    assets: float = 0.0,
    liabilities: float = 0.0,
    equity: float = 0.0,
) -> dict[str, Any]:
    revenue_value = float(revenue)
    profit_value = float(profit)
    assets_value = float(assets)
    liabilities_value = float(liabilities)
    equity_value = float(equity)

    profit_margin = (
        profit_value / revenue_value
        if revenue_value
        else 0.0
    )

    return_on_assets = (
        profit_value / assets_value
        if assets_value
        else 0.0
    )

    debt_to_equity = (
        liabilities_value / equity_value
        if equity_value
        else None
    )

    return {
        "profit_margin": round(profit_margin, 6),
        "return_on_assets": round(return_on_assets, 6),
        "debt_to_equity": (
            round(debt_to_equity, 6)
            if debt_to_equity is not None
            else None
        ),
    }
