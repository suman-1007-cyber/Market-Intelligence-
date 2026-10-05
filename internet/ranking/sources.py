from urllib.parse import urlparse

AUTHORITY = {
    ".gov": 1.00,
    ".gov.in": 1.00,
    ".edu": 0.95,
    "reuters.com": 0.90,
    "bloomberg.com": 0.90,
    "ft.com": 0.90,
    "who.int": 1.00,
    "worldbank.org": 1.00,
    "imf.org": 1.00,
    "oecd.org": 1.00,
    "un.org": 1.00
}

def score(url):
    domain = urlparse(url).netloc.lower()
    domain = domain.split(":")[0]

    value = 0.50

    for key, weight in AUTHORITY.items():
        if domain.endswith(key):
            value = max(value, weight)

    if domain.endswith(".in"):
        value = max(value, 0.70)

    return round(value, 3)

def rank(results):
    return sorted(
        results,
        key=lambda x: score(x["url"]),
        reverse=True
    )
