from __future__ import annotations

from typing import Any


def assess(
    results: list[dict[str, Any]],
    total_actions: int,
) -> dict[str, Any]:
    total_actions = max(0, int(total_actions))
    completed = sum(
        1
        for result in results
        if result.get("success") is True
    )
    failed = sum(
        1
        for result in results
        if result.get("success") is False
    )

    if failed:
        workflow_status = "FAILED"
    elif completed >= total_actions and total_actions > 0:
        workflow_status = "COMPLETED"
    else:
        workflow_status = "RUNNING"

    return {
        "status": workflow_status,
        "total_actions": total_actions,
        "completed": completed,
        "failed": failed,
    }
