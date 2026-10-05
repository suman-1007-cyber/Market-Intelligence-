"""Market intelligence synthesis."""

from typing import Any


def synthesize(
    sizing: dict[str, Any],
    trend: dict[str, Any],
    opportunity: dict[str, Any],
) -> dict[str, Any]:
    findings: list[str] = []

    growth = sizing.get("growth_rate")

    if growth is not None:
        if growth > 0:
            findings.append("Market size is growing.")
        elif growth < 0:
            findings.append("Market size is declining.")
        else:
            findings.append("Market size is unchanged.")

    direction = trend.get("direction")

    if direction == "UP":
        findings.append("The market trend is consistently upward.")
    elif direction == "DOWN":
        findings.append("The market trend is consistently downward.")
    elif direction == "MIXED":
        findings.append("The market trend is mixed.")

    classification = opportunity.get("classification")

    findings.append(
        f"Market opportunity is classified as {classification}."
    )

    return {
        "market_size": sizing.get("market_size"),
        "growth_rate": growth,
        "trend_direction": direction,
        "opportunity_score": opportunity.get("opportunity_score"),
        "opportunity_classification": classification,
        "findings": findings,
    }
