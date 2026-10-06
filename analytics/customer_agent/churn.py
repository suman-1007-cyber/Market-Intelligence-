"""Deterministic customer churn analysis."""

from typing import Any


def analyze(
    current_customers: set[str],
    previous_customers: set[str],
) -> dict[str, Any]:
    if not previous_customers:
        return {
            "churned_customers": 0,
            "churn_rate": 0.0,
            "churned_customer_ids": [],
        }

    churned = previous_customers - current_customers

    churn_rate = len(churned) / len(previous_customers)

    return {
        "churned_customers": len(churned),
        "churn_rate": round(churn_rate, 6),
        "churned_customer_ids": sorted(churned),
    }
