from __future__ import annotations

from typing import Any


def summarize(dashboard: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(dashboard, dict):
        raise TypeError("dashboard must be a dictionary")

    metrics = dashboard.get("metrics", {})
    charts = dashboard.get("charts", [])

    return {
        "metric_count": len(metrics) if isinstance(metrics, dict) else 0,
        "chart_count": len(charts) if isinstance(charts, list) else 0,
        "has_visuals": bool(charts),
    }
