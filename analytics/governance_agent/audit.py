from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def record(
    event: str,
    actor: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not event or not actor:
        raise ValueError("event and actor are required")

    return {
        "event": event,
        "actor": actor,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details or {},
    }
