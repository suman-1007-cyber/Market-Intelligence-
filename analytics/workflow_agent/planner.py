from __future__ import annotations

from typing import Any


def plan(
    actions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(actions, list):
        raise TypeError("actions must be a list")

    planned = []

    for index, action in enumerate(actions, start=1):
        if not isinstance(action, dict):
            raise TypeError("each action must be a dictionary")

        item = dict(action)
        item["sequence"] = index
        item["status"] = "PLANNED"
        planned.append(item)

    return planned
