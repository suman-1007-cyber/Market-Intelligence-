from __future__ import annotations

from typing import Any

from .dashboard import build as build_dashboard
from .dashboard_data import build as build_dashboard_data
from .quality import validate_dashboard
from .intelligence import summarize


class VisualizationDashboardAgent:
    agent_id = "visualization-dashboard-agent"

    def analyze(
        self,
        metrics: dict[str, Any],
        charts: list[dict[str, Any]],
    ) -> dict[str, Any]:
        dashboard = build_dashboard_data(metrics, charts)
        validation = validate_dashboard(dashboard)
        summary = summarize(dashboard)

        return {
            "agent_id": self.agent_id,
            "dashboard": dashboard,
            "kpis": build_dashboard(metrics),
            "validation": validation,
            "summary": summary,
        }
