from __future__ import annotations

from typing import Any


def build(metrics: dict[str, Any], charts: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(metrics, dict):
        raise TypeError("metrics must be a dictionary")
    if not isinstance(charts, list):
        raise TypeError("charts must be a list")

    return {
        "metrics": metrics,
        "charts": charts,
        "metric_count": len(metrics),
        "chart_count": len(charts),
    }
