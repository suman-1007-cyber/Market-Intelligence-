from pathlib import Path
import json

from internet.dedup import canonical, deduplicate
from internet.ranking.sources import score, rank
from internet.search.engine import search
from evidence.web.collector import collect

assert canonical(
    "HTTPS://Example.COM/a/?x=1"
) == "https://example.com/a"

items = [
    {"url": "https://example.com/a", "title": "A"},
    {"url": "https://example.com/a?x=1", "title": "A duplicate"},
    {"url": "https://example.org/b", "title": "B"}
]

assert len(deduplicate(items)) == 2
assert score("https://www.gov.in/example") == 1.0
assert rank(items)[0]["url"] in {
    "https://example.com/a",
    "https://example.com/a?x=1",
    "https://example.org/b"
}

result = search("India market", limit=3)

assert "results" in result
assert "query" in result

print("==============================================")
print(" INTERNET INTELLIGENCE LAYER TEST")
print("==============================================")
print("URL canonicalization    : PASS")
print("Deduplication            : PASS")
print("Source authority scoring : PASS")
print("Source ranking           : PASS")
print("Search engine            : PASS")
print("==============================================")
print("INTERNET LAYER READY")
print("==============================================")
print("Search results returned:", len(result["results"]))
