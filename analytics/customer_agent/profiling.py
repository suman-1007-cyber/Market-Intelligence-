"""Customer profile aggregation."""

from collections import defaultdict
from typing import Any


def profile(
    records: list[dict[str, Any]],
    customer_field: str = "customer",
) -> list[dict[str, Any]]:
    customers: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "orders": 0,
            "units": 0.0,
        }
    )

    for record in records:
        customer = str(record.get(customer_field, "")).strip()

        if not customer:
            continue

        try:
            revenue = float(record.get("revenue", 0.0))
        except (TypeError, ValueError):
            revenue = 0.0

        try:
            units = float(record.get("units", 0.0))
        except (TypeError, ValueError):
            units = 0.0

        customers[customer]["revenue"] += revenue
        customers[customer]["orders"] += 1
        customers[customer]["units"] += units

    results = []

    for customer, values in customers.items():
        revenue = values["revenue"]
        orders = values["orders"]

        results.append(
            {
                "customer": customer,
                "revenue": round(revenue, 6),
                "orders": orders,
                "units": round(values["units"], 6),
                "average_order_value": (
                    round(revenue / orders, 6)
                    if orders
                    else 0.0
                ),
            }
        )

    return sorted(
        results,
        key=lambda item: item["revenue"],
        reverse=True,
    )
