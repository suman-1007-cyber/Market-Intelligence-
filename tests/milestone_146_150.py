from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.root_cause_agent import (
    analyze_contribution,
    validate,
    estimate,
    analyze_risk_opportunity,
    RootCauseIntelligenceAgent,
)


target = [10, 20, 30, 40, 50]

drivers = {
    "marketing": [1, 2, 3, 4, 5],
    "price": [5, 4, 3, 2, 1],
    "noise": [2, 5, 1, 4, 3],
}

contribution = analyze_contribution(target, drivers)

assert contribution["marketing"]["change"] == 4.0
assert contribution["price"]["change"] == -4.0
assert abs(contribution["marketing"]["contribution"] - 0.1) < 1e-9

ranked = [
    {
        "driver": "marketing",
        "absolute_correlation": 1.0,
        "correlation": 1.0,
        "direction": "POSITIVE",
        "rank": 1,
        "strength": "HIGH",
    },
    {
        "driver": "noise",
        "absolute_correlation": 0.1,
        "correlation": 0.1,
        "direction": "POSITIVE",
        "rank": 2,
        "strength": "LOW",
    },
]

validation = validate(ranked)

assert validation["valid"]
assert validation["validated_count"] == 1

confidence = estimate(
    validated_count=1,
    total_driver_count=2,
    strongest_correlation=1.0,
)

assert abs(confidence["confidence"] - 0.8) < 1e-9

risk = analyze_risk_opportunity(
    confidence=0.8,
    strongest_correlation=1.0,
    target_change=40.0,
)

assert risk["risk_level"] == "LOW"
assert risk["opportunity_level"] == "HIGH"

agent = RootCauseIntelligenceAgent()

result = agent.investigate(
    target,
    drivers,
)

assert result["agent_id"] == "advanced_root_cause_intelligence_agent"
assert result["validation"]["validated_count"] == 2
assert result["confidence"]["confidence"] > 0
assert "contribution" in result
assert "risk_opportunity" in result

print("146 Root Cause Contribution : PASS")
print("147 Root Cause Validation   : PASS")
print("148 Root Cause Confidence   : PASS")
print("149 Root Cause Risk/Opp.    : PASS")
print("150 Root Cause Agent        : PASS")
print("MILESTONE 146-150 : PASS")
