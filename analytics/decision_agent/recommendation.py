"""Deterministic recommendation engine."""

from typing import Any


def recommend(
    ranked: list[dict[str, Any]],
    minimum_score: float = 0.60,
) -> dict[str, Any]:
    if not ranked:
        return {
            "recommendation": None,
            "score": None,
            "status": "NO_DECISION",
            "reason": "No evaluated alternatives.",
        }

    threshold = max(0.0, min(1.0, float(minimum_score)))
    best = ranked[0]
    score = float(best.get("score", 0.0))

    if score >= threshold:
        status = "RECOMMENDED"
        reason = "Top alternative meets the decision threshold."
    else:
        status = "INSUFFICIENT"
        reason = "Top alternative does not meet the decision threshold."

    return {
        "recommendation": best["name"],
        "score": score,
        "status": status,
        "threshold": threshold,
        "reason": reason,
    }
