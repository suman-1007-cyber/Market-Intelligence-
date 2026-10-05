from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

from internet.search.engine import search
from internet.fetch.client import fetch
from internet.extract.html import extract
from internet.ranking.sources import rank, score
from internet.dedup import deduplicate
from evidence.provenance import add

RAW = Path("storage/bronze/web")
CLEAN = Path("storage/silver/web")

RAW.mkdir(parents=True, exist_ok=True)
CLEAN.mkdir(parents=True, exist_ok=True)

def collect(query, limit=5):
    discovered = search(query, limit=limit)

    results = deduplicate(
        rank(discovered.get("results", []))
    )

    records = []

    for item in results[:limit]:
        fetched = fetch(item["url"])

        if fetched["status"] == "error":
            records.append({
                "url": item["url"],
                "title": item["title"],
                "status": "error",
                "error": fetched["error"]
            })
            continue

        extracted = extract(fetched["path"])

        key = hashlib.sha256(
            item["url"].encode()
        ).hexdigest()[:20]

        clean_path = CLEAN / f"{key}.txt"
        raw_path = RAW / Path(fetched["path"]).name

        clean_path.write_text(
            extracted["text"],
            encoding="utf-8"
        )

        evidence = add(
            source=item["title"],
            url=item["url"],
            raw_path=raw_path,
            methodology="web_search_http_html_extraction",
            confidence=score(item["url"])
        )

        records.append({
            "title": item["title"],
            "url": item["url"],
            "raw_path": str(raw_path),
            "clean_path": str(clean_path),
            "words": extracted["words"],
            "source_score": score(item["url"]),
            "evidence_id": evidence["evidence_id"],
            "status": "collected"
        })

    return {
        "query": query,
        "results": records,
        "retrieved": len(
            [x for x in records if x["status"] == "collected"]
        )
    }
