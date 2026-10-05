from internet.providers.rss import search as rss_search

def search(query, limit=10):
    result = rss_search(query, limit)

    if result["results"]:
        return result

    return {
        "query": query,
        "provider": None,
        "results": [],
        "error": "No RSS results available"
    }
