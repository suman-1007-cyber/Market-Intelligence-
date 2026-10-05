from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import time

UA = (
    "MarketIntelligenceEngine/1.0 "
    "(research; evidence-first)"
)

def get(url, timeout=20, retries=3):
    last_error = None

    for attempt in range(retries):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": (
                        "application/rss+xml,"
                        "application/atom+xml,"
                        "application/json,"
                        "text/html,*/*"
                    )
                }
            )

            with urlopen(req, timeout=timeout) as response:
                return {
                    "ok": True,
                    "status": response.status,
                    "url": response.geturl(),
                    "content_type": response.headers.get(
                        "Content-Type", ""
                    ),
                    "data": response.read()
                }

        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"

            if attempt < retries - 1:
                time.sleep(2 ** attempt)

    return {
        "ok": False,
        "status": None,
        "url": url,
        "content_type": "",
        "data": b"",
        "error": last_error
    }
