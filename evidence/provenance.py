from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

REGISTRY = Path("evidence/registry.jsonl")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def add(
    source,
    url=None,
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
    record = {
        "evidence_id": hashlib.sha256(
            f"{source}|{url}|{metric}|{value}|{period}".encode()
        ).hexdigest()[:24],
        "source": source,
        "url": url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "raw_path": str(raw_path) if raw_path else None,
        "sha256": sha256(raw_path) if raw_path and Path(raw_path).exists() else None,
        "metric": metric,
        "value": value,
        "unit": unit,
        "currency": currency,
        "period": period,
        "geography": geography,
        "methodology": methodology,
        "confidence": float(confidence)
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)

    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record

def all():
    if not REGISTRY.exists():
        return []

    return [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
