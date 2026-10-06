from __future__ import annotations

from typing import Any


def choose(
    models: list[dict[str, Any]],
    failed_model: str,
    health: dict[str, dict[str, Any]],
    required_capability: str,
) -> dict[str, Any] | None:
    remaining = [
        model
        for model in models
        if model.get("model_id") != failed_model
    ]

    from .router import select

    return select(
        remaining,
        health,
        required_capability,
    )
