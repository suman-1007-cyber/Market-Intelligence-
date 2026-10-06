from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.governance_agent.policy import evaluate
from analytics.governance_agent.access import check
from analytics.governance_agent.secrets import scan
from analytics.governance_agent.audit import record
from analytics.governance_agent.integrity import fingerprint, verify
from analytics.governance_agent.privacy import sanitize
from analytics.governance_agent.validation import validate
from analytics.governance_agent.risk import assess
from analytics.governance_agent.intelligence import analyze
from analytics.governance_agent.agent import GovernanceSecurityAgent


policy = evaluate("read_market", ["read_market", "analyze_market"])
assert policy["allowed"] is True
assert policy["decision"] == "ALLOW"

access = check(
    "analyst",
    "market_data",
    {"analyst": ["market_data", "reports"]},
)
assert access["granted"] is True

no_access = check(
    "guest",
    "market_data",
    {"guest": ["reports"]},
)
assert no_access["granted"] is False

clean = scan("normal market analytics payload")
assert clean["secret_detected"] is False

secret = scan("api_key=ABC123")
assert secret["secret_detected"] is True

event = record("test_event", "analyst", {"value": 10})
assert event["event"] == "test_event"
assert event["actor"] == "analyst"
assert event["timestamp"]

data = {"market": "A", "value": 100}
digest = fingerprint(data)
assert len(digest) == 64
assert verify(data, digest) is True
assert verify({"market": "B", "value": 100}, digest) is False

safe = sanitize({
    "market": "A",
    "api_key": "SECRET",
    "value": 100,
})
assert safe["api_key"] == "***REDACTED***"
assert safe["value"] == 100

validation = validate(
    policy,
    access,
    clean,
)
assert validation["valid"] is True

risk = assess(
    validation["policy_valid"],
    validation["access_valid"],
    validation["secrets_valid"],
)
assert risk["risk_level"] == "LOW"
assert risk["failure_count"] == 0

intel = analyze(validation, risk)
assert intel["governance_valid"] is True
assert intel["risk_level"] == "LOW"
assert intel["actionable"] is False

result = GovernanceSecurityAgent().analyze(
    action="read_market",
    actor="analyst",
    resource="market_data",
    allowed_actions=["read_market", "analyze_market"],
    permissions={"analyst": ["market_data", "reports"]},
    payload={"market": "A", "value": 100},
)

assert result["agent_id"] == "governance-security-agent"
assert result["validation"]["valid"] is True
assert result["risk"]["risk_level"] == "LOW"
assert result["sanitized_payload"]["value"] == 100
assert len(result["fingerprint"]) == 64

print("201 Governance Policy Engine       : PASS")
print("202 Access Control                  : PASS")
print("203 Secret Detection                : PASS")
print("204 Governance Audit                : PASS")
print("205 Data Integrity                  : PASS")
print("206 Privacy / Sanitization          : PASS")
print("207 Governance Validation           : PASS")
print("208 Security Risk Assessment        : PASS")
print("209 Governance Intelligence         : PASS")
print("210 Governance Security Agent       : PASS")
print("MILESTONE 201-210 : PASS")
