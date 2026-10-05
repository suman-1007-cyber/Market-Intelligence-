"""Deterministic market trend intelligence."""

from typing import Any


def analyze(values: list[float]) -> dict[str, Any]:
    if not values:
        raise ValueError("Trend series cannot be empty")

    series = [float(value) for value in values]

    if any(not (-float("inf") < value < float("inf")) for value in series):
        raise ValueError("Trend values must be finite")

    changes = [
        series[index] - series[index - 1]
        for index in range(1, len(series))
    ]

    if not changes:
        direction = "FLAT"
    elif all(change > 0 for change in changes):
        direction = "UP"
    elif all(change < 0 for change in changes):
        direction = "DOWN"
    elif all(change >= 0 for change in changes):
        direction = "NON_DECREASING"
    elif all(change <= 0 for change in changes):
        direction = "NON_INCREASING"
    else:
        direction = "MIXED"

    peak = max(series)
    trough = min(series)

    return {
        "values": series,
        "direction": direction,
        "change_absolute": series[-1] - series[0],
        "change_percent": (
            (series[-1] - series[0]) / series[0]
            if series[0] != 0
            else None
        ),
        "peak": peak,
        "trough": trough,
        "peak_index": series.index(peak),
        "trough_index": series.index(trough),
        "observations": len(series),
    }
