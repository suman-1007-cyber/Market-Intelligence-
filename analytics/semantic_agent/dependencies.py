"""Metric dependency graph."""

from typing import Any


def build(metric_definitions: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    for name, definition in metric_definitions.items():
        graph[str(name)] = [
            str(item)
            for item in definition.get("dependencies", [])
        ]

    return graph


def dependencies(graph: dict[str, list[str]], metric: str) -> list[str]:
    return list(graph.get(metric, []))
