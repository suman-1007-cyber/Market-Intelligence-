from __future__ import annotations

from typing import Any


def resolve(
    actions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    completed: set[str] = set()
    resolved = []

    for action in actions:
        item = dict(action)
        dependencies = item.get("depends_on", [])

        ready = all(
            dependency in completed
            for dependency in dependencies
        )

        item["ready"] = ready
        resolved.append(item)

        if ready and item.get("status") == "COMPLETED":
            completed.add(item["action_id"])

    return resolved
