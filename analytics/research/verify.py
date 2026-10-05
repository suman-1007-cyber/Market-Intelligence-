"""Deterministic research evidence verification."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class VerifiedClaim:
    claim: str
    supporting_sources: tuple[str, ...]
    source_count: int
    confidence: float
    verified: bool


def verify(
    claim: str,
    supporting_sources: Iterable[str],
    minimum_sources: int = 2,
) -> VerifiedClaim:
    sources = tuple(sorted(set(
        str(source).strip()
        for source in supporting_sources
        if str(source).strip()
    )))

    if minimum_sources < 1:
        raise ValueError("minimum_sources must be at least 1.")

    count = len(sources)
    verified = count >= minimum_sources

    confidence = min(1.0, count / minimum_sources)

    return VerifiedClaim(
        claim=claim,
        supporting_sources=sources,
        source_count=count,
        confidence=confidence,
        verified=verified,
    )
