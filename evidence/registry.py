from pathlib import Path
import json

PATH = Path("evidence/registry.jsonl")

def all_records():
    if not PATH.exists():
        return []
    return [
        json.loads(x)
        for x in PATH.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]

def find(metric=None, source=None):
    rows = all_records()
    if metric:
        rows = [r for r in rows if r.get("metric") == metric]
    if source:
        rows = [r for r in rows if r.get("source") == source]
    return rows
