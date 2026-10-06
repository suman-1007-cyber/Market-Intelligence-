from __future__ import annotations

from typing import Any, Iterable


def prepare(
    target: Iterable[float],
    drivers: dict[str, Iterable[float]],
) -> dict[str, Any]:
    target_values = [float(value) for value in target]

    if not target_values:
        raise ValueError("target must not be empty")

    prepared_drivers: dict[str, list[float]] = {}

    for name, values in drivers.items():
        driver_values = [float(value) for value in values]

        if len(driver_values) != len(target_values):
            raise ValueError(
                f"driver '{name}' must have the same length as target"
            )

        prepared_drivers[str(name)] = driver_values

    return {
        "target": target_values,
        "drivers": prepared_drivers,
        "rows": len(target_values),
        "driver_count": len(prepared_drivers),
    }
