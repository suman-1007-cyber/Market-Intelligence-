"""Deterministic hypothesis generation and scoring."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    category: str
    prior_score: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "statement": self.statement,
            "category": self.category,
            "prior_score": self.prior_score,
        }


def generate(question: str) -> list[Hypothesis]:
    question = str(question).strip()

    if not question:
        raise ValueError("Question cannot be empty")

    return [
        Hypothesis(
            "H1",
            f"Demand or market conditions contributed to: {question}",
            "market",
            0.5,
        ),
        Hypothesis(
            "H2",
            f"Competitive conditions contributed to: {question}",
            "competitive",
            0.5,
        ),
        Hypothesis(
            "H3",
            f"Internal operational factors contributed to: {question}",
            "operational",
            0.5,
        ),
        Hypothesis(
            "H4",
            f"Customer behavior contributed to: {question}",
            "customer",
            0.5,
        ),
    ]


def score(
    hypothesis: Hypothesis,
    supporting_evidence: int,
    contradicting_evidence: int,
) -> dict[str, Any]:
    supporting = max(0, int(supporting_evidence))
    contradicting = max(0, int(contradicting_evidence))
    total = supporting + contradicting

    if total == 0:
        score_value = hypothesis.prior_score
    else:
        score_value = supporting / total

    return {
        **hypothesis.to_dict(),
        "supporting_evidence": supporting,
        "contradicting_evidence": contradicting,
        "evidence_score": round(float(score_value), 6),
    }
