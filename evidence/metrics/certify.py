from pathlib import Path
import json
from collections import defaultdict

INPUT = Path(
    "evidence/metrics/normalized.jsonl"
)

OUTPUT = Path(
    "evidence/metrics/certified.jsonl"
)

def certify():
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
            "records": 0,
            "certified": 0,
            "conflicts": 0
        }

    groups = defaultdict(list)

    with INPUT.open(
        encoding="utf-8"
    ) as f:
        for line in f:
            if not line.strip():
                continue

            row = json.loads(line)

            key = (
                row.get("metric"),
                row.get("normalized_unit"),
                row.get("period"),
                row.get("geography"),
                row.get("entity")
            )

            groups[key].append(row)

    certified = []
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

        if len(values) > 1 and minimum != 0:
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
            key=lambda x: x.get(
                "confidence",
                0
            )
        )

        record = dict(best)

        record["source_count"] = len(rows)
        record["min_value"] = minimum
        record["max_value"] = maximum
        record["relative_spread"] = spread
        record["triangulated"] = agreement
        record["certification_status"] = (
            "certified"
            if agreement
            else "conflict"
        )

        certified.append(record)

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:
        for row in certified:
            f.write(
                json.dumps(
                    row,
                    ensure_ascii=False
                ) + "\n"
            )

    return {
        "records": sum(
            len(x)
            for x in groups.values()
        ),
        "certified": len(
            [
                x for x in certified
                if x["certification_status"]
                == "certified"
            ]
        ),
        "conflicts": conflicts
    }
