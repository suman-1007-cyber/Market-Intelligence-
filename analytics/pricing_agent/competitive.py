"""Competitive pricing intelligence."""


def analyze(
    own_price: float,
    competitor_prices: list[float],
) -> dict[str, float | str | None]:
    own_price = float(own_price)

    prices = [
        float(price)
        for price in competitor_prices
    ]

    if not prices:
        return {
            "own_price": own_price,
            "competitor_average": None,
            "price_gap": None,
            "price_gap_rate": None,
            "position": "UNKNOWN",
        }

    average = sum(prices) / len(prices)
    gap = own_price - average

    gap_rate = (
        gap / average
        if average != 0
        else 0.0
    )

    if gap_rate > 0.05:
        position = "PREMIUM"
    elif gap_rate < -0.05:
        position = "DISCOUNT"
    else:
        position = "PARITY"

    return {
        "own_price": own_price,
        "competitor_average": round(average, 6),
        "price_gap": round(gap, 6),
        "price_gap_rate": round(gap_rate, 6),
        "position": position,
    }
