"""Decision criteria validation and scoring."""

from typing import Any


def validate_criteria(
    criteria: dict[str, float],
) -> dict[str, Any]:
    if not criteria:
        return {
            "valid": False,
            "errors": ["No decision criteria supplied."],
        }

    errors = []

    for name, weight in criteria.items():
        if not str(name).strip():
            errors.append("Criterion name cannot be empty.")

        try:
            numeric_weight = float(weight)
        except (TypeError, ValueError):
            errors.append(
                f"Criterion '{name}' has a non-numeric weight."
            )
            continue

        if numeric_weight < 0:
            errors.append(
                f"Criterion '{name}' has a negative weight."
            )

    if sum(float(weight) for weight in criteria.values()) <= 0:
        errors.append("Total criterion weight must be positive.")

    return {
        "valid": not errors,
        "errors": errors,
        "criterion_count": len(criteria),
        "total_weight": sum(
            float(weight)
            for weight in criteria.values()
        ),
    }


def rank(
    evaluated: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return sorted(
        evaluated,
        key=lambda item: float(item.get("score", 0.0)),
        reverse=True,
    )
