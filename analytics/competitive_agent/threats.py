"""Deterministic competitive threat and opportunity analysis."""

from typing import Any


def analyze(
    profile: dict[str, Any],
    market_average_share: float | None = None,
    leader_share: float | None = None,
) -> dict[str, Any]:
    share = profile.get("market_share")

    threat_score = 0.0
    opportunity_score = 0.0
    factors: list[str] = []

    if share is not None:
        share = float(share)

        if leader_share is not None and share >= float(leader_share):
            threat_score += 0.50
            factors.append("Competitor has leader-level market share.")
        elif market_average_share is not None and share > float(
            market_average_share
        ):
            threat_score += 0.30
            factors.append("Competitor is above average market share.")

        if share < 0.10:
            opportunity_score += 0.30
            factors.append("Competitor has relatively low market share.")

    strengths = profile.get("strengths", [])
    weaknesses = profile.get("weaknesses", [])

    if strengths:
        threat_score += min(0.30, 0.10 * len(strengths))
        factors.append("Competitor has documented strengths.")

    if weaknesses:
        opportunity_score += min(0.30, 0.10 * len(weaknesses))
        factors.append("Competitor has documented weaknesses.")

    threat_score = min(1.0, threat_score)
    opportunity_score = min(1.0, opportunity_score)

    if threat_score >= 0.60:
        threat_level = "HIGH"
    elif threat_score >= 0.30:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    if opportunity_score >= 0.60:
        opportunity_level = "HIGH"
    elif opportunity_score >= 0.30:
        opportunity_level = "MEDIUM"
    else:
        opportunity_level = "LOW"

    return {
        "company": profile["company"],
        "threat_score": round(threat_score, 6),
        "threat_level": threat_level,
        "opportunity_score": round(opportunity_score, 6),
        "opportunity_level": opportunity_level,
        "factors": factors,
    }
