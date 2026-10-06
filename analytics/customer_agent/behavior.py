"""Deterministic customer behavior intelligence."""

from typing import Any


def analyze(
    profile: dict[str, Any],
    previous_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    revenue = max(0.0, float(profile.get("revenue", 0.0)))
    orders = max(0, int(profile.get("orders", 0)))

    average_order_value = (
        revenue / orders
        if orders
        else 0.0
    )

    result = {
        "customer": profile.get("customer"),
        "revenue": revenue,
        "orders": orders,
        "average_order_value": round(
            average_order_value,
            6,
        ),
    }

    if previous_profile is not None:
        previous_revenue = max(
            0.0,
            float(previous_profile.get("revenue", 0.0)),
        )

        if previous_revenue:
            change = (
                (revenue - previous_revenue)
                / previous_revenue
            )
        else:
            change = 0.0

        result["revenue_change"] = round(change, 6)

        if change > 0:
            result["behavior"] = "GROWING"
        elif change < 0:
            result["behavior"] = "DECLINING"
        else:
            result["behavior"] = "STABLE"
    else:
        result["behavior"] = "BASELINE"

    return result
