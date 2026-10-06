from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.forecasting_agent import (
    evaluate,
    estimate,
    generate,
    analyze,
    ForecastingAgent,
)


actual = [100, 110, 120]
predicted = [98, 112, 119]

evaluation = evaluate(actual, predicted)

assert abs(evaluation["mae"] - 5 / 3) < 1e-9
assert evaluation["count"] == 3
assert len(evaluation["errors"]) == 3

confidence = estimate(evaluation["errors"])

assert 0.0 <= confidence["confidence"] <= 1.0
assert confidence["uncertainty"] > 0

scenarios = generate(
    baseline=[100, 110, 120],
    growth_rates=[0.0, 0.10, -0.10],
)

assert all(abs(a - b) < 1e-9 for a, b in zip(scenarios["scenarios"]["BASE"], [100.0, 110.0, 120.0]))
assert all(abs(a - b) < 1e-9 for a, b in zip(scenarios["scenarios"]["UPSIDE"], [110.0, 121.0, 132.0]))
assert all(abs(a - b) < 1e-9 for a, b in zip(scenarios["scenarios"]["DOWNSIDE"], [90.0, 99.0, 108.0]))

risk_opportunity = analyze(
    confidence=0.8,
    growth_rate=0.20,
    uncertainty=0.10,
)

assert 0.0 <= risk_opportunity["risk_score"] <= 1.0
assert 0.0 <= risk_opportunity["opportunity_score"] <= 1.0

agent = ForecastingAgent()

result = agent.analyze(
    actual=actual,
    predicted=predicted,
    baseline=[100, 110, 120],
)

assert result["agent_id"] == "advanced_forecasting_agent"
assert "evaluation" in result
assert "confidence" in result
assert "scenarios" in result
assert "risk_opportunity" in result

print("136 Forecast Accuracy Evaluation : PASS")
print("137 Forecast Confidence           : PASS")
print("138 Scenario Forecasting          : PASS")
print("139 Forecast Risk / Opportunity   : PASS")
print("140 Forecast Intelligence Agent   : PASS")
print("MILESTONE 136-140 : PASS")
