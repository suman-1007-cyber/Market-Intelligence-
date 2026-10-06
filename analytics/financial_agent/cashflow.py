"""Cash flow analysis."""

from typing import Any


def analyze(
    cash_inflow: float,
    cash_outflow: float,
) -> dict[str, Any]:
    inflow = float(cash_inflow)
    outflow = float(cash_outflow)

    net_cash_flow = inflow - outflow

    coverage_ratio = (
        inflow / outflow
        if outflow
        else float("inf")
    )

    return {
        "cash_inflow": inflow,
        "cash_outflow": outflow,
        "net_cash_flow": round(net_cash_flow, 6),
        "positive": net_cash_flow >= 0,
        "coverage_ratio": (
            round(coverage_ratio, 6)
            if outflow
            else None
        ),
    }
