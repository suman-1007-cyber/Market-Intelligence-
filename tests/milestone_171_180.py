from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.reporting_agent.findings import collect
from analytics.reporting_agent.prioritization import prioritize
from analytics.reporting_agent.executive_summary import build
from analytics.reporting_agent.recommendations import build as recommendations
from analytics.reporting_agent.risks import extract as risks
from analytics.reporting_agent.opportunities import extract as opportunities
from analytics.reporting_agent.evidence import attach
from analytics.reporting_agent.report import build as report
from analytics.reporting_agent.intelligence import summarize
from analytics.reporting_agent.agent import ReportingExecutiveAgent


findings = [
    {
        "title": "Market growth",
        "priority": 0.80,
        "confidence": 0.90,
        "recommendation": "Expand market coverage",
        "opportunity_level": "HIGH",
    },
    {
        "title": "Competitive pressure",
        "priority": 0.60,
        "confidence": 0.85,
        "risk_level": "MEDIUM",
    },
]

evidence = [
    {"source": "source-a", "url": "https://example.com/a"},
    {"source": "source-b", "url": "https://example.com/b"},
]

collected = collect(findings)
assert collected["count"] == 2

ordered = prioritize(findings)
assert ordered[0]["title"] == "Market growth"

summary = build(findings)
assert summary["finding_count"] == 2
assert summary["key_points"][0] == "Market growth"

recs = recommendations(findings)
assert len(recs) == 1
assert recs[0]["recommendation"] == "Expand market coverage"

risk_items = risks(findings)
assert len(risk_items) == 1
assert risk_items[0]["risk_level"] == "MEDIUM"

opp_items = opportunities(findings)
assert len(opp_items) == 1
assert opp_items[0]["opportunity_level"] == "HIGH"

linked = attach(findings, evidence)
assert len(linked) == 2
assert len(linked[0]["evidence"]) == 2

built_report = report(findings, evidence)
assert built_report["finding_count"] == 2
assert built_report["evidence_count"] == 2

intel = summarize(findings)
assert len(intel["recommendations"]) == 1
assert len(intel["risks"]) == 1
assert len(intel["opportunities"]) == 1

result = ReportingExecutiveAgent().analyze(findings, evidence)
assert result["agent_id"] == "reporting-executive-agent"
assert result["report"]["evidence_count"] == 2
assert result["intelligence"]["executive_summary"]["finding_count"] == 2

print("171 Findings Collection          : PASS")
print("172 Finding Prioritization       : PASS")
print("173 Executive Summary            : PASS")
print("174 Recommendation Engine        : PASS")
print("175 Risk Reporting               : PASS")
print("176 Opportunity Reporting        : PASS")
print("177 Evidence-linked Reporting    : PASS")
print("178 Report Generation            : PASS")
print("179 Executive Intelligence       : PASS")
print("180 Reporting Executive Agent    : PASS")
print("MILESTONE 171-180 : PASS")
