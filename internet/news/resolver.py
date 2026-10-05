from urllib.parse import quote_plus, urlparse, parse_qs, unquote
from internet.providers.http import get
from internet.rss.parser import parse
from internet.content.cleaner import extract_article_text


BING_RSS = (
    "https://www.bing.com/news/search?q={query}"
    "&format=rss"
)


def _publisher_url(url):
    if not url:
        return ""

    parsed = urlparse(url)

    if "bing.com" not in parsed.netloc.lower():
        return url

    value = parse_qs(parsed.query).get("url", [""])[0]

    if not value:
        return ""

    return unquote(value)


def _domain(url):
    try:
        return urlparse(url).netloc.lower().split(":")[0]
    except Exception:
        return ""


def _publisher_match(url, publisher):
    if not publisher:
        return False

    domain = _domain(url)
    publisher = publisher.lower()

    parts = [
        p.strip(" .,-_")
        for p in publisher.replace("&", " ").split()
        if len(p.strip(" .,-_")) >= 3
    ]

    return any(part in domain for part in parts)


def resolve(title, publisher="", exclude_url=""):
    query = quote_plus(f'"{title}"')

    url = BING_RSS.format(query=query)

    response = get(url)

    if not response["ok"]:
        return {
            "ok": False,
            "reason": "bing_news_unavailable",
            "article_url": "",
            "discovery_url": exclude_url,
            "title": title,
            "publisher": publisher,
        }

    try:
        rows = parse(
            response["data"],
            response["url"]
        )
    except Exception:
        return {
            "ok": False,
            "reason": "bing_rss_parse_failed",
            "article_url": "",
            "discovery_url": exclude_url,
            "title": title,
            "publisher": publisher,
        }

    candidates = []

    for row in rows:
        bing_url = row.get("url", "")
        article_url = _publisher_url(bing_url)

        if not article_url:
            continue

        if article_url == exclude_url:
            continue

        score = 0

        row_title = row.get("title", "").strip().lower()
        target_title = title.strip().lower()

        if row_title == target_title:
            score += 10

        if target_title in row_title or row_title in target_title:
            score += 5

        if _publisher_match(article_url, publisher):
            score += 10

        candidates.append(
            (score, article_url, row)
        )

    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    for score, article_url, row in candidates:
        article_response = get(article_url)

        if not article_response["ok"]:
            continue

        content_type = article_response.get(
            "content_type",
            ""
        ).lower()

        if "html" not in content_type:
            continue

        html = article_response["data"].decode(
            "utf-8",
            errors="ignore"
        )

        article = extract_article_text(html)

        if not article.get("ok"):
            continue

        return {
            "ok": True,
            "article_url": article_response["url"],
            "discovery_url": exclude_url,
            "title": title,
            "publisher": publisher,
            "provider": "bing_news",
            "score": score,
            "text": article["text"],
        }

    return {
        "ok": False,
        "reason": "publisher_article_not_accessible",
        "article_url": "",
        "discovery_url": exclude_url,
        "title": title,
        "publisher": publisher,
    }
