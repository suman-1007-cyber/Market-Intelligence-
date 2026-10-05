from pathlib import Path
from urllib.request import Request, urlopen
import hashlib

def fetch(url, output_dir="storage/bronze"):
    req = Request(
        url,
        headers={"User-Agent": "MarketIntelligenceEngine/1.0"}
    )

    with urlopen(req, timeout=20) as response:
        data = response.read()

    digest = hashlib.sha256(url.encode()).hexdigest()[:20]
    path = Path(output_dir) / f"web_{digest}.raw"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

    return path
