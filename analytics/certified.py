
from collections import defaultdict

def market(facts):
    metrics = defaultdict(list)

    for fact in facts:
        metrics[fact.get("metric")].append({
            "value": fact.get("normalized_value"),
            "unit": fact.get("normalized_unit"),
            "source": fact.get("source_url")
        })

    return {
        "engine": "market",
        "metrics": dict(metrics),
        "fact_count": len(facts)
    }

def competitive(facts):
    entities = defaultdict(list)

    for fact in facts:
        entities[
            fact.get("entity_id", "unknown")
        ].append(fact)

    return {
        "engine": "competitive",
        "entities": dict(entities),
        "fact_count": len(facts)
    }

def customer(facts):
    return {
        "engine": "customer",
        "facts": list(facts),
        "fact_count": len(facts)
    }

def run(facts):
    return {
        "market": market(facts),
        "competitive": competitive(facts),
        "customer": customer(facts)
    }
