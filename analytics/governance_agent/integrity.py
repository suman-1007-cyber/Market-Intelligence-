from __future__ import annotations

import hashlib
import json
from typing import Any


def fingerprint(data: Any) -> str:
    payload = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def verify(data: Any, expected: str) -> bool:
    return fingerprint(data) == str(expected)
