from __future__ import annotations

from typing import Any


def evaluate(
    action: str,
    allowed_actions: list[str],
) -> dict[str, Any]:
    if not action:
        raise ValueError("action must not be empty")

    allowed = action in set(allowed_actions)

    return {
        "action": action,
        "allowed": allowed,
        "decision": "ALLOW" if allowed else "DENY",
    }
