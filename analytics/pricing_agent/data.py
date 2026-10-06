"""Pricing data normalization."""

from typing import Any

NUMERIC_FIELDS = (
    "price",
    "cost",
    "units",
    "revenue",
    "discount",
    "competitor_price",
)


def normalize(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)

    for field in NUMERIC_FIELDS:
        if field not in result:
            continue

        try:
            result[field] = float(result[field])
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid numeric value for '{field}'."
            ) from exc

    return result


def normalize_many(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [normalize(record) for record in records]
