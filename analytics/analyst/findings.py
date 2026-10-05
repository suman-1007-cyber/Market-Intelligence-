"""Evidence-backed analyst finding model."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnalystFinding:
    finding: str
    finding_type: str
    evidence: dict[str, Any]
    calculation: str
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding": self.finding,
            "type": self.finding_type,
            "evidence": self.evidence,
            "calculation": self.calculation,
            "confidence": self.confidence,
        }
