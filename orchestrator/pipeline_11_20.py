import json
from pathlib import Path

from analytics.market_engine_v2 import analyze as market_analyze
from analytics.competitive_engine_v2 import analyze as competitive_analyze
from analytics.customer_engine_v2 import analyze as customer_analyze
from analytics.business_dimensions_v2 import analyze as dimensions_analyze
from analytics.trends_v2 import analyze as trends_analyze
from analytics.forecasting_v2 import forecast
from analytics.scenarios_v2 import scenario
from analytics.opportunity_risk_v2 import analyze as opportunity_analyze
from visualization.graph_data_v2 import build as graph_build
from visualization.evidence_svg_v2 import build as svg_build


def run(facts):
    market = market_analyze(facts)
    competitive = competitive_analyze(facts)
    customer = customer_analyze(facts)
    dimensions = dimensions_analyze(facts)

    trends = trends_analyze(facts)

    forecasts = {}

    for metric, data in trends.items():
        values = [
            point["value"]
            for point in data.get("series", [])
        ]

        forecasts[metric] = forecast(values, periods=2)

    scenarios = {}

    for fact in facts:
        metric = fact.get("metric")
        value = fact.get("value")

        if metric and value is not None:
            try:
                scenarios[metric] = scenario(
                float(value),
                {
                    "base": 0.0,
                    "upside": 0.10,
                    "downside": -0.10,
                },
            )
            except (TypeError, ValueError):
                pass

    opportunity_risk = opportunity_analyze(
        trends,
        forecasts,
    )

    graph_points = graph_build(facts)

    svg = svg_build(
        graph_points,
        title="Certified Evidence Analysis",
    )

    return {
        "market": market,
        "competitive": competitive,
        "customer": customer,
        "business_dimensions": dimensions,
        "trends": trends,
        "forecasts": forecasts,
        "scenarios": scenarios,
        "opportunity_risk": opportunity_risk,
        "graph_data": graph_points,
        "svg": svg,
    }


def save(result):
    gold_path = Path("storage/gold/pipeline_11_20.json")
    svg_path = Path("reports/certified_evidence_chart.svg")

    gold_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.parent.mkdir(parents=True, exist_ok=True)

    output = dict(result)
    output.pop("svg", None)

    gold_path.write_text(
        json.dumps(output, indent=2, default=str),
        encoding="utf-8",
    )

    svg_path.write_text(
        result["svg"],
        encoding="utf-8",
    )

    return gold_path, svg_path
