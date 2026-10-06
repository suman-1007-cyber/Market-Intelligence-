from __future__ import annotations

from collections import defaultdict
from typing import Any


def profile(
    segmented_customers: list[dict[str, Any]],
    value_field: str = "revenue",
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[float]] = defaultdict(list)

    for customer in segmented_customers:
        groups[str(customer["segment"])].append(
            float(customer[value_field])
        )

    results = {}

    for segment, values in groups.items():
        results[segment] = {
            "count": len(values),
            "total_value": sum(values),
            "average_value": sum(values) / len(values),
            "minimum_value": min(values),
            "maximum_value": max(values),
        }

    return results
