"""Milestones 91-95: Competitive Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.competitive_agent.agent import (
    CompetitiveIntelligenceAgent,
)
from analytics.competitive_agent.benchmark import benchmark
from analytics.competitive_agent.discovery import discover
from analytics.competitive_agent.intelligence import synthesize
from analytics.competitive_agent.profiling import profile
from analytics.competitive_agent.threats import analyze


records = [
    {
        "company": "Alpha",
        "market_share": 0.40,
        "revenue": 500.0,
        "products": ["A"],
        "strengths": ["brand", "distribution"],
        "source": "source-a",
    },
    {
        "company": "Beta",
        "market_share": 0.25,
        "revenue": 300.0,
        "products": ["B"],
        "weaknesses": ["price"],
        "source": "source-b",
    },
    {
        "company": "Gamma",
        "market_share": 0.10,
        "revenue": 100.0,
        "products": ["C"],
        "weaknesses": ["distribution"],
        "source": "source-c",
    },
    {
        "company": "Alpha",
        "market_share": 0.40,
        "revenue": 500.0,
        "source": "source-d",
    },
]


discovered = discover(records)

assert len(discovered) == 3
assert discovered[0]["company"] == "Alpha"
assert discovered[0]["source_count"] == 2

profiles = profile(records)

assert len(profiles) == 3
assert profiles[0]["company"] == "Alpha"
assert profiles[0]["market_share"] == 0.40
assert "brand" in profiles[0]["strengths"]

benchmarks = benchmark(
    profiles,
    "market_share",
)

assert benchmarks["leader"] == "Alpha"
assert abs(benchmarks["average"] - 0.25) < 1e-9

assessment = analyze(
    profiles[0],
    market_average_share=0.25,
    leader_share=0.40,
)

assert assessment["threat_level"] == "HIGH"
assert assessment["threat_score"] >= 0.60

summary = synthesize(
    discovered,
    profiles,
    benchmarks,
    [assessment],
)

assert summary["competitor_count"] == 3
assert summary["leader"] == "Alpha"
assert summary["findings"]

agent = CompetitiveIntelligenceAgent()

result = agent.analyze(
    records,
    benchmark_metric="market_share",
)

assert result["agent_id"] == "competitive-intelligence-agent"
assert len(result["discovery"]) == 3
assert len(result["profiles"]) == 3
assert result["benchmarks"]["leader"] == "Alpha"
assert result["assessments"]
assert result["intelligence"]["competitor_count"] == 3

print("91 Competitor Discovery             : PASS")
print("92 Competitor Profiling             : PASS")
print("93 Competitive Benchmarking         : PASS")
print("94 Competitive Threat / Opportunity : PASS")
print("95 Competitive Intelligence Agent   : PASS")
print("==============================================")
print("MILESTONE 91-95 : PASS")
print("==============================================")
