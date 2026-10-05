from collections import defaultdict


def analyze(facts):
    grouped = defaultdict(list)

    for fact in facts:
        metric = fact.get("metric")
        period = fact.get("period")
        value = fact.get("value")

        if metric and period is not None and value is not None:
            try:
                grouped[metric].append(
                    (str(period), float(value))
                )
            except (TypeError, ValueError):
                pass

    result = {}

    for metric, rows in grouped.items():
        rows.sort(key=lambda x: x[0])

        values = [value for _, value in rows]

        if len(values) < 2:
            direction = "insufficient_data"
            change_pct = None
        else:
            first = values[0]
            last = values[-1]

            if first == 0:
                change_pct = None
            else:
                change_pct = ((last - first) / abs(first)) * 100

            if last > first:
                direction = "up"
            elif last < first:
                direction = "down"
            else:
                direction = "flat"

        result[metric] = {
            "observations": len(rows),
            "direction": direction,
            "change_pct": change_pct,
            "series": [
                {"period": period, "value": value}
                for period, value in rows
            ],
        }

    return result
