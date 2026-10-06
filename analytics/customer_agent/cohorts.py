"""Deterministic customer cohort analysis."""

from collections import defaultdict
from typing import Any


def analyze(
    records: list[dict[str, Any]],
    customer_field: str = "customer",
    cohort_field: str = "cohort",
) -> list[dict[str, Any]]:
    groups: dict[str, set[str]] = defaultdict(set)

    for record in records:
        customer = str(record.get(customer_field, "")).strip()
        cohort = str(record.get(cohort_field, "")).strip()

        if customer and cohort:
            groups[cohort].add(customer)

    return [
        {
            "cohort": cohort,
            "customers": len(customers),
        }
        for cohort, customers in sorted(groups.items())
    ]
