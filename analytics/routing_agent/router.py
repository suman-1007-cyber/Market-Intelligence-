from __future__ import annotations

from typing import Any


def select(
    models: list[dict[str, Any]],
    health: dict[str, dict[str, Any]],
    required_capability: str,
) -> dict[str, Any] | None:
    candidates = []

    for model in models:
        model_id = model.get("model_id")
        status = health.get(model_id, {})

        if (
            model_id
            and required_capability in model.get("capabilities", [])
            and status.get("healthy") is True
        ):
            candidates.append(model)

    if not candidates:
        return None

    return min(
        candidates,
        key=lambda item: float(item.get("cost_per_request", 0.0)),
    )
