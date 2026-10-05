"""Semantic entity resolution."""

from typing import Any


ALIASES = {
    "company": "company",
    "companies": "company",
    "firm": "company",
    "firms": "company",
    "customer": "customer",
    "customers": "customer",
    "client": "customer",
    "clients": "customer",
    "product": "product",
    "products": "product",
    "market": "market",
    "markets": "market",
    "region": "geography",
    "regions": "geography",
    "country": "geography",
    "countries": "geography",
}


def resolve(value: str) -> dict[str, Any]:
    raw = str(value).strip().lower()
    canonical = ALIASES.get(raw)

    return {
        "input": value,
        "canonical": canonical,
        "resolved": canonical is not None,
        "confidence": 1.0 if canonical else 0.0,
    }
