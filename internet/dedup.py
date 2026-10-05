from urllib.parse import urlsplit, urlunsplit

def canonical(url):
    parts = urlsplit(url)

    return urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path.rstrip("/"),
        "",
        ""
    ))

def deduplicate(results):
    seen = set()
    output = []

    for item in results:
        url = canonical(item["url"])

        if url in seen:
            continue

        seen.add(url)

        copy = dict(item)
        copy["canonical_url"] = url
        output.append(copy)

    return output
