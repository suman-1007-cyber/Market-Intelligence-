from __future__ import annotations

from typing import Any


def compare_agents(
    scores: dict[str, float],
) -> dict[str, Any]:
    if not scores:
        return {
            "leader": None,
            "scores": {},
        }

    normalized = {
        str(name): float(value)
        for name, value in scores.items()
    }

    leader = max(normalized, key=normalized.get)

    return {
        "leader": leader,
        "scores": normalized,
    }
