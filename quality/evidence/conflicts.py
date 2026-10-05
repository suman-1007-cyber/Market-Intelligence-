from collections import defaultdict


def detect(facts, tolerance=0.0):
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

    conflicts = []

    for key, rows in groups.items():
        values = []

        for row in rows:
            try:
                values.append(float(row["value"]))
            except (KeyError, TypeError, ValueError):
                continue

        if len(values) < 2:
            continue

        minimum = min(values)
        maximum = max(values)

        if abs(maximum - minimum) > float(tolerance):
            conflicts.append({
                "key": key,
                "values": values,
                "min": minimum,
                "max": maximum,
                "spread": maximum - minimum,
                "source_count": len(rows),
            })

    return conflicts
