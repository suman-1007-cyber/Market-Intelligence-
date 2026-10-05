"""Deterministic decision engine."""

from typing import Any


def evaluate(
    alternatives: list[dict[str, Any]],
    criteria: dict[str, float],
) -> list[dict[str, Any]]:
    if not alternatives:
        raise ValueError("Alternatives cannot be empty")

    if not criteria:
        raise ValueError("Criteria cannot be empty")

    total_weight = sum(float(weight) for weight in criteria.values())

    if total_weight <= 0:
        raise ValueError("Criterion weights must have positive total")

    results = []

    for alternative in alternatives:
        name = str(alternative.get("name", "")).strip()

        if not name:
            raise ValueError("Every alternative requires a name")

        weighted_score = 0.0
        criterion_scores = {}

        for criterion, weight in criteria.items():
            raw = float(alternative.get(criterion, 0.0))
            score = max(0.0, min(1.0, raw))

            criterion_scores[criterion] = score
            weighted_score += score * float(weight)

        normalized = weighted_score / total_weight

        results.append(
            {
                "name": name,
                "criteria": criterion_scores,
                "score": round(normalized, 6),
            }
        )

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )
