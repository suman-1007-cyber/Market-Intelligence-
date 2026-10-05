"""Deterministic market sizing and growth analysis."""

from typing import Any


def analyze(
    market_size: float,
    previous_size: float | None = None,
    period: str | None = None,
) -> dict[str, Any]:
    size = float(market_size)

    if size < 0:
        raise ValueError("Market size cannot be negative")

    result: dict[str, Any] = {
        "market_size": size,
        "period": period,
        "growth_rate": None,
        "growth_absolute": None,
    }

    if previous_size is not None:
        previous = float(previous_size)

        if previous < 0:
            raise ValueError("Previous market size cannot be negative")

        result["growth_absolute"] = size - previous

        if previous != 0:
            result["growth_rate"] = (size - previous) / previous

    return result
