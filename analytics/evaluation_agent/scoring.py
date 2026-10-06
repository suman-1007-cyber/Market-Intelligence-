from __future__ import annotations

from typing import Any


def score(expected: Any, actual: Any) -> dict[str, Any]:
    matched = expected == actual

    return {
        "matched": matched,
        "score": 1.0 if matched else 0.0,
    }
