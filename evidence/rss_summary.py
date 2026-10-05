from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
import hashlib
import json

from internet.providers.http import get
from internet.rss.parser import parse
from internet.content.cleaner import extract_article_text


OUTPUT = Path("storage/silver/intelligence/rss_summaries.jsonl")

BING_RSS = (
    "https://www.bing.com/news/search?q={query}"
    "&format=rss"
)


def _hash(value):
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:24]


def resolve_article_url(discovery_url):
    if not discovery_url:
        return ""

    parsed = urlparse(discovery_url)

    if "bing.com" not in parsed.netloc.lower():
        return discovery_url

    target = parse_qs(
        parsed.query
    ).get("url", [""])[0]

    return unquote(target) if target else ""


def _publisher_accessible(article_url):
    if not article_url:
        return False

    try:
        response = get(article_url)
    except Exception:
        return False

    if not response["ok"]:
        return False

    content_type = response.get(
        "content_type",
        ""
    ).lower()

    if "html" not in content_type:
        return False

    try:
        html = response["data"].decode(
            "utf-8",
            errors="ignore"
        )

        article = extract_article_text(html)

        return bool(article.get("ok"))

    except Exception:
        return False


def collect(query, limit=10):
    url = BING_RSS.format(
        query=quote_plus(query)
    )

    response = get(url)

    if not response["ok"]:
        return []

    try:
        rows = parse(
            response["data"],
            response["url"]
        )
    except Exception:
        return []

    records = []

    for row in rows[:limit]:
        title = row.get(
            "title",
            ""
        ).strip()

        summary = row.get(
            "description",
            ""
        ).strip()

        discovery_url = row.get(
            "url",
            ""
        ).strip()

        if not title or not summary:
            continue

        article_url = resolve_article_url(
            discovery_url
        )

        accessible = _publisher_accessible(
            article_url
        )

        evidence_type = (
            "FULL_ARTICLE"
            if accessible
            else "RSS_SUMMARY"
        )

        content_status = (
            "article_accessible"
            if accessible
            else "summary_only"
        )

        record_id = _hash(
            discovery_url + "|" + title
        )

        records.append({
            "record_id": record_id,
            "evidence_type": evidence_type,
            "source": "bing_news",
            "query": query,
            "title": title,
            "publisher": (
                urlparse(article_url).netloc
                if article_url
                else ""
            ),
            "discovery_url": discovery_url,
            "article_url": article_url,
            "summary": summary,
            "retrieved_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "content_status": content_status,
            "methodology": "bing_news_rss"
        })

    return records


def write(records):
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT.open(
        "a",
        encoding="utf-8"
    ) as f:
        for record in records:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    return len(records)
