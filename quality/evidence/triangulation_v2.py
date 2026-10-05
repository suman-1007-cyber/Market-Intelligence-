from collections import defaultdict


def analyze(facts):
    groups = defaultdict(list)

    for fact in facts:
        key = (
            fact.get("entity"),
            fact.get("metric"),
            fact.get("period"),
            fact.get("geography"),
            fact.get("unit"),
        )
        groups[key].append(fact)

    results = []

    for key, rows in groups.items():
        sources = {
            row.get("source_url")
            for row in rows
            if row.get("source_url")
        }

        values = []

        for row in rows:
            try:
                values.append(float(row["value"]))
            except (KeyError, TypeError, ValueError):
                pass

        unique_values = sorted(set(values))

        if len(unique_values) <= 1:
            status = "corroborated"
        elif len(sources) >= 2:
            status = "conflicting_sources"
        else:
            status = "single_source"

        results.append({
            "key": key,
            "source_count": len(sources),
            "sources": sorted(sources),
            "values": unique_values,
            "status": status,
        })

    return results
