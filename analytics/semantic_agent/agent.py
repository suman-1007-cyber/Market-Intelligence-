"""Semantic Intelligence Agent."""

from dataclasses import dataclass
from typing import Any

from .dependencies import build as build_dependencies
from .dimensions import DIMENSIONS
from .metrics import METRICS
from .query import resolve
from .validation import validate


@dataclass
class SemanticIntelligenceAgent:
    agent_id: str = "semantic-intelligence-agent"

    def analyze(self, query: dict[str, Any]) -> dict[str, Any]:
        metric_definitions = {
            name: {
                "dependencies": list(metric.dependencies),
                "expression": metric.expression,
            }
            for name, metric in METRICS.items()
        }

        resolution = resolve(query)
        validation = validate(resolution)

        graph = build_dependencies(metric_definitions)

        return {
            "agent_id": self.agent_id,
            "query": query,
            "resolution": resolution,
            "validation": validation,
            "metric_dependencies": graph,
            "known_dimensions": sorted(DIMENSIONS),
        }
