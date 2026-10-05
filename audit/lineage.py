import hashlib
import json
from datetime import datetime, timezone


def create(
    source_url,
    raw_record,
    metric=None,
    value=None,
    unit=None,
    period=None,
    entity=None,
    transformation=None,
):
    raw_json = json.dumps(
        raw_record,
        sort_keys=True,
        default=str,
    )

    evidence_hash = hashlib.sha256(
        raw_json.encode("utf-8")
    ).hexdigest()

    return {
        "lineage_id": evidence_hash[:16],
        "source_url": source_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "evidence_hash": evidence_hash,
        "entity": entity,
        "metric": metric,
        "value": value,
        "unit": unit,
        "period": period,
        "transformation": transformation,
    }
