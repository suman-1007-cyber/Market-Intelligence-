from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def create(
    event_type: str,
    agent_id: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not event_type or not agent_id:
        raise ValueError("event_type and agent_id are required")

    return {
        "event_type": str(event_type),
        "agent_id": str(agent_id),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details or {},
    }
