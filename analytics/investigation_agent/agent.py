"""Investigation Intelligence Agent."""

from dataclasses import dataclass
from typing import Any


from .cross_source import compare
from .evidence import collect
from .hypotheses import generate, score
from .planner import plan
from .root_cause import investigate
from .synthesis import synthesize


@dataclass
class InvestigationAgent:
    agent_id: str = "investigation-agent"

    def investigate(
        self,
        question: str,
        evidence_records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        investigation_plan = plan(question)

        hypotheses = generate(question)

        evidence = collect(evidence_records)

        evidence_dicts = [
            item.to_dict()
            for item in evidence
        ]

        scored_hypotheses = []

        for hypothesis in hypotheses:
            supporting = sum(
                1
                for item in evidence_dicts
                if hypothesis.hypothesis_id
                in item.get("supports", [])
            )

            contradicting = sum(
                1
                for item in evidence_dicts
                if hypothesis.hypothesis_id
                in item.get("contradicts", [])
            )

            scored_hypotheses.append(
                score(
                    hypothesis,
                    supporting,
                    contradicting,
                )
            )

        cross_source = compare(evidence_dicts)

        root_causes = investigate(
            scored_hypotheses,
            evidence_dicts,
        )

        synthesis = synthesize(
            question,
            root_causes,
            cross_source,
        )

        return {
            "agent_id": self.agent_id,
            "plan": investigation_plan.to_dict(),
            "hypotheses": scored_hypotheses,
            "evidence": evidence_dicts,
            "cross_source": cross_source,
            "root_causes": root_causes,
            "synthesis": synthesis,
        }
