"""Deterministic discount and promotion analysis."""

from typing import Any


def analyze(
    list_price: float,
    selling_price: float,
    units: float = 0.0,
) -> dict[str, Any]:
    list_price = float(list_price)
    selling_price = float(selling_price)
    units = float(units)

    if list_price < 0 or selling_price < 0:
        raise ValueError("Prices cannot be negative.")

    discount_value = list_price - selling_price

    discount_rate = (
        discount_value / list_price
        if list_price != 0
        else 0.0
    )

    revenue = selling_price * units

    if discount_rate > 0:
        promotion_status = "DISCOUNTED"
    else:
        promotion_status = "FULL_PRICE"

    return {
        "list_price": list_price,
        "selling_price": selling_price,
        "units": units,
        "discount_value": round(discount_value, 6),
        "discount_rate": round(discount_rate, 6),
        "revenue": round(revenue, 6),
        "promotion_status": promotion_status,
    }
