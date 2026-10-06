"""Deterministic price analysis."""

from typing import Any


def analyze(
    price: float,
    cost: float = 0.0,
    units: float = 0.0,
) -> dict[str, Any]:
    price = float(price)
    cost = float(cost)
    units = float(units)

    margin_value = price - cost

    margin_rate = (
        margin_value / price
        if price != 0
        else 0.0
    )

    revenue = price * units

    return {
        "price": price,
        "cost": cost,
        "units": units,
        "margin_value": round(margin_value, 6),
        "margin_rate": round(margin_rate, 6),
        "revenue": round(revenue, 6),
    }
