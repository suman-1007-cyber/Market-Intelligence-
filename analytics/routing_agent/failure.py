from __future__ import annotations

from typing import Any


def classify(
    model_id: str,
    error: str | None,
    retryable: bool = True,
) -> dict[str, Any]:
    return {
        "model_id": str(model_id),
        "failed": bool(error),
        "error": error,
        "retryable": bool(error and retryable),
    }
