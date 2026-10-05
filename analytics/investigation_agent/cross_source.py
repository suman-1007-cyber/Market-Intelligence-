"""Cross-source evidence comparison."""

from collections import defaultdict
from typing import Any


def compare(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for item in evidence:
        claim = str(item.get("claim", "")).strip().lower()
        if claim:
            groups[claim].append(item)

    comparisons = []

    for claim, rows in groups.items():
        sources = sorted(
            {
                str(row.get("source", "")).strip()
                for row in rows
                if str(row.get("source", "")).strip()
            }
        )

        strength_values = [
            float(row.get("strength", 0.0))
            for row in rows
        ]

        comparisons.append(
            {
                "claim": claim,
                "source_count": len(sources),
                "sources": sources,
                "evidence_count": len(rows),
                "average_strength": (
                    sum(strength_values) / len(strength_values)
                    if strength_values
                    else 0.0
                ),
                "cross_source_confirmed": len(sources) >= 2,
            }
        )

    return {
        "claims": comparisons,
        "multi_source_claims": sum(
            1
            for item in comparisons
            if item["cross_source_confirmed"]
        ),
    }
