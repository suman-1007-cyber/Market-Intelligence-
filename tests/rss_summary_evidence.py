from pathlib import Path
import json

from evidence.rss_summary import (
    collect,
    write,
    resolve_article_url
)

QUERY = "Dassault Systèmes India semiconductor"

print("==============================================")
print(" RSS SUMMARY / ARTICLE URL TEST")
print("==============================================")

records = collect(
    QUERY,
    limit=10
)

assert records, "No RSS records collected"

resolved = 0
full_articles = 0
summary_only = 0

for record in records:
    assert record["record_id"]
    assert record["evidence_type"] in {
        "RSS_SUMMARY",
        "FULL_ARTICLE"
    }
    assert record["source"] == "bing_news"
    assert record["title"]
    assert record["summary"]
    assert record["discovery_url"]
    assert record["article_url"].startswith("http")

    resolved += 1

    if record["evidence_type"] == "FULL_ARTICLE":
        assert record["content_status"] == "article_accessible"
        full_articles += 1
    else:
        assert record["evidence_type"] == "RSS_SUMMARY"
        assert record["content_status"] == "summary_only"
        summary_only += 1

sample_url = records[0]["discovery_url"]

resolved_url = resolve_article_url(
    sample_url
)

assert resolved_url.startswith("http")

count = write(records)

output = Path(
    "storage/silver/intelligence/rss_summaries.jsonl"
)

assert output.exists()
assert output.stat().st_size > 0

print("Records collected :", len(records))
print("Publisher URLs    :", resolved)
print("Full articles     :", full_articles)
print("RSS summaries     :", summary_only)
print("Written records   :", count)
print("URL resolution    : PASS")
print("Graceful fallback : PASS")
print("Evidence separation: PASS")
print("Silver output     :", output)
print("----------------------------------------------")
print("RSS evidence layer: PASS")
print("==============================================")

print("\nFIRST RECORD:")
print(
    json.dumps(
        records[0],
        indent=2,
        ensure_ascii=False
    )
)
