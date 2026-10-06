from __future__ import annotations

from typing import Any, Iterable


def detect(values: Iterable[float]) -> dict[str, Any]:
    series = [float(value) for value in values]

    if not series:
        return {
            "direction": "EMPTY",
            "change": 0.0,
            "change_rate": 0.0,
        }

    if len(series) == 1:
        return {
            "direction": "FLAT",
            "change": 0.0,
            "change_rate": 0.0,
        }

    change = series[-1] - series[0]
    change_rate = (
        change / abs(series[0])
        if series[0] != 0
        else 0.0
    )

    if all(
        series[index] <= series[index + 1]
        for index in range(len(series) - 1)
    ):
        direction = "UP"
    elif all(
        series[index] >= series[index + 1]
        for index in range(len(series) - 1)
    ):
        direction = "DOWN"
    elif change == 0:
        direction = "FLAT"
    else:
        direction = "MIXED"

    return {
        "direction": direction,
        "change": change,
        "change_rate": change_rate,
    }
