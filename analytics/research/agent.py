"""Deterministic Deep Research Agent."""

from dataclasses import dataclass
from typing import Any

from .planner import plan
from .sources import discover
from .verify import verify
from .synthesis import ResearchFinding, synthesize


@dataclass
class DeepResearchAgent:
    agent_id: str = "deep-research-agent"

    def investigate(
        self,
        question: str,
        sources: list[dict[str, Any]],
        claims: list[dict[str, Any]],
    ) -> dict[str, Any]:
        research_plan = plan(question)
        discovered = discover(sources)

        verified_claims = []

        for item in claims:
            claim = str(item.get("claim", "")).strip()
            supporting = item.get("supporting_sources", [])

            if not claim:
                continue

            verified_claims.append(
                verify(
                    claim,
                    supporting,
                    minimum_sources=int(
                        item.get("minimum_sources", 2)
                    ),
                )
            )

        findings = [
            ResearchFinding(
                finding=claim.claim,
                evidence=tuple(
                    {"source": source}
                    for source in claim.supporting_sources
                ),
                confidence=claim.confidence,
                verified=claim.verified,
            )
            for claim in verified_claims
        ]

        return {
            "agent_id": self.agent_id,
            "plan": research_plan,
            "sources": discovered,
            "verification": verified_claims,
            "synthesis": synthesize(findings),
        }
