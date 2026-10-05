"""Execution context shared by an agent during one task."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    """Runtime context for a single agent execution."""

    task_id: str
    input_data: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_metadata(self, **values: Any) -> "AgentContext":
        """Return a context with additional metadata."""
        updated = dict(self.metadata)
        updated.update(values)
        return AgentContext(
            task_id=self.task_id,
            input_data=self.input_data,
            metadata=updated,
        )
