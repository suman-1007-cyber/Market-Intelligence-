
from collections import defaultdict

def run(facts):
    groups = defaultdict(list)

    for fact in facts:
        groups[
            (
                fact.get("metric"),
                fact.get("normalized_value"),
                fact.get("normalized_unit")
            )
        ].append(fact)

    result = []

    for rows in groups.values():
        sources = sorted({
            r.get("source_url")
            for r in rows
            if r.get("source_url")
        })

        fact = dict(rows[0])
        fact["supporting_sources"] = len(sources)
        fact["supporting_source_urls"] = sources
        fact["triangulation_status"] = (
            "MULTI_SOURCE" if len(sources) >= 2
            else "SINGLE_SOURCE"
        )

        result.append(fact)

    return result
