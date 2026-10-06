from __future__ import annotations

from typing import Any


def validate(
    selected_model: dict[str, Any] | None,
    required_capability: str,
) -> dict[str, Any]:
    valid = (
        selected_model is not None
        and required_capability
        in selected_model.get("capabilities", [])
    )

    return {
        "valid": valid,
        "required_capability": required_capability,
        "selected_model": (
            selected_model.get("model_id")
            if selected_model
            else None
        ),
    }
