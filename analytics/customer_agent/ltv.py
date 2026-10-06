"""Deterministic customer lifetime value."""

from typing import Any


def calculate(
    revenue: float,
    gross_margin: float = 1.0,
    retention_rate: float = 1.0,
    periods: int = 1,
) -> dict[str, Any]:
    revenue_value = max(0.0, float(revenue))
    margin = max(0.0, min(1.0, float(gross_margin)))
    retention = max(0.0, min(0.999999, float(retention_rate)))
    period_count = max(1, int(periods))

    if retention == 1.0:
        lifetime = float(period_count)
    else:
        lifetime = sum(
            retention ** index
            for index in range(period_count)
        )

    ltv = revenue_value * margin * lifetime

    return {
        "revenue": revenue_value,
        "gross_margin": margin,
        "retention_rate": retention,
        "periods": period_count,
        "expected_lifetime": round(lifetime, 6),
        "ltv": round(ltv, 6),
    }
