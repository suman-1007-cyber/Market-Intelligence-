from pathlib import Path
import json

from quality.evidence.relevance import relevance_score
from semantic.validation.period import detect as detect_period
from semantic.validation.geography import detect as detect_geography
from semantic.validation.entity import detect as detect_entity
from semantic.validation.units import validate as validate_units

INPUT = Path(
    "evidence/metrics/normalized.jsonl"
)

OUTPUT = Path(
    "storage/gold/facts/validated.jsonl"
)

def validate_all():
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
            "input": 0,
            "validated": 0,
            "rejected": 0
        }

    accepted = []
    total = 0

    with INPUT.open(
        encoding="utf-8"
    ) as source:

        for line in source:
            if not line.strip():
                continue

            total += 1

            row = json.loads(line)

            relevance = relevance_score(row)
            units = validate_units(row)

            text = row.get(
                "claim",
                ""
            )

            period = detect_period(text)
            geography = detect_geography(text)
            entities = detect_entity(text)

            row["semantic_metrics"] = (
                relevance["metrics"]
            )

            row["relevance_score"] = (
                relevance["score"]
            )

            row["detected_period"] = period

            row["detected_geography"] = (
                geography[0]
                if geography
                else row.get("geography")
            )

            row["detected_entities"] = entities

            row["unit_validation"] = units

            strong_metric = bool(
                relevance["metrics"]
            )

            strong_source = (
                float(
                    row.get(
                        "confidence",
                        0
                    )
                ) >= 0.70
            )

            if (
                strong_metric
                and units["valid"]
                and relevance["score"] >= 0.65
                and strong_source
            ):
                row["quality_status"] = "validated"
                accepted.append(row)

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as target:

        for row in accepted:
            target.write(
                json.dumps(
                    row,
                    ensure_ascii=False
                ) + "\n"
            )

    return {
        "input": total,
        "validated": len(accepted),
        "rejected": total - len(accepted)
    }
