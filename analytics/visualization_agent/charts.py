from __future__ import annotations

from typing import Any


SUPPORTED = {
    "line",
    "bar",
    "scatter",
    "pie",
    "histogram",
    "box_plot",
    "heatmap",
    "funnel",
    "waterfall",
    "treemap",
}


def prepare(chart_type: str, data: list[dict[str, Any]]) -> dict[str, Any]:
    chart_type = str(chart_type).lower().strip()

    if chart_type not in SUPPORTED:
        raise ValueError(f"unsupported chart type: {chart_type}")

    if not isinstance(data, list):
        raise TypeError("data must be a list")

    return {
        "chart_type": chart_type,
        "rows": len(data),
        "data": data,
    }
