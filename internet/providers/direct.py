from internet.providers.http import get

def fetch(url):
    response = get(url)

    if not response["ok"]:
        return response

    return {
        "ok": True,
        "url": response["url"],
        "status": response["status"],
        "content_type": response["content_type"],
        "data": response["data"]
    }
