"""Deterministic competitive benchmarking."""

from typing import Any


def benchmark(
    profiles: list[dict[str, Any]],
    metric: str,
) -> dict[str, Any]:
    values = []

    for profile in profiles:
        value = profile.get(metric)

        if value is None:
            continue

        values.append(
            {
                "company": profile["company"],
                "value": float(value),
            }
        )

    values.sort(
        key=lambda item: item["value"],
        reverse=True,
    )

    if not values:
        return {
            "metric": metric,
            "benchmarks": [],
            "leader": None,
            "average": None,
        }

    average = sum(
        item["value"]
        for item in values
    ) / len(values)

    return {
        "metric": metric,
        "benchmarks": values,
        "leader": values[0]["company"],
        "average": average,
    }
