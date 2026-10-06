from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.evaluation_agent.cases import create
from analytics.evaluation_agent.scoring import score
from analytics.evaluation_agent.accuracy import calculate
from analytics.evaluation_agent.failures import collect
from analytics.evaluation_agent.regression import compare
from analytics.evaluation_agent.reliability import assess
from analytics.evaluation_agent.benchmark import compare_agents
from analytics.evaluation_agent.report import build
from analytics.evaluation_agent.intelligence import analyze
from analytics.evaluation_agent.agent import AgentEvaluationAgent


case_a = create("case-a", {"x": 1}, 10)
case_b = create("case-b", {"x": 2}, 20)

assert case_a["case_id"] == "case-a"
assert case_b["expected"] == 20

matched = score(10, 10)
assert matched["matched"] is True
assert matched["score"] == 1.0

failed = score(10, 20)
assert failed["matched"] is False
assert failed["score"] == 0.0

accuracy = calculate([1.0, 1.0, 0.0])
assert accuracy["count"] == 3
assert abs(accuracy["accuracy"] - (2 / 3)) < 1e-9

cases = [case_a, case_b]
results = [
    {"matched": True, "actual": 10},
    {"matched": False, "actual": 30},
]

failures = collect(cases, results)
assert len(failures) == 1
assert failures[0]["case_id"] == "case-b"

regression = compare(0.60, 0.80)
assert regression["direction"] == "IMPROVED"
assert abs(regression["change"] - 0.20) < 1e-9

regression_down = compare(0.90, 0.80)
assert regression_down["direction"] == "REGRESSED"

reliability = assess(1.0, 0)
assert reliability["reliability"] == "HIGH"

reliability_low = assess(0.50, 2)
assert reliability_low["reliability"] == "LOW"

benchmark = compare_agents({
    "agent-a": 0.80,
    "agent-b": 0.90,
})
assert benchmark["leader"] == "agent-b"

report = build(
    {"accuracy": 1.0, "count": 2},
    {"reliability": "HIGH"},
    [],
)
assert report["failure_count"] == 0

intel = analyze(
    {"accuracy": 1.0},
    {"reliability": "HIGH"},
    {"direction": "IMPROVED"},
)
assert intel["needs_attention"] is False

result = AgentEvaluationAgent().evaluate(
    cases,
    [10, 30],
    previous_accuracy=0.50,
)

assert result["agent_id"] == "agent-evaluation-agent"
assert abs(result["accuracy"]["accuracy"] - 0.50) < 1e-9
assert len(result["failures"]) == 1
assert result["regression"]["direction"] == "UNCHANGED"
assert result["reliability"]["reliability"] == "LOW"
assert result["intelligence"]["needs_attention"] is True

print("211 Evaluation Case Model          : PASS")
print("212 Evaluation Scoring              : PASS")
print("213 Accuracy Measurement            : PASS")
print("214 Failure Analysis                : PASS")
print("215 Regression Detection            : PASS")
print("216 Reliability Assessment          : PASS")
print("217 Agent Benchmarking              : PASS")
print("218 Evaluation Reporting            : PASS")
print("219 Evaluation Intelligence         : PASS")
print("220 Agent Evaluation Agent          : PASS")
print("MILESTONE 211-220 : PASS")
