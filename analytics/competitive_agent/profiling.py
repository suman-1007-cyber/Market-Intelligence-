"""Deterministic competitor profiling."""

from typing import Any


def profile(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}

    for record in records:
        company = str(record.get("company", "")).strip()

        if not company:
            continue

        key = company.casefold()

        if key not in profiles:
            profiles[key] = {
                "company": company,
                "revenue": None,
                "market_share": None,
                "customers": None,
                "products": set(),
                "strengths": set(),
                "weaknesses": set(),
            }

        item = profiles[key]

        for field in ("revenue", "market_share", "customers"):
            if record.get(field) is not None:
                item[field] = float(record[field])

        for field in ("products", "strengths", "weaknesses"):
            value = record.get(field)

            if isinstance(value, (list, tuple, set)):
                item[field].update(
                    str(v).strip()
                    for v in value
                    if str(v).strip()
                )
            elif value:
                item[field].add(str(value).strip())

    result = []

    for item in profiles.values():
        result.append(
            {
                "company": item["company"],
                "revenue": item["revenue"],
                "market_share": item["market_share"],
                "customers": item["customers"],
                "products": sorted(item["products"]),
                "strengths": sorted(item["strengths"]),
                "weaknesses": sorted(item["weaknesses"]),
            }
        )

    return sorted(
        result,
        key=lambda item: item["company"].casefold(),
    )
