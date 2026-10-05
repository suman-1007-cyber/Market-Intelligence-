"""Milestones 96-100: Decision Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.decision_agent.agent import (
    DecisionIntelligenceAgent,
)
from analytics.decision_agent.engine import evaluate
from analytics.decision_agent.intelligence import synthesize
from analytics.decision_agent.recommendation import recommend
from analytics.decision_agent.risk import analyze
from analytics.decision_agent.scoring import (
    rank,
    validate_criteria,
)


criteria = {
    "growth": 0.50,
    "profitability": 0.30,
    "risk": 0.20,
}

alternatives = [
    {
        "name": "Option A",
        "growth": 0.90,
        "profitability": 0.80,
        "risk": 0.40,
    },
    {
        "name": "Option B",
        "growth": 0.70,
        "profitability": 0.70,
        "risk": 0.60,
    },
    {
        "name": "Option C",
        "growth": 0.50,
        "profitability": 0.60,
        "risk": 0.30,
    },
]

criteria_check = validate_criteria(criteria)

assert criteria_check["valid"]
assert criteria_check["criterion_count"] == 3
assert abs(criteria_check["total_weight"] - 1.0) < 1e-9

evaluation = evaluate(
    alternatives,
    criteria,
)

assert len(evaluation) == 3
assert evaluation[0]["name"] == "Option A"
assert abs(evaluation[0]["score"] - 0.77) < 1e-9

ranked = rank(evaluation)

assert ranked[0]["name"] == "Option A"

recommendation = recommend(
    ranked,
    minimum_score=0.60,
)

assert recommendation["recommendation"] == "Option A"
assert recommendation["status"] == "RECOMMENDED"

risk = analyze(
    ranked,
    {
        "execution": 0.20,
        "market": 0.30,
    },
)

assert risk["risk_level"] == "LOW"
assert abs(risk["risk_score"] - 0.25) < 1e-9
assert risk["decision_margin"] > 0

summary = synthesize(
    ranked,
    recommendation,
    risk,
)

assert summary["decision"] == "Option A"
assert summary["decision_status"] == "RECOMMENDED"
assert summary["findings"]

agent = DecisionIntelligenceAgent()

result = agent.decide(
    alternatives,
    criteria,
    risk_factors={
        "execution": 0.20,
        "market": 0.30,
    },
)

assert result["agent_id"] == "decision-intelligence-agent"
assert result["recommendation"]["recommendation"] == "Option A"
assert result["recommendation"]["status"] == "RECOMMENDED"
assert result["risk"]["risk_level"] == "LOW"
assert result["intelligence"]["decision"] == "Option A"

print("96 Decision Engine                : PASS")
print("97 Decision Criteria & Scoring    : PASS")
print("98 Recommendation Engine          : PASS")
print("99 Decision Risk Analysis         : PASS")
print("100 Decision Intelligence Agent  : PASS")
print("==============================================")
print("MILESTONE 96-100 : PASS")
print("==============================================")
