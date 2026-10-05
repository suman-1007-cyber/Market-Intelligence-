"""Deterministic investigation synthesis."""

from typing import Any


def synthesize(
    question: str,
    root_causes: list[dict[str, Any]],
    cross_source: dict[str, Any],
) -> dict[str, Any]:
    ranked = list(root_causes)

    conclusion = None

    if ranked:
        top = ranked[0]

        if top["status"] == "SUPPORTED":
            conclusion = top["statement"]
        else:
            conclusion = "No root cause has sufficient supporting evidence."

    confidence = 0.0

    if ranked:
        confidence = float(ranked[0]["root_cause_score"])

    if cross_source.get("multi_source_claims", 0) > 0:
        confidence = min(1.0, confidence + 0.1)

    return {
        "question": question,
        "conclusion": conclusion,
        "confidence": round(confidence, 6),
        "root_causes": ranked,
        "cross_source_confirmation": int(
            cross_source.get("multi_source_claims", 0)
        ),
    }
