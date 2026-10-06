"""Milestones 111-115: Financial Intelligence foundation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.financial_agent.cashflow import (
    analyze as analyze_cashflow,
)
from analytics.financial_agent.data import normalize
from analytics.financial_agent.profitability import (
    analyze as analyze_profitability,
)
from analytics.financial_agent.ratios import (
    analyze as analyze_ratios,
)
from analytics.financial_agent.trends import (
    analyze as analyze_trends,
)


record = normalize(
    {
        "revenue": "1000",
        "cost": "400",
        "operating_expense": "200",
    }
)

assert record["revenue"] == 1000.0
assert record["cost"] == 400.0

profitability = analyze_profitability(
    revenue=1000,
    cost=400,
    operating_expense=200,
)

assert profitability["gross_profit"] == 600.0
assert profitability["operating_profit"] == 400.0
assert abs(
    profitability["gross_margin"] - 0.60
) < 1e-9
assert abs(
    profitability["operating_margin"] - 0.40
) < 1e-9

cashflow = analyze_cashflow(
    cash_inflow=1200,
    cash_outflow=900,
)

assert cashflow["net_cash_flow"] == 300.0
assert cashflow["positive"]
assert abs(
    cashflow["coverage_ratio"] - (1200 / 900)
) < 1e-6

ratios = analyze_ratios(
    revenue=1000,
    profit=200,
    assets=2000,
    liabilities=500,
    equity=1500,
)

assert abs(
    ratios["profit_margin"] - 0.20
) < 1e-9
assert abs(
    ratios["return_on_assets"] - 0.10
) < 1e-9
assert abs(
    ratios["debt_to_equity"] - (1 / 3)
) < 1e-6

trends = analyze_trends(
    [100, 120, 140, 160]
)

assert trends["direction"] == "UP"
assert trends["change"] == 60.0
assert abs(
    trends["change_rate"] - 0.60
) < 1e-9
assert trends["peak"] == 160.0
assert trends["trough"] == 100.0

print("111 Financial Data Engine          : PASS")
print("112 Revenue & Profitability        : PASS")
print("113 Cash Flow Analysis              : PASS")
print("114 Financial Ratio Engine          : PASS")
print("115 Financial Trend Intelligence   : PASS")
print("==============================================")
print("MILESTONE 111-115 : PASS")
print("==============================================")
