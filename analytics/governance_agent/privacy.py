from __future__ import annotations

from typing import Any


SENSITIVE_FIELDS = {
    "password",
    "token",
    "secret",
    "api_key",
    "apikey",
}


def sanitize(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary")

    return {
        key: "***REDACTED***" if str(key).lower() in SENSITIVE_FIELDS else value
        for key, value in record.items()
    }
