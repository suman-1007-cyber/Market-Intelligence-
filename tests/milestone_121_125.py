"""Milestones 121-125: Pricing Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.pricing_agent.analysis import (
    analyze as analyze_price,
)
from analytics.pricing_agent.competitive import (
    analyze as analyze_competitive,
)
from analytics.pricing_agent.data import (
    normalize,
    normalize_many,
)
from analytics.pricing_agent.elasticity import (
    analyze as analyze_elasticity,
)
from analytics.pricing_agent.segmentation import (
    segment,
)


# 121 Pricing Data Engine
record = normalize(
    {
        "product": "Alpha",
        "price": "100",
        "cost": "60",
        "units": "10",
    }
)

assert record["price"] == 100.0
assert record["cost"] == 60.0
assert record["units"] == 10.0

records = normalize_many([record])
assert len(records) == 1


# 122 Price Analysis Engine
price = analyze_price(
    price=100,
    cost=60,
    units=10,
)

assert price["margin_value"] == 40.0
assert price["margin_rate"] == 0.4
assert price["revenue"] == 1000.0


# 123 Price Elasticity Analysis
elasticity = analyze_elasticity(
    old_price=100,
    new_price=110,
    old_quantity=100,
    new_quantity=80,
)

assert abs(
    elasticity["elasticity"] - (-2.0)
) < 1e-9

assert elasticity["classification"] == "ELASTIC"


# 124 Competitive Pricing Intelligence
competitive = analyze_competitive(
    own_price=110,
    competitor_prices=[100, 105, 95],
)

assert competitive["competitor_average"] == 100.0
assert competitive["price_gap"] == 10.0
assert competitive["position"] == "PREMIUM"


# 125 Price Segmentation
segmented = segment(
    [
        {"product": "A", "price": 50},
        {"product": "B", "price": 100},
        {"product": "C", "price": 150},
        {"product": "D", "price": 200},
        {"product": "E", "price": 250},
        {"product": "F", "price": 300},
    ]
)

assert segmented["count"] == 6
assert len(segmented["low"]) > 0
assert len(segmented["medium"]) > 0
assert len(segmented["high"]) > 0


print("121 Pricing Data Engine              : PASS")
print("122 Price Analysis Engine            : PASS")
print("123 Price Elasticity Analysis        : PASS")
print("124 Competitive Pricing Intelligence : PASS")
print("125 Price Segmentation                : PASS")
print("==============================================")
print("MILESTONE 121-125 : PASS")
print("==============================================")
