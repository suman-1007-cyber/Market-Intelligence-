from __future__ import annotations

from typing import Any


def sequence(
    actions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pending = [dict(action) for action in actions]
    ordered: list[dict[str, Any]] = []
    completed: set[str] = set()

    while pending:
        ready = [
            action
            for action in pending
            if all(
                dependency in completed
                for dependency in action.get("depends_on", [])
            )
        ]

        if not ready:
            raise ValueError("workflow dependency cycle or unresolved dependency")

        for action in ready:
            action["sequence"] = len(ordered) + 1
            ordered.append(action)
            completed.add(action["action_id"])
            pending.remove(action)

    return ordered
