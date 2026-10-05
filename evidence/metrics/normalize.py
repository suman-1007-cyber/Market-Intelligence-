from pathlib import Path
import json
import re

INPUT = Path(
    "evidence/claims/claims.jsonl"
)

OUTPUT = Path(
    "evidence/metrics/normalized.jsonl"
)

UNIT_MULTIPLIER = {
    "million": 1_000_000,
    "billion": 1_000_000_000,
    "trillion": 1_000_000_000_000,
    "crore": 10_000_000,
    "lakh": 100_000
}

def normalize(claim):
    value = claim.get("value")

    if value is None:
        return claim

    unit = claim.get("unit")

    if unit in UNIT_MULTIPLIER:
        claim["normalized_value"] = (
            value * UNIT_MULTIPLIER[unit]
        )
        claim["normalized_unit"] = "absolute"

    elif unit == "percent":
        claim["normalized_value"] = value / 100.0
        claim["normalized_unit"] = "ratio"

    else:
        claim["normalized_value"] = value
        claim["normalized_unit"] = unit

    return claim

def run():
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not INPUT.exists():
        OUTPUT.write_text(
            "",
            encoding="utf-8"
        )
        return 0

    count = 0

    with INPUT.open(
        encoding="utf-8"
    ) as source, OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as target:

        for line in source:
            if not line.strip():
                continue

            claim = json.loads(line)
            claim = normalize(claim)

            target.write(
                json.dumps(
                    claim,
                    ensure_ascii=False
                ) + "\n"
            )

            count += 1

    return count
