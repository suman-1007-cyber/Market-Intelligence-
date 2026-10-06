from __future__ import annotations

from typing import Any


def collect(findings: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")

    valid = [item for item in findings if isinstance(item, dict)]
    return {
        "count": len(valid),
        "findings": valid,
    }
