from collections import defaultdict


def analyze(facts):
    grouped = defaultdict(list)
    for fact in facts:
        metric = fact.get("metric")
        if metric:
            grouped[metric].append(fact)

    return {
        "metrics": {
            metric: {
                "count": len(rows),
                "values": [r.get("value") for r in rows],
                "unit": rows[0].get("unit"),
            }
            for metric, rows in grouped.items()
        }
    }
