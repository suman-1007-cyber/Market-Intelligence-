from urllib.parse import quote_plus
from internet.providers.http import get
from internet.rss.parser import parse

FEEDS = {
    "google_news": (
        "https://news.google.com/rss/search?q={query}"
        "&hl=en-IN&gl=IN&ceid=IN:en"
    ),
    "bing_news": (
        "https://www.bing.com/news/search?q={query}"
        "&format=rss"
    )
}

def search(query, limit=10):
    all_results = []

    for provider, template in FEEDS.items():
        url = template.format(
            query=quote_plus(query)
        )

        response = get(url)

        if not response["ok"]:
            continue

        try:
            rows = parse(
                response["data"],
                response["url"]
            )
        except Exception:
            continue

        for row in rows:
            row["provider"] = provider
            all_results.append(row)

            if len(all_results) >= limit:
                return {
                    "query": query,
                    "provider": provider,
                    "results": all_results
                }

    return {
        "query": query,
        "provider": None,
        "results": all_results
    }
