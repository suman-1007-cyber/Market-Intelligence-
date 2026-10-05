from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

REGISTRY = Path("evidence/registry.jsonl")

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def record(
    source,
    url=None,
    retrieved_at=None,
    raw_path=None,
    metric=None,
    value=None,
    unit=None,
    currency=None,
    period=None,
    geography=None,
    methodology=None,
    confidence=0.0,
):
    if retrieved_at is None:
        retrieved_at = datetime.now(timezone.utc).isoformat()

    digest = None
    if raw_path:
        p = Path(raw_path)
        if p.exists():
            digest = sha256_bytes(p.read_bytes())

    item = {
        "source": source,
        "url": url,
        "retrieved_at": retrieved_at,
        "raw_path": str(raw_path) if raw_path else None,
        "sha256": digest,
        "metric": metric,
        "value": value,
        "unit": unit,
        "currency": currency,
        "period": period,
        "geography": geography,
        "methodology": methodology,
        "confidence": float(confidence),
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return item
