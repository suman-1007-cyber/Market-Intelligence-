from __future__ import annotations

from typing import Any


def attach(
    findings: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")
    if not isinstance(evidence, list):
        raise TypeError("evidence must be a list")

    return [
        {
            **item,
            "evidence": evidence,
        }
        for item in findings
        if isinstance(item, dict)
    ]
