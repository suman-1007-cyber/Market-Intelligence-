"""Deterministic business metric definitions."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MetricDefinition:
    name: str
    expression: str
    description: str
    dependencies: tuple[str, ...]
    unit: str


METRICS = {
    "revenue": MetricDefinition(
        "revenue",
        "sum(revenue)",
        "Total revenue.",
        ("revenue",),
        "currency",
    ),
    "sales": MetricDefinition(
        "sales",
        "sum(sales)",
        "Total sales.",
        ("sales",),
        "currency",
    ),
    "customers": MetricDefinition(
        "customers",
        "sum(customers)",
        "Total customers.",
        ("customers",),
        "count",
    ),
    "average_price": MetricDefinition(
        "average_price",
        "revenue / units",
        "Average selling price.",
        ("revenue", "units"),
        "currency_per_unit",
    ),
    "growth_rate": MetricDefinition(
        "growth_rate",
        "(current - previous) / previous",
        "Period-over-period growth rate.",
        ("current", "previous"),
        "ratio",
    ),
}


def resolve(name: str) -> dict[str, Any]:
    key = str(name).strip().lower()
    metric = METRICS.get(key)

    if metric is None:
        return {
            "name": name,
            "resolved": False,
            "definition": None,
            "confidence": 0.0,
        }

    return {
        "name": metric.name,
        "resolved": True,
        "definition": metric.expression,
        "description": metric.description,
        "dependencies": list(metric.dependencies),
        "unit": metric.unit,
        "confidence": 1.0,
    }
