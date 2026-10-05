def build(facts):
    points = []

    for fact in facts:
        if fact.get("value") is None:
            continue

        try:
            value = float(fact["value"])
        except (TypeError, ValueError):
            continue

        points.append({
            "x": fact.get("period"),
            "y": value,
            "series": fact.get("metric"),
            "metric": fact.get("metric"),
            "unit": fact.get("unit"),
            "source_url": fact.get("source_url"),
            "confidence": fact.get("confidence"),
        })

    return points
