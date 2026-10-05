"""Business dimension resolution."""

from typing import Any


DIMENSIONS = {
    "time": {"aliases": ["time", "date", "period", "year", "month", "quarter"]},
    "geography": {"aliases": ["region", "country", "city", "geography", "location"]},
    "product": {"aliases": ["product", "sku", "item"]},
    "customer": {"aliases": ["customer", "client", "segment"]},
    "company": {"aliases": ["company", "competitor", "firm"]},
    "channel": {"aliases": ["channel", "sales channel", "distribution"]},
}


def resolve(value: str) -> dict[str, Any]:
    raw = str(value).strip().lower()

    for canonical, definition in DIMENSIONS.items():
        if raw == canonical or raw in definition["aliases"]:
            return {
                "input": value,
                "canonical": canonical,
                "resolved": True,
                "confidence": 1.0,
            }

    return {
        "input": value,
        "canonical": None,
        "resolved": False,
        "confidence": 0.0,
    }
