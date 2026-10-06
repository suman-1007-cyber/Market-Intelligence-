"""Revenue and profitability analysis."""

from typing import Any


def analyze(
    revenue: float,
    cost: float = 0.0,
    operating_expense: float = 0.0,
) -> dict[str, Any]:
    revenue_value = float(revenue)
    cost_value = float(cost)
    expense_value = float(operating_expense)

    gross_profit = revenue_value - cost_value
    operating_profit = gross_profit - expense_value

    gross_margin = (
        gross_profit / revenue_value
        if revenue_value
        else 0.0
    )

    operating_margin = (
        operating_profit / revenue_value
        if revenue_value
        else 0.0
    )

    return {
        "revenue": revenue_value,
        "cost": cost_value,
        "operating_expense": expense_value,
        "gross_profit": round(gross_profit, 6),
        "operating_profit": round(operating_profit, 6),
        "gross_margin": round(gross_margin, 6),
        "operating_margin": round(operating_margin, 6),
    }
