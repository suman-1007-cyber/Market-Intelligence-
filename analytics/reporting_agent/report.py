from __future__ import annotations

from typing import Any


def build(
    findings: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")
    if not isinstance(evidence, list):
        raise TypeError("evidence must be a list")

    return {
        "title": "Market Intelligence Executive Report",
        "finding_count": len(findings),
        "evidence_count": len(evidence),
        "findings": findings,
        "evidence": evidence,
    }
