from __future__ import annotations

from typing import Any, Iterable


def decompose(values: Iterable[float]) -> dict[str, Any]:
    series = [float(value) for value in values]

    if not series:
        return {
            "trend": [],
            "residual": [],
            "mean": 0.0,
        }

    mean = sum(series) / len(series)

    if len(series) == 1:
        trend = [series[0]]
    else:
        first = series[0]
        last = series[-1]
        step = (last - first) / (len(series) - 1)
        trend = [first + step * index for index in range(len(series))]

    residual = [value - trend[index] for index, value in enumerate(series)]

    return {
        "trend": trend,
        "residual": residual,
        "mean": mean,
    }
