from __future__ import annotations

from typing import Any


def build(findings: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")

    priorities = []
    for item in findings:
        if not isinstance(item, dict):
            continue
        title = item.get("title", item.get("finding", item.get("type", "")))
        if title:
            priorities.append(str(title))

    return {
        "finding_count": len(findings),
        "key_points": priorities[:5],
    }
