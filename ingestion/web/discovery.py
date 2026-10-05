from urllib.parse import quote_plus

def search_urls(query):
    q = quote_plus(query)

    return {
        "google": f"https://www.google.com/search?q={q}",
        "bing": f"https://www.bing.com/search?q={q}",
        "duckduckgo": f"https://html.duckduckgo.com/html/?q={q}"
    }
