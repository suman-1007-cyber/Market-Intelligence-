"""Deterministic semantic query resolution."""

from typing import Any

from .dimensions import resolve as resolve_dimension
from .entities import resolve as resolve_entity
from .metrics import resolve as resolve_metric


def resolve(query: dict[str, Any]) -> dict[str, Any]:
    metric = query.get("metric")
    entity = query.get("entity")
    dimensions = query.get("dimensions", [])

    metric_result = resolve_metric(metric) if metric else None
    entity_result = resolve_entity(entity) if entity else None
    dimension_results = [
        resolve_dimension(value)
        for value in dimensions
    ]

    resolved = (
        (metric_result is None or metric_result["resolved"])
        and (entity_result is None or entity_result["resolved"])
        and all(item["resolved"] for item in dimension_results)
    )

    return {
        "resolved": resolved,
        "metric": metric_result,
        "entity": entity_result,
        "dimensions": dimension_results,
    }
