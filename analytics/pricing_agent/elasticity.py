"""Deterministic price elasticity analysis."""


def analyze(
    old_price: float,
    new_price: float,
    old_quantity: float,
    new_quantity: float,
) -> dict[str, float | str]:
    old_price = float(old_price)
    new_price = float(new_price)
    old_quantity = float(old_quantity)
    new_quantity = float(new_quantity)

    if old_price == 0 or old_quantity == 0:
        raise ValueError(
            "Old price and old quantity must be non-zero."
        )

    price_change = (
        (new_price - old_price) / old_price
    )

    quantity_change = (
        (new_quantity - old_quantity) / old_quantity
    )

    if price_change == 0:
        elasticity = 0.0
    else:
        elasticity = quantity_change / price_change

    absolute_elasticity = abs(elasticity)

    if absolute_elasticity > 1:
        classification = "ELASTIC"
    elif absolute_elasticity < 1:
        classification = "INELASTIC"
    else:
        classification = "UNIT_ELASTIC"

    return {
        "price_change_rate": round(price_change, 6),
        "quantity_change_rate": round(quantity_change, 6),
        "elasticity": round(elasticity, 6),
        "classification": classification,
    }
