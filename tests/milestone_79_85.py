"""Milestones 79-85: Investigation Intelligence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.investigation_agent.agent import InvestigationAgent
from analytics.investigation_agent.cross_source import compare
from analytics.investigation_agent.evidence import collect
from analytics.investigation_agent.hypotheses import generate, score
from analytics.investigation_agent.planner import plan
from analytics.investigation_agent.root_cause import investigate
from analytics.investigation_agent.synthesis import synthesize


question = "Why did product sales decline?"

investigation_plan = plan(question)
assert investigation_plan.question == question
assert "generate_hypotheses" in investigation_plan.steps

hypotheses = generate(question)
assert len(hypotheses) == 4
assert hypotheses[0].hypothesis_id == "H1"

evidence = collect(
    [
        {
            "evidence_id": "E1",
            "source": "source-a",
            "claim": "Market demand declined",
            "supports": ["H1"],
            "strength": 0.9,
        },
        {
            "evidence_id": "E2",
            "source": "source-b",
            "claim": "Market demand declined",
            "supports": ["H1"],
            "strength": 0.8,
        },
        {
            "evidence_id": "E3",
            "source": "source-c",
            "claim": "Competition increased",
            "supports": ["H2"],
            "contradicts": ["H3"],
            "strength": 0.7,
        },
    ]
)

assert len(evidence) == 3

scored = score(hypotheses[0], 2, 0)
assert scored["evidence_score"] == 1.0

cross_source = compare(
    [item.to_dict() for item in evidence]
)
assert cross_source["multi_source_claims"] == 1

root_causes = investigate(
    [scored],
    [item.to_dict() for item in evidence],
)
assert root_causes[0]["status"] == "SUPPORTED"

summary = synthesize(
    question,
    root_causes,
    cross_source,
)
assert summary["conclusion"] is not None
assert summary["confidence"] > 0

agent = InvestigationAgent()
result = agent.investigate(
    question,
    [
        {
            "source": "source-a",
            "claim": "Market demand declined",
            "supports": ["H1"],
            "strength": 0.9,
        },
        {
            "source": "source-b",
            "claim": "Market demand declined",
            "supports": ["H1"],
            "strength": 0.8,
        },
    ],
)

assert result["agent_id"] == "investigation-agent"
assert result["plan"]["question"] == question
assert len(result["hypotheses"]) == 4
assert len(result["evidence"]) == 2
assert result["cross_source"]["multi_source_claims"] == 1
assert result["root_causes"]
assert result["synthesis"]["conclusion"] is not None

print("79 Investigation Planner       : PASS")
print("80 Hypothesis Engine           : PASS")
print("81 Evidence Collector          : PASS")
print("82 Cross-source Investigator   : PASS")
print("83 Root Cause Investigation    : PASS")
print("84 Investigation Synthesis     : PASS")
print("85 Investigation Agent         : PASS")
print("==============================================")
print("MILESTONE 79-85 : PASS")
print("==============================================")
