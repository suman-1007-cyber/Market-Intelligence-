from urllib.request import Request, urlopen
from pathlib import Path
import hashlib

def fetch(url, output_dir="storage/bronze"):
    req = Request(url, headers={"User-Agent": "MarketIntelligenceEngine/1.0"})
    with urlopen(req, timeout=20) as r:
        data = r.read()

    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    out = Path(output_dir) / f"web_{digest}.raw"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return out, data
