from pathlib import Path
import json
import re

INPUT = Path(
    "evidence/metrics/certified.jsonl"
)

OUTPUT = Path(
    "evidence/entities/resolved.jsonl"
)

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "market",
    "industry",
    "company",
    "companies",
    "technology",
    "india"
}

def candidates(text):
    words = re.findall(
        r"\b[A-Z][A-Za-z0-9&.-]{2,}\b",
        text or ""
    )

    output = []

    for word in words:
        if word.lower() not in STOPWORDS:
            if word not in output:
                output.append(word)

    return output[:10]

def resolve():
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

            row = json.loads(line)

            if not row.get("entity"):
                names = candidates(
                    row.get("claim", "")
                )

                if names:
                    row["entity_candidates"] = names

            target.write(
                json.dumps(
                    row,
                    ensure_ascii=False
                ) + "\n"
            )

            count += 1

    return count
