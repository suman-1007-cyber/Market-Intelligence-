from __future__ import annotations

from typing import Any, Iterable


def forecast(
    values: Iterable[float],
    periods: int = 1,
    model: str = "NAIVE_BASELINE",
) -> dict[str, Any]:
    series = [float(value) for value in values]

    if not series:
        raise ValueError("values must not be empty")

    if periods <= 0:
        raise ValueError("periods must be positive")

    if model == "NAIVE_BASELINE":
        predictions = [series[-1]] * periods

    elif model == "TREND_BASELINE":
        if len(series) < 2:
            predictions = [series[-1]] * periods
        else:
            slope = (series[-1] - series[0]) / (len(series) - 1)
            predictions = [
                series[-1] + slope * step
                for step in range(1, periods + 1)
            ]

    elif model == "SEASONAL_BASELINE":
        if len(series) < 2:
            predictions = [series[-1]] * periods
        else:
            predictions = [
                series[-1 - (step % min(len(series) - 1, periods))]
                for step in range(periods)
            ]

    else:
        raise ValueError(f"Unknown forecast model: {model}")

    return {
        "model": model,
        "periods": int(periods),
        "predictions": predictions,
    }
