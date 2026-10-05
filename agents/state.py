"""Agent task state management."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TaskState(str, Enum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskRecord:
    """State record for one agent task."""

    task_id: str
    agent_id: str
    state: TaskState = TaskState.CREATED
    attempts: int = 0
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class StateManager:
    """In-memory task state store for the first control-plane version."""

    def __init__(self) -> None:
        self._tasks: dict[str, TaskRecord] = {}

    def create(self, task_id: str, agent_id: str, **metadata: Any) -> TaskRecord:
        if task_id in self._tasks:
            raise ValueError(f"Task already exists: {task_id}")

        record = TaskRecord(
            task_id=task_id,
            agent_id=agent_id,
            metadata=dict(metadata),
        )
        self._tasks[task_id] = record
        return record

    def get(self, task_id: str) -> TaskRecord:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"Task not found: {task_id}") from exc

    def update(self, task_id: str, state: TaskState, **values: Any) -> TaskRecord:
        record = self.get(task_id)
        record.state = state

        for key, value in values.items():
            if hasattr(record, key):
                setattr(record, key, value)
            else:
                record.metadata[key] = value

        record.updated_at = datetime.now(timezone.utc).isoformat()
        return record

    def increment_attempt(self, task_id: str) -> int:
        record = self.get(task_id)
        record.attempts += 1
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return record.attempts

    def list_tasks(self) -> list[TaskRecord]:
        return list(self._tasks.values())
