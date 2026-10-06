from __future__ import annotations

from typing import Any


def register(
    model_id: str,
    provider: str,
    capabilities: list[str],
    cost_per_request: float = 0.0,
) -> dict[str, Any]:
    if not model_id or not provider:
        raise ValueError("model_id and provider are required")

    return {
        "model_id": str(model_id),
        "provider": str(provider),
        "capabilities": list(capabilities),
        "cost_per_request": max(0.0, float(cost_per_request)),
    }
