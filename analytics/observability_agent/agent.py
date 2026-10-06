from __future__ import annotations

from typing import Any

from .events import create
from .latency import measure
from .errors import classify
from .resources import record
from .cost import estimate
from .health import assess
from .aggregation import aggregate
from .intelligence import analyze


class ObservabilityCostAgent:
    agent_id = "observability-cost-agent"

    def analyze(
        self,
        start: float,
        end: float,
        requests: int,
        cost_per_request: float,
        cpu_seconds: float = 0.0,
        cost_per_cpu_second: float = 0.0,
        errors: list[dict[str, Any]] | None = None,
        max_latency_seconds: float = 1.0,
    ) -> dict[str, Any]:
        latency = measure(start, end)
        resources = record(
            cpu_seconds=cpu_seconds,
            requests=requests,
        )

        cost = estimate(
            requests=requests,
            cost_per_request=cost_per_request,
            cpu_seconds=cpu_seconds,
            cost_per_cpu_second=cost_per_cpu_second,
        )

        error_events = errors or []
        error_count = len(error_events)

        health = assess(
            error_count=error_count,
            latency_seconds=latency["elapsed_seconds"],
            max_latency_seconds=max_latency_seconds,
        )

        events = [
            create("execution", self.agent_id, latency),
        ]

        for error in error_events:
            events.append(
                create("error", self.agent_id, error)
            )

        aggregation = aggregate(events)

        return {
            "agent_id": self.agent_id,
            "latency": latency,
            "resources": resources,
            "cost": cost,
            "health": health,
            "events": events,
            "aggregation": aggregation,
            "intelligence": analyze(
                health,
                resources,
                cost,
            ),
        }
