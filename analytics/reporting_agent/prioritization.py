from __future__ import annotations

from typing import Any


def prioritize(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")

    def score(item: dict[str, Any]) -> float:
        value = item.get("priority", item.get("confidence", 0))
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    return sorted(
        [item for item in findings if isinstance(item, dict)],
        key=score,
        reverse=True,
    )
