from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from datetime import datetime, timezone
import hashlib
import json

CACHE = Path("internet/cache")
CACHE.mkdir(parents=True, exist_ok=True)

def fetch(url, timeout=20):
    key = hashlib.sha256(url.encode()).hexdigest()
    body_path = CACHE / f"{key}.html"
    meta_path = CACHE / f"{key}.json"

    if body_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return {
            "url": url,
            "path": str(body_path),
            "status": "cached",
            "retrieved_at": meta["retrieved_at"],
            "content_type": meta.get("content_type")
        }

    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Android) MarketIntelligenceEngine/1.0",
            "Accept": "text/html,application/xhtml+xml"
        }
    )

    try:
        with urlopen(req, timeout=timeout) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type", "")

        body_path.write_bytes(data)

        meta = {
            "url": url,
            "domain": urlparse(url).netloc,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "content_type": content_type,
            "bytes": len(data)
        }

        meta_path.write_text(
            json.dumps(meta, indent=2),
            encoding="utf-8"
        )

        return {
            "url": url,
            "path": str(body_path),
            "status": "downloaded",
            "retrieved_at": meta["retrieved_at"],
            "content_type": content_type
        }

    except Exception as exc:
        return {
            "url": url,
            "path": None,
            "status": "error",
            "error": str(exc)
        }
