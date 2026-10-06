"""Deterministic price segmentation."""


def segment(
    records: list[dict],
    price_field: str = "price",
) -> dict:
    prices = [
        float(record[price_field])
        for record in records
        if price_field in record
    ]

    if not prices:
        return {
            "count": 0,
            "low": [],
            "medium": [],
            "high": [],
        }

    ordered = sorted(prices)
    n = len(ordered)

    low_cut = ordered[max(0, int(n * 0.33) - 1)]
    high_index = min(n - 1, max(0, int(n * 0.67)))
    high_cut = ordered[high_index]

    low = []
    medium = []
    high = []

    for record in records:
        if price_field not in record:
            continue

        price = float(record[price_field])

        if price <= low_cut:
            low.append(record)
        elif price >= high_cut:
            high.append(record)
        else:
            medium.append(record)

    return {
        "count": len(prices),
        "low": low,
        "medium": medium,
        "high": high,
        "low_threshold": round(low_cut, 6),
        "high_threshold": round(high_cut, 6),
    }
