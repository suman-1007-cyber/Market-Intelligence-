from __future__ import annotations

from typing import Any


def extract(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")

    risks = []
    for item in findings:
        if not isinstance(item, dict):
            continue

        level = str(item.get("risk_level", "")).upper()
        if level in {"HIGH", "MEDIUM", "LOW"}:
            risks.append({
                "title": item.get("title", item.get("finding", "")),
                "risk_level": level,
            })

    return risks
