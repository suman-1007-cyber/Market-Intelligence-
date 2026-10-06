from __future__ import annotations

import re


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,]+"),
]


def scan(text: str) -> dict[str, object]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    matches = []
    for pattern in SECRET_PATTERNS:
        matches.extend(pattern.findall(text))

    return {
        "secret_detected": bool(matches),
        "match_count": len(matches),
    }
