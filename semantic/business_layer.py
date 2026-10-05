
DEFINITIONS = {
    "growth_rate": {
        "domain": "market",
        "type": "rate",
        "unit": "percent"
    },
    "percentage": {
        "domain": "market",
        "type": "percentage",
        "unit": "percent"
    }
}

def build(facts):
    metrics = {}

    for fact in facts:
        metric = fact.get("metric")

        if metric not in DEFINITIONS:
            continue

        metrics.setdefault(metric, []).append({
            "value": fact["normalized_value"],
            "unit": fact["normalized_unit"],
            "source_url": fact["source_url"],
            "confidence": fact["confidence"],
            "triangulation_status": fact.get(
                "triangulation_status",
                "SINGLE_SOURCE"
            )
        })

    return {
        "definitions": DEFINITIONS,
        "metrics": metrics,
        "fact_count": len(facts)
    }
