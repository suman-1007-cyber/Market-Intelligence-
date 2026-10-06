from __future__ import annotations

from typing import Any, Iterable


def detect(values: Iterable[float], period: int = 0) -> dict[str, Any]:
    series = [float(value) for value in values]

    if period < 0:
        raise ValueError("period must be non-negative")

    if period == 0 or len(series) < period * 2:
        return {
            "detected": False,
            "period": None,
            "strength": 0.0,
        }

    groups = []
    for offset in range(period):
        group = series[offset::period]
        if group:
            groups.append(group)

    if not groups:
        return {
            "detected": False,
            "period": None,
            "strength": 0.0,
        }

    group_means = [sum(group) / len(group) for group in groups]
    overall = sum(series) / len(series)

    variation = sum(abs(value - overall) for value in group_means)
    scale = sum(abs(value) for value in series) / len(series)

    strength = variation / (scale * period) if scale != 0 else 0.0
    strength = max(0.0, min(1.0, strength))

    return {
        "detected": strength > 0.10,
        "period": period if strength > 0.10 else None,
        "strength": strength,
    }
