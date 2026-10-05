def analyze(facts):
    customer_metrics = {}

    for fact in facts:
        metric = str(fact.get("metric", "")).lower()

        if "customer" in metric or "retention" in metric or "churn" in metric:
            customer_metrics.setdefault(metric, []).append(fact)

    return {
        "metrics": customer_metrics,
        "metric_count": len(customer_metrics),
    }
