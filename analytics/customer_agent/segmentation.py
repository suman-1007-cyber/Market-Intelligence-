"""Deterministic customer segmentation."""

from typing import Any


def segment(
    records: list[dict[str, Any]],
    value_field: str = "revenue",
    customer_field: str = "customer",
) -> list[dict[str, Any]]:
    if not records:
        return []

    values = []

    for record in records:
        if customer_field not in record:
            raise KeyError(f"Missing customer field: {customer_field}")

        try:
            value = float(record.get(value_field, 0.0))
        except (TypeError, ValueError):
            value = 0.0

        values.append((str(record[customer_field]), max(0.0, value)))

    sorted_values = sorted(
        values,
        key=lambda item: item[1],
        reverse=True,
    )

    count = len(sorted_values)

    results = []

    for index, (customer, value) in enumerate(sorted_values):
        percentile = (index + 1) / count

        if percentile <= 0.25:
            segment_name = "HIGH_VALUE"
        elif percentile <= 0.50:
            segment_name = "MEDIUM_VALUE"
        else:
            segment_name = "LOW_VALUE"

        results.append(
            {
                "customer": customer,
                "value": value,
                "segment": segment_name,
                "rank": index + 1,
            }
        )

    return results
