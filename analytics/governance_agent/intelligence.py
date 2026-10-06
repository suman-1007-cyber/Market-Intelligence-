from __future__ import annotations

from typing import Any


def analyze(
    validation: dict[str, Any],
    risk: dict[str, Any],
) -> dict[str, Any]:
    return {
        "governance_valid": validation["valid"],
        "risk_level": risk["risk_level"],
        "failure_count": risk["failure_count"],
        "actionable": not validation["valid"],
    }
