"""Deterministic competitor discovery."""

from typing import Any


def discover(
    records: list[dict[str, Any]],
    company_field: str = "company",
) -> list[dict[str, Any]]:
    discovered: dict[str, dict[str, Any]] = {}

    for record in records:
        name = str(record.get(company_field, "")).strip()

        if not name:
            continue

        key = name.casefold()

        if key not in discovered:
            discovered[key] = {
                "company": name,
                "sources": set(),
                "records": 0,
            }

        source = str(
            record.get("source")
            or record.get("source_url")
            or ""
        ).strip()

        if source:
            discovered[key]["sources"].add(source)

        discovered[key]["records"] += 1

    result = []

    for item in discovered.values():
        result.append(
            {
                "company": item["company"],
                "source_count": len(item["sources"]),
                "record_count": item["records"],
                "sources": sorted(item["sources"]),
            }
        )

    return sorted(
        result,
        key=lambda item: item["company"].casefold(),
    )
