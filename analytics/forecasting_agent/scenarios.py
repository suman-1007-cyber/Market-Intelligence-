from __future__ import annotations

from typing import Any, Iterable


def generate(
    baseline: Iterable[float],
    growth_rates: Iterable[float],
) -> dict[str, Any]:
    baseline_values = [float(value) for value in baseline]
    rates = [float(rate) for rate in growth_rates]

    if not baseline_values:
        raise ValueError("baseline must not be empty")

    scenarios: dict[str, list[float]] = {}

    for rate in rates:
        name = (
            "BASE"
            if rate == 0
            else "UPSIDE"
            if rate > 0
            else "DOWNSIDE"
        )

        scenarios[name] = [
            value * (1.0 + rate)
            for value in baseline_values
        ]

    return {
        "baseline": baseline_values,
        "growth_rates": rates,
        "scenarios": scenarios,
    }
