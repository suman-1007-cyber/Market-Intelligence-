from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.visualization_agent.dashboard import build
from analytics.visualization_agent.layout import arrange
from analytics.visualization_agent.formatting import format_number, format_percent
from analytics.visualization_agent.charts import prepare
from analytics.visualization_agent.evidence_links import link_visualization
from analytics.visualization_agent.dashboard_data import build as build_data
from analytics.visualization_agent.quality import validate_dashboard
from analytics.visualization_agent.intelligence import summarize
from analytics.visualization_agent.agent import VisualizationDashboardAgent


metrics = {
    "revenue": 125000,
    "growth_rate": 0.20,
    "customers": 500,
}

kpis = build(metrics)
assert kpis["kpi_count"] == 3

layout = arrange([
    {"id": "market", "title": "Market"},
    {"id": "competitive", "title": "Competitive"},
])
assert layout["section_count"] == 2
assert layout["sections"][1]["order"] == 1

assert format_number(1250.5) == "1,250.50"
assert format_percent(0.25) == "25.0%"

chart = prepare("line", [{"period": "Q1", "value": 100}])
assert chart["chart_type"] == "line"
assert chart["rows"] == 1

linked = link_visualization(chart, [{"source": "source-a"}])
assert linked["traceable"] is True
assert linked["evidence_count"] == 1

dashboard = build_data(metrics, [chart])
assert dashboard["metric_count"] == 3
assert dashboard["chart_count"] == 1

quality = validate_dashboard(dashboard)
assert quality["valid"] is True
assert quality["missing"] == []

summary = summarize(dashboard)
assert summary["metric_count"] == 3
assert summary["chart_count"] == 1
assert summary["has_visuals"] is True

result = VisualizationDashboardAgent().analyze(metrics, [chart])
assert result["agent_id"] == "visualization-dashboard-agent"
assert result["validation"]["valid"] is True

print("161 Visualization Dashboard Data : PASS")
print("162 Dashboard KPI Engine         : PASS")
print("163 Dashboard Layout Engine      : PASS")
print("164 Visualization Formatting     : PASS")
print("165 Chart Preparation             : PASS")
print("166 Evidence-linked Visualization : PASS")
print("167 Dashboard Quality             : PASS")
print("168 Dashboard Intelligence        : PASS")
print("169 Visualization Integration    : PASS")
print("170 Visualization Dashboard Agent : PASS")
print("MILESTONE 161-170 : PASS")
