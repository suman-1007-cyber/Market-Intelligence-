"""Financial Intelligence Agent."""

from typing import Any

from .intelligence import analyze


class FinancialIntelligenceAgent:
    agent_id = "financial-intelligence-agent"

    def analyze(
        self,
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
        result = analyze(
            revenue=revenue,
            cost=cost,
            operating_expense=operating_expense,
            cash_inflow=cash_inflow,
            cash_outflow=cash_outflow,
            assets=assets,
            liabilities=liabilities,
            equity=equity,
            trend_values=trend_values,
            forecast_periods=forecast_periods,
        )

        result["agent_id"] = self.agent_id
        return result
