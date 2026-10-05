from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import re

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_href = None
        self.current_text = []
        self.results = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "a":
            href = attrs.get("href")

            if href:
                self.current_href = href
                self.current_text = []

    def handle_data(self, data):
        if self.current_href:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.current_href:
            text = re.sub(
                r"\s+",
                " ",
                " ".join(self.current_text)
            ).strip()

            if text:
                self.results.append({
                    "url": self.current_href,
                    "title": text
                })

            self.current_href = None
            self.current_text = []

def _fetch(url):
    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 16) "
                "AppleWebKit/537.36 Chrome/140 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml"
        }
    )

    with urlopen(req, timeout=20) as response:
        return response.read().decode(
            "utf-8",
            errors="ignore"
        )

def _valid(url):
    if not url.startswith(("http://", "https://")):
        return False

    host = urlparse(url).netloc.lower()

    blocked = (
        "bing.com",
        "google.com",
        "duckduckgo.com"
    )

    return host and not any(
        host == x or host.endswith("." + x)
        for x in blocked
    )

def _parse(html):
    parser = LinkParser()
    parser.feed(html)

    output = []
    seen = set()

    for item in parser.results:
        url = item["url"]

        if not _valid(url):
            continue

        if url in seen:
            continue

        seen.add(url)

        output.append(item)

        if len(output) >= 10:
            break

    return output

def _bing(query):
    url = (
        "https://www.bing.com/search?q="
        + quote_plus(query)
    )

    html = _fetch(url)
    return _parse(html)

def _duckduckgo(query):
    url = (
        "https://html.duckduckgo.com/html/?q="
        + quote_plus(query)
    )

    html = _fetch(url)
    return _parse(html)

def _google(query):
    url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    html = _fetch(url)
    return _parse(html)

def search(query, limit=10):
    engines = [
        ("bing", _bing),
        ("duckduckgo", _duckduckgo),
        ("google", _google)
    ]

    errors = []

    for name, engine in engines:
        try:
            results = engine(query)

            if results:
                return {
                    "query": query,
                    "engine": name,
                    "results": results[:limit],
                    "error": None
                }

            errors.append(f"{name}: no results")

        except Exception as exc:
            errors.append(
                f"{name}: {type(exc).__name__}: {exc}"
            )

    return {
        "query": query,
        "engine": None,
        "results": [],
        "error": "; ".join(errors)
    }
