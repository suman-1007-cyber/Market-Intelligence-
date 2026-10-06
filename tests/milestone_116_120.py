"""Milestones 116-120: Financial Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.financial_agent.agent import (
    FinancialIntelligenceAgent,
)
from analytics.financial_agent.cashflow import (
    analyze as analyze_cashflow,
)
from analytics.financial_agent.forecast import forecast
from analytics.financial_agent.health import (
    analyze as analyze_health,
)
from analytics.financial_agent.opportunity import (
    analyze as analyze_opportunity,
)
from analytics.financial_agent.profitability import (
    analyze as analyze_profitability,
)
from analytics.financial_agent.ratios import (
    analyze as analyze_ratios,
)
from analytics.financial_agent.risk import (
    analyze as analyze_risk,
)
from analytics.financial_agent.trends import (
    analyze as analyze_trends,
)


profitability = analyze_profitability(
    revenue=1000,
    cost=400,
    operating_expense=200,
)

cashflow = analyze_cashflow(
    cash_inflow=1200,
    cash_outflow=900,
)

ratios = analyze_ratios(
    revenue=1000,
    profit=400,
    assets=2000,
    liabilities=500,
    equity=1500,
)

health = analyze_health(
    profitability,
    cashflow,
    ratios,
)

assert health["status"] == "HEALTHY"
assert health["health_score"] == 1.0

risk = analyze_risk(
    profitability,
    cashflow,
    ratios,
)

assert risk["risk_level"] == "LOW"
assert risk["requires_review"] is False

financial_forecast = forecast(
    [100, 120, 144],
    periods=2,
)

assert abs(
    financial_forecast["growth_rate"] - 0.20
) < 1e-9
assert financial_forecast["forecast"] == [
    172.8,
    207.36,
]

trends = analyze_trends(
    [100, 120, 144]
)

opportunity = analyze_opportunity(
    profitability,
    trends,
    health,
)

assert opportunity["opportunity_level"] == "MEDIUM"
assert abs(
    opportunity["opportunity_score"] - 0.594
) < 1e-9

agent = FinancialIntelligenceAgent()

result = agent.analyze(
    revenue=1000,
    cost=400,
    operating_expense=200,
    cash_inflow=1200,
    cash_outflow=900,
    assets=2000,
    liabilities=500,
    equity=1500,
    trend_values=[100, 120, 144],
    forecast_periods=2,
)

assert result["agent_id"] == "financial-intelligence-agent"
assert result["health"]["status"] == "HEALTHY"
assert result["risk"]["risk_level"] == "LOW"
assert result["forecast"]["forecast"] == [
    172.8,
    207.36,
]

print("116 Financial Health Engine          : PASS")
print("117 Financial Risk Detection         : PASS")
print("118 Financial Forecasting             : PASS")
print("119 Financial Opportunity Analysis   : PASS")
print("120 Financial Intelligence Agent     : PASS")
print("==============================================")
print("MILESTONE 116-120 : PASS")
print("==============================================")
