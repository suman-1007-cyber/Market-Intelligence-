"""Milestones 106-110: Customer Intelligence Agent."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.customer_agent.agent import (
    CustomerIntelligenceAgent,
)
from analytics.customer_agent.behavior import (
    analyze as analyze_behavior,
)
from analytics.customer_agent.ltv import calculate
from analytics.customer_agent.opportunity import (
    analyze as analyze_opportunity,
)
from analytics.customer_agent.risk import (
    analyze as analyze_risk,
)


ltv = calculate(
    revenue=1000,
    gross_margin=0.70,
    retention_rate=0.50,
    periods=4,
)

assert abs(ltv["ltv"] - 1312.5) < 1e-6

behavior = analyze_behavior(
    {
        "customer": "Alpha",
        "revenue": 1200,
        "orders": 3,
    },
    {
        "customer": "Alpha",
        "revenue": 1000,
        "orders": 2,
    },
)

assert behavior["behavior"] == "GROWING"
assert abs(behavior["revenue_change"] - 0.20) < 1e-6

opportunity = analyze_opportunity(
    behavior,
    segment="HIGH_VALUE",
)

assert opportunity["opportunity_level"] == "MEDIUM"
assert abs(
    opportunity["opportunity_score"] - 0.52
) < 1e-6

risk = analyze_risk(
    {
        "customer": "Beta",
        "revenue_change": -0.50,
    },
    churn_rate=0.50,
)

assert risk["risk_level"] == "MEDIUM"
assert abs(risk["risk_score"] - 0.50) < 1e-6

agent = CustomerIntelligenceAgent()

result = agent.analyze(
    {
        "customer": "Alpha",
        "revenue": 1200,
        "orders": 3,
        "units": 12,
    },
    {
        "customer": "Alpha",
        "revenue": 1000,
        "orders": 2,
        "units": 10,
    },
    churn_rate=0.10,
    customer_population=[
        {"customer": "Alpha", "revenue": 1200},
        {"customer": "Beta", "revenue": 500},
        {"customer": "Gamma", "revenue": 200},
        {"customer": "Delta", "revenue": 100},
    ],
)

assert result["agent_id"] == "customer-intelligence-agent"
assert result["customer"] == "Alpha"
assert result["segment"] == "HIGH_VALUE"
assert result["behavior"]["behavior"] == "GROWING"
assert result["ltv"]["ltv"] > 0
assert result["opportunity"]["opportunity_level"] == "MEDIUM"
assert result["risk"]["risk_level"] == "LOW"

print("106 Customer Lifetime Value       : PASS")
print("107 Customer Behavior Intelligence: PASS")
print("108 Customer Opportunity          : PASS")
print("109 Customer Risk                 : PASS")
print("110 Customer Intelligence Agent   : PASS")
print("==============================================")
print("MILESTONE 106-110 : PASS")
print("==============================================")
