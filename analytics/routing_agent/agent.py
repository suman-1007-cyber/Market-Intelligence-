from __future__ import annotations

from typing import Any

from .router import select
from .fallback import choose
from .failure import classify
from .cost import estimate
from .quality import validate
from .intelligence import analyze


class ModelRoutingFallbackAgent:
    agent_id = "model-routing-fallback-agent"

    def route(
        self,
        models: list[dict[str, Any]],
        health: dict[str, dict[str, Any]],
        required_capability: str,
        failed_model: str | None = None,
        error: str | None = None,
    ) -> dict[str, Any]:
        selected = select(
            models,
            health,
            required_capability,
        )

        failure = classify(
            failed_model or "",
            error,
        )

        fallback = None

        if failed_model and error:
            fallback = choose(
                models,
                failed_model,
                health,
                required_capability,
            )

        active_model = fallback or selected

        return {
            "agent_id": self.agent_id,
            "selected_model": selected,
            "fallback_model": fallback,
            "active_model": active_model,
            "failure": failure,
            "cost": estimate(active_model),
            "validation": validate(
                active_model,
                required_capability,
            ),
            "intelligence": analyze(
                selected,
                fallback,
                failure,
            ),
        }
