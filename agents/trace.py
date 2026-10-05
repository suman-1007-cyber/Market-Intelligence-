"""Agent execution tracing and observability."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class TraceEvent:
    """Single immutable execution event."""

    task_id: str
    event: str
    timestamp: str
    metadata: dict[str, Any]


class TraceRecorder:
    """Records the execution trajectory of agents."""

    def __init__(self) -> None:
        self._events: list[TraceEvent] = []

    def record(
        self,
        task_id: str,
        event: str,
        **metadata: Any,
    ) -> TraceEvent:
        item = TraceEvent(
            task_id=task_id,
            event=event,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
        )
        self._events.append(item)
        return item

    def for_task(self, task_id: str) -> list[TraceEvent]:
        return [
            event
            for event in self._events
            if event.task_id == task_id
        ]

    def all(self) -> list[TraceEvent]:
        return list(self._events)
