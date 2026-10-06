from __future__ import annotations

from typing import Any


def create(
    workflow_id: str,
    actions: list[dict[str, Any]],
) -> dict[str, Any]:
    if not workflow_id:
        raise ValueError("workflow_id is required")
    if not isinstance(actions, list):
        raise TypeError("actions must be a list")

    return {
        "workflow_id": str(workflow_id),
        "actions": actions,
        "action_count": len(actions),
    }
