from __future__ import annotations

from typing import Any


def analyze(
    cause_effect: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    drivers = []

    for name, result in cause_effect.items():
        drivers.append(
            {
                "driver": name,
                "correlation": float(result["correlation"]),
                "absolute_correlation": float(
                    result["absolute_correlation"]
                ),
                "direction": result["direction"],
            }
        )

    drivers.sort(
        key=lambda item: item["absolute_correlation"],
        reverse=True,
    )

    return drivers
