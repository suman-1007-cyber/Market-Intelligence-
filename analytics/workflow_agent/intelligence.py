from __future__ import annotations

from typing import Any


def analyze(
    validation: dict[str, Any],
    status: dict[str, Any],
    recovery: list[dict[str, Any]],
) -> dict[str, Any]:
    retry_count = sum(
        1
        for item in recovery
        if item.get("recovery_action") == "RETRY"
    )

    return {
        "workflow_status": status["status"],
        "valid": validation["valid"],
        "completed": status["completed"],
        "failed": status["failed"],
        "retry_count": retry_count,
        "needs_attention": (
            not validation["valid"]
            or status["failed"] > 0
        ),
    }
