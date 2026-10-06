from __future__ import annotations

from typing import Any


def recover(
    result: dict[str, Any],
    retryable: bool = True,
) -> dict[str, Any]:
    failed = not bool(result.get("success"))

    if not failed:
        action = "NONE"
    elif retryable:
        action = "RETRY"
    else:
        action = "STOP"

    return {
        "action_id": result.get("action_id"),
        "failed": failed,
        "recovery_action": action,
    }
