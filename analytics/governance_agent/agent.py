from __future__ import annotations

from typing import Any

from .policy import evaluate
from .access import check
from .secrets import scan
from .audit import record
from .integrity import fingerprint
from .privacy import sanitize
from .validation import validate
from .risk import assess
from .intelligence import analyze


class GovernanceSecurityAgent:
    agent_id = "governance-security-agent"

    def analyze(
        self,
        action: str,
        actor: str,
        resource: str,
        allowed_actions: list[str],
        permissions: dict[str, list[str]],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        policy = evaluate(action, allowed_actions)
        access = check(actor, resource, permissions)

        raw_text = str(payload)
        secret_scan = scan(raw_text)

        validation = validate(policy, access, secret_scan)
        risk = assess(
            validation["policy_valid"],
            validation["access_valid"],
            validation["secrets_valid"],
        )

        audit_event = record(
            event="governance_evaluation",
            actor=actor,
            details={
                "action": action,
                "resource": resource,
                "decision": validation["valid"],
            },
        )

        safe_payload = sanitize(payload)
        data_fingerprint = fingerprint(safe_payload)

        return {
            "agent_id": self.agent_id,
            "policy": policy,
            "access": access,
            "secret_scan": secret_scan,
            "validation": validation,
            "risk": risk,
            "audit": audit_event,
            "sanitized_payload": safe_payload,
            "fingerprint": data_fingerprint,
            "intelligence": analyze(validation, risk),
        }
