from __future__ import annotations

from typing import Any


def estimate(
    requests: int,
    cost_per_request: float,
    cpu_seconds: float = 0.0,
    cost_per_cpu_second: float = 0.0,
) -> dict[str, Any]:
    requests = max(0, int(requests))
    cost_per_request = max(0.0, float(cost_per_request))
    cpu_seconds = max(0.0, float(cpu_seconds))
    cost_per_cpu_second = max(0.0, float(cost_per_cpu_second))

    request_cost = requests * cost_per_request
    compute_cost = cpu_seconds * cost_per_cpu_second

    return {
        "request_cost": request_cost,
        "compute_cost": compute_cost,
        "total_cost": request_cost + compute_cost,
    }
