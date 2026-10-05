"""Deterministic research planning."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchPlan:
    question: str
    objectives: tuple[str, ...]
    source_types: tuple[str, ...]
    steps: tuple[str, ...]


def plan(question: str) -> ResearchPlan:
    if not question or not question.strip():
        raise ValueError("Research question cannot be empty.")

    return ResearchPlan(
        question=question.strip(),
        objectives=(
            "identify relevant evidence",
            "compare independent sources",
            "verify important claims",
        ),
        source_types=("web", "news", "documents"),
        steps=(
            "discover_sources",
            "retrieve_evidence",
            "extract_claims",
            "verify_claims",
            "synthesize_findings",
        ),
    )
