from __future__ import annotations

from typing import Any


def record(
    action_id: str,
    success: bool,
    output: Any = None,
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "action_id": str(action_id),
        "success": bool(success),
        "output": output,
        "error": error,
        "status": "COMPLETED" if success else "FAILED",
    }
