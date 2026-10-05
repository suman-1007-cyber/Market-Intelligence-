"""Milestones 86-90: Market Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.market_agent.agent import MarketIntelligenceAgent
from analytics.market_agent.intelligence import synthesize
from analytics.market_agent.opportunity import analyze as analyze_opportunity
from analytics.market_agent.sizing import analyze as analyze_sizing
from analytics.market_agent.trends import analyze as analyze_trend


sizing = analyze_sizing(
    150.0,
    previous_size=100.0,
    period="2026",
)

assert sizing["market_size"] == 150.0
assert sizing["growth_absolute"] == 50.0
assert sizing["growth_rate"] == 0.5

trend = analyze_trend([100.0, 110.0, 125.0, 150.0])

assert trend["direction"] == "UP"
assert trend["change_absolute"] == 50.0
assert trend["change_percent"] == 0.5
assert trend["peak"] == 150.0
assert trend["trough"] == 100.0

opportunity = analyze_opportunity(
    market_growth=0.50,
    market_size=150.0,
    competition_level=0.20,
    trend_strength=1.0,
)

assert abs(opportunity["opportunity_score"] - 0.74) < 1e-9
assert opportunity["classification"] == "HIGH"

summary = synthesize(
    sizing,
    trend,
    opportunity,
)

assert summary["growth_rate"] == 0.5
assert summary["trend_direction"] == "UP"
assert summary["opportunity_classification"] == "HIGH"
assert summary["findings"]

agent = MarketIntelligenceAgent()

result = agent.analyze(
    market_size=150.0,
    previous_size=100.0,
    trend_values=[100.0, 110.0, 125.0, 150.0],
    competition_level=0.20,
    period="2026",
)

assert result["agent_id"] == "market-intelligence-agent"
assert result["sizing"]["growth_rate"] == 0.5
assert result["trend"]["direction"] == "UP"
assert result["opportunity"]["classification"] == "HIGH"
assert result["intelligence"]["findings"]

print("86 Market Intelligence Engine  : PASS")
print("87 Market Sizing & Growth      : PASS")
print("88 Market Trend Intelligence   : PASS")
print("89 Market Opportunity Analysis : PASS")
print("90 Market Intelligence Agent   : PASS")
print("==============================================")
print("MILESTONE 86-90 : PASS")
print("==============================================")
