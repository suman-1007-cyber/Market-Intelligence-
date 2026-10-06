from __future__ import annotations

from typing import Any


def segment(
    customers: list[dict[str, Any]],
    value_field: str = "revenue",
) -> list[dict[str, Any]]:
    if not customers:
        return []

    values = [float(customer[value_field]) for customer in customers]
    ordered = sorted(values)

    def percentile(value: float) -> float:
        if len(ordered) == 1:
            return 1.0

        rank = sum(item <= value for item in ordered) - 1
        return rank / (len(ordered) - 1)

    results = []

    for customer in customers:
        value = float(customer[value_field])
        p = percentile(value)

        if p <= 0.25:
            label = "LOW_VALUE"
        elif p >= 0.75:
            label = "HIGH_VALUE"
        else:
            label = "MID_VALUE"

        item = dict(customer)
        item["segment"] = label
        item["percentile"] = p
        results.append(item)

    return results
