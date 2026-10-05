"""Research source discovery."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ResearchSource:
    url: str
    title: str = ""
    source_type: str = "web"
    publisher: str = ""
    authority: float = 0.5


def discover(sources: Iterable[dict]) -> list[ResearchSource]:
    results = []

    for item in sources:
        url = str(item.get("url", "")).strip()
        if not url:
            continue

        results.append(
            ResearchSource(
                url=url,
                title=str(item.get("title", "")),
                source_type=str(item.get("source_type", "web")),
                publisher=str(item.get("publisher", "")),
                authority=float(item.get("authority", 0.5)),
            )
        )

    return results
