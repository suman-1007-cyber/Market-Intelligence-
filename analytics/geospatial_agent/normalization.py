from __future__ import annotations

from typing import Any


ALIASES = {
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
}


def normalize_region(region: str) -> str:
    value = str(region).strip()
    return ALIASES.get(value.lower(), value)


def normalize(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    normalized = []

    for record in records:
        item = dict(record)
        item["region"] = normalize_region(item["region"])
        normalized.append(item)

    return normalized
