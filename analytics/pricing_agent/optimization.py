"""Deterministic price optimization."""

from typing import Any


def optimize(
    current_price: float,
    cost: float,
    candidate_prices: list[float],
    expected_units: list[float],
) -> dict[str, Any]:
    current_price = float(current_price)
    cost = float(cost)

    if len(candidate_prices) != len(expected_units):
        raise ValueError(
            "candidate_prices and expected_units must have equal length."
        )

    if not candidate_prices:
        raise ValueError("At least one candidate price is required.")

    candidates = []

    for price, units in zip(candidate_prices, expected_units):
        price = float(price)
        units = float(units)

        if price < 0 or units < 0:
            raise ValueError(
                "Candidate prices and units cannot be negative."
            )

        revenue = price * units
        profit = (price - cost) * units

        candidates.append(
            {
                "price": price,
                "expected_units": units,
                "revenue": round(revenue, 6),
                "profit": round(profit, 6),
            }
        )

    best = max(
        candidates,
        key=lambda item: item["profit"],
    )

    return {
        "current_price": current_price,
        "cost": cost,
        "candidates": candidates,
        "recommended_price": best["price"],
        "recommended_profit": best["profit"],
        "optimization_basis": "EXPECTED_PROFIT",
    }
