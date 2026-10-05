"""Competitive intelligence synthesis."""

from typing import Any


def synthesize(
    discovery: list[dict[str, Any]],
    profiles: list[dict[str, Any]],
    benchmarks: dict[str, Any],
    assessments: list[dict[str, Any]],
) -> dict[str, Any]:
    findings: list[str] = []

    if discovery:
        findings.append(
            f"{len(discovery)} competitors were identified."
        )

    if benchmarks.get("leader"):
        findings.append(
            f"{benchmarks['leader']} leads on {benchmarks['metric']}."
        )

    high_threats = [
        item
        for item in assessments
        if item["threat_level"] == "HIGH"
    ]

    high_opportunities = [
        item
        for item in assessments
        if item["opportunity_level"] == "HIGH"
    ]

    if high_threats:
        findings.append(
            f"{len(high_threats)} competitors have high threat scores."
        )

    if high_opportunities:
        findings.append(
            f"{len(high_opportunities)} competitors have high opportunity scores."
        )

    return {
        "competitor_count": len(profiles),
        "leader": benchmarks.get("leader"),
        "metric": benchmarks.get("metric"),
        "high_threat_count": len(high_threats),
        "high_opportunity_count": len(high_opportunities),
        "findings": findings,
    }
