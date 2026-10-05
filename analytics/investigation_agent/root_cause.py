"""Deterministic root-cause evaluation."""

from typing import Any


def investigate(
    hypotheses: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    results = []

    for hypothesis in hypotheses:
        hypothesis_id = str(hypothesis.get("hypothesis_id", ""))

        supporting = 0
        contradicting = 0
        weighted_support = 0.0

        for item in evidence:
            supports = {
                str(value)
                for value in item.get("supports", [])
            }
            contradicts = {
                str(value)
                for value in item.get("contradicts", [])
            }

            strength = float(item.get("strength", 0.0))

            if hypothesis_id in supports:
                supporting += 1
                weighted_support += strength

            if hypothesis_id in contradicts:
                contradicting += 1

        total = supporting + contradicting

        score = (
            weighted_support / total
            if total
            else float(hypothesis.get("prior_score", 0.5))
        )

        results.append(
            {
                "hypothesis_id": hypothesis_id,
                "statement": hypothesis.get("statement", ""),
                "supporting_evidence": supporting,
                "contradicting_evidence": contradicting,
                "root_cause_score": round(score, 6),
                "status": (
                    "SUPPORTED"
                    if supporting > contradicting
                    else "CONTRADICTED"
                    if contradicting > supporting
                    else "INCONCLUSIVE"
                ),
            }
        )

    return sorted(
        results,
        key=lambda item: item["root_cause_score"],
        reverse=True,
    )
