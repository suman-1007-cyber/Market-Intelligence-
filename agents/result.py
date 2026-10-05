"""Standard result object returned by agents."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    """Normalized result from an agent execution."""

    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: Any = None, **metadata: Any) -> "AgentResult":
        """Create a successful result."""
        return cls(
            success=True,
            data=data,
            metadata=metadata,
        )

    @classmethod
    def failure(cls, error: str, **metadata: Any) -> "AgentResult":
        """Create a failed result."""
        return cls(
            success=False,
            error=error,
            metadata=metadata,
        )
