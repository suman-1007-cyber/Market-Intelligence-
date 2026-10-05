"""Evidence collection and normalization."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source: str
    claim: str
    supports: tuple[str, ...] = ()
    contradicts: tuple[str, ...] = ()
    strength: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source": self.source,
            "claim": self.claim,
            "supports": list(self.supports),
            "contradicts": list(self.contradicts),
            "strength": self.strength,
        }


def collect(records: list[dict[str, Any]]) -> list[Evidence]:
    result: list[Evidence] = []

    for index, record in enumerate(records, start=1):
        source = str(
            record.get("source")
            or record.get("source_url")
            or ""
        ).strip()

        claim = str(
            record.get("claim")
            or record.get("finding")
            or record.get("text")
            or ""
        ).strip()

        if not claim:
            continue

        supports = tuple(
            str(value)
            for value in record.get("supports", [])
            if str(value).strip()
        )

        contradicts = tuple(
            str(value)
            for value in record.get("contradicts", [])
            if str(value).strip()
        )

        strength = float(record.get("strength", 0.5))
        strength = max(0.0, min(1.0, strength))

        result.append(
            Evidence(
                evidence_id=str(record.get("evidence_id", f"E{index}")),
                source=source,
                claim=claim,
                supports=supports,
                contradicts=contradicts,
                strength=strength,
            )
        )

    return result
