"""Milestones 126-130: Pricing Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.pricing_agent.agent import (
    PricingIntelligenceAgent,
)
from analytics.pricing_agent.discounts import (
    analyze as analyze_discount,
)
from analytics.pricing_agent.elasticity import (
    analyze as analyze_elasticity,
)
from analytics.pricing_agent.optimization import (
    optimize,
)
from analytics.pricing_agent.analysis import (
    analyze as analyze_price,
)
from analytics.pricing_agent.competitive import (
    analyze as analyze_competitive,
)
from analytics.pricing_agent.risk import (
    analyze as analyze_risk,
)
from analytics.pricing_agent.opportunity import (
    analyze as analyze_opportunity,
)


# 126 Discount & Promotion Analysis
discount = analyze_discount(
    list_price=100,
    selling_price=80,
    units=10,
)

assert discount["discount_value"] == 20.0
assert discount["discount_rate"] == 0.20
assert discount["revenue"] == 800.0
assert discount["promotion_status"] == "DISCOUNTED"


# 127 Price Optimization Engine
optimization = optimize(
    current_price=100,
    cost=60,
    candidate_prices=[90, 100, 110],
    expected_units=[120, 100, 85],
)

assert optimization["recommended_price"] == 110.0
assert optimization["recommended_profit"] == 4250.0


# Supporting analysis
price = analyze_price(
    price=100,
    cost=60,
    units=100,
)

competitive = analyze_competitive(
    own_price=100,
    competitor_prices=[100, 105, 95],
)

elasticity = analyze_elasticity(
    old_price=100,
    new_price=110,
    old_quantity=100,
    new_quantity=80,
)


# 128 Pricing Risk Detection
risk = analyze_risk(
    price,
    competitive,
    discount,
)

assert risk["risk_level"] == "LOW"
assert risk["requires_review"] is False


# 129 Pricing Opportunity Analysis
opportunity = analyze_opportunity(
    optimization,
    competitive,
    elasticity,
)

assert opportunity["opportunity_level"] == "LOW"
assert opportunity["opportunity_score"] > 0


# 130 Pricing Intelligence Agent
agent = PricingIntelligenceAgent()

result = agent.analyze(
    current_price=100,
    cost=60,
    units=100,
    competitor_prices=[100, 105, 95],
    old_price=100,
    new_price=110,
    old_quantity=100,
    new_quantity=80,
    list_price=120,
    candidate_prices=[90, 100, 110],
    expected_units=[120, 100, 85],
)

assert result["agent_id"] == "pricing-intelligence-agent"
assert result["optimization"]["recommended_price"] == 110.0
assert result["risk"]["risk_level"] == "LOW"
assert result["opportunity"]["opportunity_level"] == "LOW"


print("126 Discount & Promotion Analysis   : PASS")
print("127 Price Optimization Engine       : PASS")
print("128 Pricing Risk Detection          : PASS")
print("129 Pricing Opportunity Analysis    : PASS")
print("130 Pricing Intelligence Agent      : PASS")
print("==============================================")
print("MILESTONE 126-130 : PASS")
print("==============================================")
