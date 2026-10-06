from __future__ import annotations

from typing import Any


def analyze(
    selected_model: dict[str, Any] | None,
    fallback_model: dict[str, Any] | None,
    failure: dict[str, Any],
) -> dict[str, Any]:
    return {
        "selected_model": (
            selected_model.get("model_id")
            if selected_model
            else None
        ),
        "fallback_model": (
            fallback_model.get("model_id")
            if fallback_model
            else None
        ),
        "fallback_used": fallback_model is not None,
        "failure": failure["failed"],
        "routing_status": (
            "FALLBACK"
            if fallback_model is not None
            else "PRIMARY"
            if selected_model is not None
            else "NO_ROUTE"
        ),
    }
