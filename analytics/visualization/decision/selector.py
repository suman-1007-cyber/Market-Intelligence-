def _has_time_dimension(rows):
    return any(
        any(k in row for k in ("period", "date", "year", "month", "time"))
        for row in rows
    )


def _has_numeric_pair(rows):
    numeric = 0
    for row in rows:
        values = []
        for value in row.values():
            try:
                float(value)
                values.append(value)
            except (TypeError, ValueError):
                pass
        if len(values) >= 2:
            numeric += 1
    return numeric >= 2


def _has_category(rows):
    for row in rows:
        for key, value in row.items():
            if key in {"entity", "company", "category", "segment", "product", "region"}:
                if value not in (None, ""):
                    return True
    return False


def _question_type(question):
    q = str(question or "").lower()

    if any(x in q for x in ("correlation", "relationship", "related", "association")):
        return "relationship"

    if any(x in q for x in ("distribution", "spread", "range of", "how are values distributed")):
        return "distribution"

    if any(x in q for x in ("forecast", "actual vs", "prediction", "predicted")):
        return "forecast"

    if any(x in q for x in ("trend", "over time", "growth", "decline", "changed", "change over")):
        return "trend"

    if any(x in q for x in ("rank", "ranking", "highest", "lowest", "top", "bottom", "leader")):
        return "ranking"

    if any(x in q for x in ("share", "composition", "mix", "percentage of total", "breakdown")):
        return "composition"

    if any(x in q for x in ("outlier", "anomaly", "unusual", "exception")):
        return "outlier"

    if any(x in q for x in ("funnel", "conversion", "drop off", "drop-off")):
        return "funnel"

    if any(x in q for x in ("geographic", "geography", "region", "country", "location", "map")):
        return "geographic"

    if any(x in q for x in ("flow", "movement between", "from to", "source to destination")):
        return "flow"

    if any(x in q for x in ("financial movement", "bridge", "waterfall")):
        return "waterfall"

    return "comparison"


def select(question, rows, metric=None):
    rows = list(rows or [])
    intent = _question_type(question)

    has_time = _has_time_dimension(rows)
    has_pair = _has_numeric_pair(rows)
    has_category = _has_category(rows)

    if intent == "relationship" and has_pair:
        primary = "scatter"
        alternatives = ["regression_plot", "correlation_heatmap"]

    elif intent == "distribution":
        primary = "histogram"
        alternatives = ["box_plot", "violin_plot"]

    elif intent == "trend" and has_time:
        primary = "line"
        alternatives = ["area_chart", "moving_average_plot"]

    elif intent == "ranking" and has_category:
        primary = "horizontal_bar"
        alternatives = ["pareto_chart"]

    elif intent == "composition" and has_category:
        primary = "stacked_bar"
        alternatives = ["treemap", "pie"]

    elif intent == "forecast" and has_time:
        primary = "forecast_line"
        alternatives = ["actual_vs_forecast", "residual_plot"]

    elif intent == "outlier":
        primary = "box_plot"
        alternatives = ["scatter", "histogram"]

    elif intent == "funnel":
        primary = "funnel"
        alternatives = ["conversion_bar"]

    elif intent == "geographic":
        primary = "map"
        alternatives = ["regional_bar"]

    elif intent == "flow":
        primary = "sankey"
        alternatives = ["flow_matrix"]

    elif intent == "waterfall":
        primary = "waterfall"
        alternatives = ["bridge_chart"]

    elif has_time:
        primary = "line"
        alternatives = ["bar"]

    elif has_pair:
        primary = "scatter"
        alternatives = ["bar"]

    elif has_category:
        primary = "bar"
        alternatives = ["horizontal_bar"]

    else:
        primary = "table"
        alternatives = ["kpi_cards"]

    return {
        "status": "SELECTED",
        "question_intent": intent,
        "metric": metric,
        "primary_visualization": primary,
        "alternative_visualizations": alternatives,
        "selection_basis": {
            "time_dimension": has_time,
            "numeric_relationship": has_pair,
            "categorical_dimension": has_category,
        },
    }
