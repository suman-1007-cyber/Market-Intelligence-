from __future__ import annotations

from typing import Any


def estimate(
    model: dict[str, Any] | None,
    requests: int = 1,
) -> dict[str, Any]:
    requests = max(0, int(requests))

    if model is None:
        return {
            "requests": requests,
            "cost": 0.0,
        }

    unit_cost = max(
        0.0,
        float(model.get("cost_per_request", 0.0)),
    )

    return {
        "requests": requests,
        "cost": requests * unit_cost,
    }
