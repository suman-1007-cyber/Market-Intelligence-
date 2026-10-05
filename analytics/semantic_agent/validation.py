"""Semantic validation."""

from typing import Any


def validate(resolution: dict[str, Any]) -> dict[str, Any]:
    errors = []

    metric = resolution.get("metric")
    entity = resolution.get("entity")
    dimensions = resolution.get("dimensions", [])

    if metric is not None and not metric.get("resolved", False):
        errors.append("Unresolved metric.")

    if entity is not None and not entity.get("resolved", False):
        errors.append("Unresolved entity.")

    for dimension in dimensions:
        if not dimension.get("resolved", False):
            errors.append(
                f"Unresolved dimension: {dimension.get('input')}"
            )

    return {
        "valid": not errors,
        "errors": errors,
        "confidence": 1.0 if not errors else 0.0,
    }
