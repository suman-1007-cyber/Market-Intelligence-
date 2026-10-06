from __future__ import annotations

from typing import Any


def build(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")

    recommendations = []
    for item in findings:
        if not isinstance(item, dict):
            continue

        recommendation = item.get("recommendation")
        if recommendation:
            recommendations.append({
                "finding": item.get("title", item.get("finding", "")),
                "recommendation": str(recommendation),
            })

    return recommendations
