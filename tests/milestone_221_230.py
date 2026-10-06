from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.observability_agent.events import create
from analytics.observability_agent.latency import measure
from analytics.observability_agent.errors import classify
from analytics.observability_agent.resources import record
from analytics.observability_agent.cost import estimate
from analytics.observability_agent.health import assess
from analytics.observability_agent.aggregation import aggregate
from analytics.observability_agent.intelligence import analyze
from analytics.observability_agent.agent import ObservabilityCostAgent


event = create(
    "execution",
    "agent-a",
    {"task": "analysis"},
)
assert event["event_type"] == "execution"
assert event["agent_id"] == "agent-a"
assert event["details"]["task"] == "analysis"

latency = measure(10, 12.5)
assert abs(latency["elapsed_seconds"] - 2.5) < 1e-9

negative_latency = measure(12.5, 10)
assert negative_latency["elapsed_seconds"] == 0.0

no_error = classify(None)
assert no_error["has_error"] is False
assert no_error["type"] == "NONE"

retryable = classify("timeout", retryable=True)
assert retryable["has_error"] is True
assert retryable["type"] == "RETRYABLE"
assert retryable["retryable"] is True

resources = record(
    cpu_seconds=4,
    memory_mb=512,
    requests=10,
)
assert resources["cpu_seconds"] == 4
assert resources["memory_mb"] == 512
assert resources["requests"] == 10

cost = estimate(
    requests=10,
    cost_per_request=0.02,
    cpu_seconds=5,
    cost_per_cpu_second=0.01,
)
assert abs(cost["request_cost"] - 0.20) < 1e-9
assert abs(cost["compute_cost"] - 0.05) < 1e-9
assert abs(cost["total_cost"] - 0.25) < 1e-9

health = assess(
    error_count=0,
    latency_seconds=0.5,
    max_latency_seconds=1.0,
)
assert health["status"] == "HEALTHY"

degraded = assess(
    error_count=1,
    latency_seconds=0.5,
    max_latency_seconds=1.0,
)
assert degraded["status"] == "DEGRADED"

slow = assess(
    error_count=0,
    latency_seconds=2.0,
    max_latency_seconds=1.0,
)
assert slow["status"] == "SLOW"

events = [
    create("execution", "agent-a"),
    create("error", "agent-a"),
]
aggregation = aggregate(events)
assert aggregation["event_count"] == 2
assert aggregation["error_count"] == 1

intel = analyze(
    health,
    resources,
    cost,
)
assert intel["status"] == "HEALTHY"
assert intel["requests"] == 10
assert intel["needs_attention"] is False

result = ObservabilityCostAgent().analyze(
    start=10,
    end=10.5,
    requests=10,
    cost_per_request=0.02,
    cpu_seconds=5,
    cost_per_cpu_second=0.01,
    errors=[],
    max_latency_seconds=1.0,
)

assert result["agent_id"] == "observability-cost-agent"
assert abs(result["latency"]["elapsed_seconds"] - 0.5) < 1e-9
assert abs(result["cost"]["total_cost"] - 0.25) < 1e-9
assert result["health"]["status"] == "HEALTHY"
assert result["aggregation"]["error_count"] == 0

print("221 Observability Event Model       : PASS")
print("222 Latency Measurement              : PASS")
print("223 Error Classification             : PASS")
print("224 Resource Tracking                : PASS")
print("225 Cost Estimation                  : PASS")
print("226 Operational Health               : PASS")
print("227 Event Aggregation                : PASS")
print("228 Observability Intelligence       : PASS")
print("229 Observability Integration        : PASS")
print("230 Observability Cost Agent         : PASS")
print("MILESTONE 221-230 : PASS")
