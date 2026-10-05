from dataclasses import dataclass, asdict
from typing import Optional
import json

@dataclass
class Claim:
    claim_id: str
    evidence_id: Optional[str]
    source_url: Optional[str]
    title: str
    claim: str
    metric: Optional[str]
    value: Optional[float]
    unit: Optional[str]
    currency: Optional[str]
    period: Optional[str]
    geography: Optional[str]
    entity: Optional[str]
    confidence: float
    extraction_method: str

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False
        )
