from __future__ import annotations

from typing import Any


def validate(
    actions: list[dict[str, Any]],
) -> dict[str, Any]:
    valid = True
    errors: list[str] = []

    for index, action in enumerate(actions, start=1):
        if not action.get("action_id"):
            valid = False
            errors.append(f"action_{index}: missing action_id")

        if not action.get("name"):
            valid = False
            errors.append(f"action_{index}: missing name")

    return {
        "valid": valid,
        "errors": errors,
        "action_count": len(actions),
    }
