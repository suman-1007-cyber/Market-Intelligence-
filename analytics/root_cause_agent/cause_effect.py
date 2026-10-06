from __future__ import annotations

from typing import Any, Iterable


def correlation(
    target: Iterable[float],
    driver: Iterable[float],
) -> float:
    y = [float(value) for value in target]
    x = [float(value) for value in driver]

    if len(x) != len(y):
        raise ValueError("target and driver must have equal length")

    if len(x) < 2:
        return 0.0

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = sum(
        (a - mean_x) * (b - mean_y)
        for a, b in zip(x, y)
    )

    denominator_x = sum(
        (value - mean_x) ** 2 for value in x
    )
    denominator_y = sum(
        (value - mean_y) ** 2 for value in y
    )

    denominator = (denominator_x * denominator_y) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def analyze(
    target: Iterable[float],
    drivers: dict[str, Iterable[float]],
) -> dict[str, Any]:
    results = {}

    for name, values in drivers.items():
        value = correlation(target, values)

        if value > 0:
            direction = "POSITIVE"
        elif value < 0:
            direction = "NEGATIVE"
        else:
            direction = "NONE"

        results[str(name)] = {
            "correlation": value,
            "absolute_correlation": abs(value),
            "direction": direction,
        }

    return results
