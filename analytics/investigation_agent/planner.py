"""Deterministic investigation planning."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InvestigationPlan:
    question: str
    objectives: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    steps: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "objectives": list(self.objectives),
            "evidence_requirements": list(self.evidence_requirements),
            "steps": list(self.steps),
        }


def plan(question: str) -> InvestigationPlan:
    question = str(question).strip()

    if not question:
        raise ValueError("Investigation question cannot be empty")

    return InvestigationPlan(
        question=question,
        objectives=(
            "identify the observed issue",
            "collect supporting evidence",
            "compare competing explanations",
            "identify the most supported cause",
        ),
        evidence_requirements=(
            "source-backed observations",
            "relevant quantitative metrics",
            "cross-source confirmation",
            "time or sequence context",
        ),
        steps=(
            "define_problem",
            "generate_hypotheses",
            "collect_evidence",
            "compare_evidence",
            "test_root_causes",
            "synthesize_findings",
        ),
    )
