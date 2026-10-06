"""Deterministic financial forecasting."""

from typing import Any


def forecast(
    values: list[float],
    periods: int = 1,
) -> dict[str, Any]:
    if not values:
        raise ValueError("At least one value is required.")

    periods = max(1, int(periods))
    numeric = [float(value) for value in values]

    if len(numeric) == 1:
        growth = 0.0
    else:
        previous = numeric[-2]
        current = numeric[-1]
        growth = (
            (current - previous) / previous
            if previous != 0
            else 0.0
        )

    predictions = []
    current = numeric[-1]

    for _ in range(periods):
        current = current * (1.0 + growth)
        predictions.append(round(current, 6))

    return {
        "historical": numeric,
        "growth_rate": round(growth, 6),
        "periods": periods,
        "forecast": predictions,
    }
