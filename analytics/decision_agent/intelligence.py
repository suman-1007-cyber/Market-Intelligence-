"""Decision intelligence synthesis."""

from typing import Any


def synthesize(
    evaluation: list[dict[str, Any]],
    recommendation: dict[str, Any],
    risk: dict[str, Any],
) -> dict[str, Any]:
    findings: list[str] = []

    if evaluation:
        findings.append(
            f"{len(evaluation)} alternatives were evaluated."
        )

    if recommendation.get("recommendation"):
        findings.append(
            f"Top recommendation: "
            f"{recommendation['recommendation']}."
        )

    findings.append(
        f"Decision risk is {risk['risk_level']}."
    )

    if risk.get("requires_review"):
        findings.append(
            "Decision requires additional review before execution."
        )

    return {
        "decision": recommendation.get("recommendation"),
        "decision_score": recommendation.get("score"),
        "decision_status": recommendation.get("status"),
        "risk_level": risk.get("risk_level"),
        "risk_score": risk.get("risk_score"),
        "decision_margin": risk.get("decision_margin"),
        "findings": findings,
    }
