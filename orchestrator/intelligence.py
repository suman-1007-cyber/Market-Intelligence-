from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

from sources.discovery import discover
from orchestrator.planner import plan
from internet.providers.router import search
from internet.providers.http import get
from internet.rss.parser import parse
from internet.ranking.sources import score, rank
from internet.dedup import deduplicate
from evidence.provenance import add

BRONZE = Path("storage/bronze/intelligence")
SILVER = Path("storage/silver/intelligence")
BRONZE.mkdir(parents=True, exist_ok=True)
SILVER.mkdir(parents=True, exist_ok=True)

def _safe_name(value):
    return hashlib.sha256(
        value.encode()
    ).hexdigest()[:24]

def _queries(question):
    return [
        question,
        f"{question} market size",
        f"{question} market growth",
        f"{question} market share",
        f"{question} competitors",
        f"{question} industry trends",
        f"{question} forecast"
    ]

def investigate(question, limit_per_query=5):
    investigation_plan = plan(question)
    source_plan = discover(question)

    discovered = []

    for query in _queries(question):
        result = search(
            query,
            limit=limit_per_query
        )

        for item in result.get("results", []):
            item = dict(item)
            item["query"] = query
            discovered.append(item)

    discovered = deduplicate(discovered)
    discovered = rank(discovered)

    documents = []

    for item in discovered:
        url = item.get("url")

        if not url:
            continue

        response = get(url)

        if not response["ok"]:
            continue

        data = response["data"]
        key = _safe_name(url)

        raw_path = BRONZE / f"{key}.raw"
        raw_path.write_bytes(data)

        content_type = response.get(
            "content_type",
            ""
        ).lower()

        extracted = ""

        if (
            "rss" in content_type
            or "xml" in content_type
            or data.lstrip().startswith(b"<?xml")
        ):
            try:
                rows = parse(
                    data,
                    response["url"]
                )

                extracted = json.dumps(
                    rows,
                    indent=2,
                    ensure_ascii=False
                )

            except Exception:
                extracted = data.decode(
                    "utf-8",
                    errors="ignore"
                )
        else:
            extracted = data.decode(
                "utf-8",
                errors="ignore"
            )

        clean_path = SILVER / f"{key}.txt"

        clean_path.write_text(
            extracted,
            encoding="utf-8"
        )

        evidence = add(
            source=item.get(
                "provider",
                item.get("title", "external")
            ),
            url=url,
            raw_path=raw_path,
            methodology="external_rss_http_ingestion",
            confidence=score(url)
        )

        documents.append({
            "title": item.get("title", ""),
            "url": url,
            "query": item.get("query"),
            "provider": item.get("provider"),
            "source_score": score(url),
            "raw_path": str(raw_path),
            "clean_path": str(clean_path),
            "evidence_id": evidence["evidence_id"],
            "retrieved_at": datetime.now(
                timezone.utc
            ).isoformat()
        })

    result = {
        "question": question,
        "plan": investigation_plan,
        "sources": source_plan,
        "documents": documents,
        "document_count": len(documents),
        "status": (
            "evidence_acquired"
            if documents
            else "no_external_evidence"
        )
    }

    output = SILVER / "investigation.json"

    output.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return result
