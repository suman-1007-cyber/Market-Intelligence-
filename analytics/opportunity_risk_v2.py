def analyze(trends=None, forecasts=None):
    trends = trends or {}
    forecasts = forecasts or {}

    opportunities = []
    risks = []

    for metric, data in trends.items():
        change = data.get("change_pct")

        if change is not None:
            if change >= 10:
                opportunities.append({
                    "metric": metric,
                    "reason": "growth",
                    "change_pct": change,
                })

            elif change <= -10:
                risks.append({
                    "metric": metric,
                    "reason": "decline",
                    "change_pct": change,
                })

    for metric, data in forecasts.items():
        slope = data.get("slope")

        if slope is None:
            continue

        if slope > 0:
            opportunities.append({
                "metric": metric,
                "reason": "positive_forecast_trend",
                "slope": slope,
            })

        elif slope < 0:
            risks.append({
                "metric": metric,
                "reason": "negative_forecast_trend",
                "slope": slope,
            })

    return {
        "opportunities": opportunities,
        "risks": risks,
    }
