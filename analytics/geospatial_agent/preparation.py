from __future__ import annotations

from typing import Any, Iterable


def prepare(
    records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    prepared = []

    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Each geographic record must be a dictionary")

        if "region" not in record:
            raise ValueError("Each record must contain 'region'")

        item = dict(record)
        item["region"] = str(item["region"]).strip()

        if not item["region"]:
            raise ValueError("region must not be empty")

        prepared.append(item)

    return {
        "records": prepared,
        "count": len(prepared),
    }
