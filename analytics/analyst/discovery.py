"""Dataset discovery for the Data Analyst subsystem."""

from pathlib import Path
from typing import Any


SUPPORTED = {".csv", ".xlsx", ".xls", ".parquet", ".json", ".jsonl"}


def discover(root: str | Path) -> list[dict[str, Any]]:
    base = Path(root).expanduser()
    if not base.exists():
        raise FileNotFoundError(base)

    results = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        results.append({
            "name": path.name,
            "path": str(path),
            "format": path.suffix.lower().lstrip("."),
            "size_bytes": path.stat().st_size,
        })
    return results
