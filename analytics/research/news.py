"""News intelligence normalization."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NewsItem:
    title: str
    url: str
    publisher: str = ""
    published_at: str = ""
    summary: str = ""


def normalize(items: list[dict]) -> list[NewsItem]:
    result = []

    for item in items:
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()

        if not title or not url:
            continue

        result.append(
            NewsItem(
                title=title,
                url=url,
                publisher=str(item.get("publisher", "")),
                published_at=str(item.get("published_at", "")),
                summary=str(item.get("summary", "")),
            )
        )

    return result
