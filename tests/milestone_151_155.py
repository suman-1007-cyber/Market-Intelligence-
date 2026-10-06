from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.geospatial_agent import (
    prepare,
    normalize,
    normalize_region,
    analyze,
    detect,
    analyze_opportunity,
)


records = [
    {"region": "usa", "sales": 100},
    {"region": "United States", "sales": 200},
    {"region": "uk", "sales": 80},
    {"region": "United Kingdom", "sales": 120},
]

prepared = prepare(records)

assert prepared["count"] == 4

normalized = normalize(prepared["records"])

assert normalize_region("usa") == "United States"
assert normalize_region("uk") == "United Kingdom"

regional = analyze(normalized, "sales")

assert regional["United States"]["total"] == 300.0
assert regional["United Kingdom"]["total"] == 200.0
assert regional["United States"]["count"] == 2

trend_up = detect([100, 110, 120])

assert trend_up["direction"] == "UP"
assert trend_up["change"] == 20.0
assert abs(trend_up["change_rate"] - 0.20) < 1e-9

trend_down = detect([120, 110, 100])

assert trend_down["direction"] == "DOWN"

opportunity = analyze_opportunity(
    growth_rate=0.80,
    market_value=500.0,
    minimum_market_value=100.0,
)

assert abs(opportunity["opportunity_score"] - 0.86) < 1e-9
assert opportunity["opportunity_level"] == "HIGH"

print("151 Geographic Data Preparation : PASS")
print("152 Geographic Normalization     : PASS")
print("153 Regional Analysis            : PASS")
print("154 Geographic Trend Detection   : PASS")
print("155 Geographic Opportunity       : PASS")
print("MILESTONE 151-155 : PASS")
