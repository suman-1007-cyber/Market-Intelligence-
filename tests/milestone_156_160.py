from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.geospatial_agent import (
    analyze_risk,
    segment,
    profile,
    analyze_segment_opportunity,
    GeospatialSegmentationAgent,
)


risk = analyze_risk(
    growth_rate=-0.20,
    volatility=0.50,
    concentration=0.20,
)

assert abs(risk["risk_score"] - 0.29) < 1e-9
assert risk["risk_level"] == "LOW"

customers = [
    {"customer": "A", "revenue": 100},
    {"customer": "B", "revenue": 200},
    {"customer": "C", "revenue": 300},
    {"customer": "D", "revenue": 400},
]

segmented = segment(customers)

assert len(segmented) == 4
assert segmented[0]["segment"] == "LOW_VALUE"
assert segmented[-1]["segment"] == "HIGH_VALUE"

profiles = profile(segmented)

assert profiles["LOW_VALUE"]["count"] == 1
assert profiles["HIGH_VALUE"]["count"] == 1

segment_result = analyze_segment_opportunity(
    profiles["HIGH_VALUE"],
    growth_rate=0.50,
    risk_score=0.0,
)

assert abs(segment_result["opportunity_score"] - 0.85) < 1e-9
assert abs(segment_result["risk_adjusted_score"] - 0.85) < 1e-9

agent = GeospatialSegmentationAgent()

result = agent.analyze(
    geographic_records=[
        {"region": "usa", "sales": 100},
        {"region": "United States", "sales": 200},
        {"region": "uk", "sales": 80},
        {"region": "United Kingdom", "sales": 120},
    ],
    customers=customers,
)

assert result["agent_id"] == "geospatial_segmentation_intelligence_agent"
assert "geographic" in result
assert "segmentation" in result
assert result["geographic"]["regional"]["United States"]["total"] == 300.0
assert "HIGH_VALUE" in result["segmentation"]["profiles"]

print("156 Geographic Risk Analysis       : PASS")
print("157 Advanced Customer Segmentation  : PASS")
print("158 Segment Profiling               : PASS")
print("159 Segment Opportunity / Risk      : PASS")
print("160 Geospatial & Segmentation Agent : PASS")
print("MILESTONE 156-160 : PASS")
