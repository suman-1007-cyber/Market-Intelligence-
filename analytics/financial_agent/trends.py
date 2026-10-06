"""Financial trend intelligence."""

from typing import Any


def analyze(values: list[float]) -> dict[str, Any]:
    if not values:
        return {
            "direction": "EMPTY",
            "change": 0.0,
            "change_rate": 0.0,
            "peak": None,
            "trough": None,
        }

    numeric = [float(value) for value in values]

    change = numeric[-1] - numeric[0]

    change_rate = (
        change / numeric[0]
        if numeric[0] != 0
        else 0.0
    )

    if all(
        numeric[index] <= numeric[index + 1]
        for index in range(len(numeric) - 1)
    ):
        direction = "UP"
    elif all(
        numeric[index] >= numeric[index + 1]
        for index in range(len(numeric) - 1)
    ):
        direction = "DOWN"
    else:
        direction = "MIXED"

    return {
        "direction": direction,
        "change": round(change, 6),
        "change_rate": round(change_rate, 6),
        "peak": max(numeric),
        "trough": min(numeric),
        "peak_index": numeric.index(max(numeric)),
        "trough_index": numeric.index(min(numeric)),
    }
