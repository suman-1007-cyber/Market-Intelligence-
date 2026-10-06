from __future__ import annotations

from typing import Any


def classify(
    error: str | None,
    retryable: bool = False,
) -> dict[str, Any]:
    if error:
        error_type = "RETRYABLE" if retryable else "NON_RETRYABLE"
    else:
        error_type = "NONE"

    return {
        "has_error": bool(error),
        "error": error,
        "type": error_type,
        "retryable": bool(retryable and error),
    }
