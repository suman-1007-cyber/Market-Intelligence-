from pathlib import Path
import json
from collections import defaultdict

INPUT = Path(
    "storage/gold/facts/validated.jsonl"
)

OUTPUT = Path(
    "storage/gold/facts/certified.jsonl"
)

def build():
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not INPUT.exists():
        OUTPUT.write_text(
            "",
            encoding="utf-8"
        )

        return {
            "validated": 0,
            "gold": 0,
            "conflicts": 0
        }

    groups = defaultdict(list)

    with INPUT.open(
        encoding="utf-8"
    ) as source:

        for line in source:
            if not line.strip():
                continue

            row = json.loads(line)

            metric = (
                row.get("semantic_metrics")
                or [row.get("metric")]
            )[0]

            key = (
                metric,
                row.get("normalized_unit"),
                row.get("detected_period"),
                row.get("detected_geography")
            )

            groups[key].append(row)

    gold = []
    conflicts = 0

    for key, rows in groups.items():
        values = [
            r.get("normalized_value")
            for r in rows
            if isinstance(
                r.get("normalized_value"),
                (int, float)
            )
        ]

        if not values:
            continue

        minimum = min(values)
        maximum = max(values)

        if (
            len(values) > 1
            and minimum != 0
        ):
            spread = (
                abs(maximum - minimum)
                / abs(minimum)
            )
        else:
            spread = 0.0

        agreement = spread <= 0.10

        if not agreement:
            conflicts += 1

        best = max(
            rows,
            key=lambda x: (
                float(
                    x.get(
                        "confidence",
                        0
                    )
                ),
                float(
                    x.get(
                        "relevance_score",
                        0
                    )
                )
            )
        )

        record = dict(best)

        record["gold_metric"] = key[0]
        record["source_count"] = len(rows)
        record["min_value"] = minimum
        record["max_value"] = maximum
        record["relative_spread"] = spread
        record["cross_source_agreement"] = agreement

        if agreement:
            record["gold_status"] = "certified"
            gold.append(record)
        else:
            record["gold_status"] = "conflict"

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as target:

        for row in gold:
            target.write(
                json.dumps(
                    row,
                    ensure_ascii=False
                ) + "\n"
            )

    return {
        "validated": sum(
            len(x)
            for x in groups.values()
        ),
        "gold": len(gold),
        "conflicts": conflicts
    }
