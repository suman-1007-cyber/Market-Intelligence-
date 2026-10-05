"""Evidence-preserving research synthesis."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResearchFinding:
    finding: str
    evidence: tuple[dict[str, Any], ...]
    confidence: float
    verified: bool


def synthesize(
    findings: list[ResearchFinding],
) -> dict[str, Any]:
    return {
        "finding_count": len(findings),
        "verified_count": sum(
            1 for finding in findings if finding.verified
        ),
        "findings": [
            {
                "finding": finding.finding,
                "evidence": list(finding.evidence),
                "confidence": finding.confidence,
                "verified": finding.verified,
            }
            for finding in findings
        ],
    }
