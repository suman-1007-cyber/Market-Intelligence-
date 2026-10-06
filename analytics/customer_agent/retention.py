"""Customer retention analysis."""

from typing import Any


def analyze(
    current_customers: set[str],
    previous_customers: set[str],
) -> dict[str, Any]:
    previous_count = len(previous_customers)
    retained = current_customers & previous_customers

    retained_count = len(retained)

    retention_rate = (
        retained_count / previous_count
        if previous_count
        else 0.0
    )

    return {
        "previous_customers": previous_count,
        "current_customers": len(current_customers),
        "retained_customers": retained_count,
        "retention_rate": round(retention_rate, 6),
        "retained_customer_ids": sorted(retained),
    }
