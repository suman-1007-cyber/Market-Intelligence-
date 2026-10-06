from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.routing_agent.models import register
from analytics.routing_agent.health import evaluate
from analytics.routing_agent.capability import matches
from analytics.routing_agent.router import select
from analytics.routing_agent.fallback import choose
from analytics.routing_agent.failure import classify
from analytics.routing_agent.cost import estimate
from analytics.routing_agent.quality import validate
from analytics.routing_agent.intelligence import analyze
from analytics.routing_agent.agent import ModelRoutingFallbackAgent


model_a = register(
    "model-a",
    "provider-a",
    ["analysis", "forecast"],
    cost_per_request=0.10,
)

model_b = register(
    "model-b",
    "provider-b",
    ["analysis"],
    cost_per_request=0.05,
)

models = [model_a, model_b]

assert model_a["model_id"] == "model-a"
assert model_a["provider"] == "provider-a"
assert model_a["cost_per_request"] == 0.10

healthy = evaluate(
    available=True,
    error_rate=0.10,
    latency_seconds=0.5,
)
assert healthy["healthy"] is True

unhealthy = evaluate(
    available=False,
    error_rate=0.0,
)
assert unhealthy["healthy"] is False

assert matches(model_a, "forecast") is True
assert matches(model_b, "forecast") is False

health = {
    "model-a": healthy,
    "model-b": evaluate(True, 0.05, 0.3),
}

selected = select(
    models,
    health,
    "analysis",
)
assert selected["model_id"] == "model-b"

fallback = choose(
    models,
    "model-b",
    health,
    "analysis",
)
assert fallback["model_id"] == "model-a"

failure = classify(
    "model-b",
    "timeout",
    retryable=True,
)
assert failure["failed"] is True
assert failure["retryable"] is True

cost = estimate(model_b, requests=4)
assert abs(cost["cost"] - 0.20) < 1e-9

quality = validate(model_b, "analysis")
assert quality["valid"] is True

intel = analyze(
    model_b,
    model_a,
    failure,
)
assert intel["fallback_used"] is True
assert intel["routing_status"] == "FALLBACK"

result = ModelRoutingFallbackAgent().route(
    models=models,
    health=health,
    required_capability="analysis",
    failed_model="model-b",
    error="timeout",
)

assert result["agent_id"] == "model-routing-fallback-agent"
assert result["selected_model"]["model_id"] == "model-b"
assert result["fallback_model"]["model_id"] == "model-a"
assert result["active_model"]["model_id"] == "model-a"
assert result["validation"]["valid"] is True
assert result["intelligence"]["fallback_used"] is True

print("231 Model Registry                  : PASS")
print("232 Model Health Evaluation         : PASS")
print("233 Capability Matching             : PASS")
print("234 Deterministic Model Router      : PASS")
print("235 Fallback Selection              : PASS")
print("236 Failure Classification          : PASS")
print("237 Routing Cost Estimation         : PASS")
print("238 Routing Quality Validation      : PASS")
print("239 Routing Intelligence            : PASS")
print("240 Model Routing/Fallback Agent    : PASS")
print("MILESTONE 231-240 : PASS")
