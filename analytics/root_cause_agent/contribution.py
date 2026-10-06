from __future__ import annotations

from typing import Any


def analyze(
    target: list[float],
    drivers: dict[str, list[float]],
) -> dict[str, dict[str, Any]]:
    if not target:
        raise ValueError("target must not be empty")

    target_change = target[-1] - target[0]

    results = {}

    for name, values in drivers.items():
        if len(values) != len(target):
            raise ValueError(
                f"driver '{name}' must have the same length as target"
            )

        change = values[-1] - values[0]

        if target_change == 0:
            contribution = 0.0
        else:
            contribution = abs(change) / abs(target_change)

        results[str(name)] = {
            "change": change,
            "contribution": contribution,
        }

    return results
