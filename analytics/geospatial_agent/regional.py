from __future__ import annotations

from collections import defaultdict
from typing import Any


def analyze(
    records: list[dict[str, Any]],
    value_field: str,
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[float]] = defaultdict(list)

    for record in records:
        if value_field not in record:
            raise ValueError(
                f"Missing value field: {value_field}"
            )

        grouped[str(record["region"])].append(
            float(record[value_field])
        )

    results = {}

    for region, values in grouped.items():
        results[region] = {
            "count": len(values),
            "total": sum(values),
            "average": sum(values) / len(values),
            "minimum": min(values),
            "maximum": max(values),
        }

    return results
