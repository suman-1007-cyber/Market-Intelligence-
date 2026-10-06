"""Financial intelligence aggregation."""

from typing import Any

from .cashflow import analyze as analyze_cashflow
from .forecast import forecast
from .health import analyze as analyze_health
from .opportunity import analyze as analyze_opportunity
from .profitability import analyze as analyze_profitability
from .ratios import analyze as analyze_ratios
from .risk import analyze as analyze_risk
from .trends import analyze as analyze_trends


def analyze(
    revenue: float,
    cost: float = 0.0,
    operating_expense: float = 0.0,
    cash_inflow: float = 0.0,
    cash_outflow: float = 0.0,
    assets: float = 0.0,
    liabilities: float = 0.0,
    equity: float = 0.0,
    trend_values: list[float] | None = None,
    forecast_periods: int = 2,
) -> dict[str, Any]:
    profitability = analyze_profitability(
        revenue,
        cost,
        operating_expense,
    )

    cashflow = analyze_cashflow(
        cash_inflow,
        cash_outflow,
    )

    ratios = analyze_ratios(
        revenue,
        profitability["operating_profit"],
        assets,
        liabilities,
        equity,
    )

    health = analyze_health(
        profitability,
        cashflow,
        ratios,
    )

    risk = analyze_risk(
        profitability,
        cashflow,
        ratios,
    )

    values = trend_values or [float(revenue)]
    trends = analyze_trends(values)

    financial_forecast = forecast(
        values,
        forecast_periods,
    )

    opportunity = analyze_opportunity(
        profitability,
        trends,
        health,
    )

    return {
        "revenue": float(revenue),
        "profitability": profitability,
        "cashflow": cashflow,
        "ratios": ratios,
        "health": health,
        "risk": risk,
        "trends": trends,
        "forecast": financial_forecast,
        "opportunity": opportunity,
    }
