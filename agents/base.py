"""Base agent runtime contract.

This module intentionally contains no LLM, tool, network, or provider logic.
Those capabilities are added by later milestones.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from .context import AgentContext
from .result import AgentResult


class AgentStatus(str, Enum):
    """Lifecycle states for an agent execution."""

    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Agent(ABC):
    """Base contract implemented by every future agent."""

    name = "base-agent"
    version = "1.0.0"

    def __init__(self) -> None:
        self.status = AgentStatus.CREATED
        self.context: AgentContext | None = None

    def prepare(self, context: AgentContext) -> None:
        """Prepare the agent for execution."""
        if self.status not in {
            AgentStatus.CREATED,
            AgentStatus.COMPLETED,
            AgentStatus.FAILED,
            AgentStatus.CANCELLED,
        }:
            raise RuntimeError(
                f"Cannot prepare agent from state: {self.status.value}"
            )

        self.context = context
        self.status = AgentStatus.READY

    def execute(self, context: AgentContext | None = None) -> AgentResult:
        """Execute the agent using the standard lifecycle."""
        if context is not None:
            self.prepare(context)

        if self.context is None:
            raise RuntimeError("Agent context is required before execution.")

        if self.status != AgentStatus.READY:
            raise RuntimeError(
                f"Agent must be READY before execution, got: {self.status.value}"
            )

        self.status = AgentStatus.RUNNING

        try:
            result = self.run(self.context)

            if not isinstance(result, AgentResult):
                raise TypeError(
                    "Agent run() must return an AgentResult."
                )

            self.status = AgentStatus.VERIFYING

            if result.success:
                self.status = AgentStatus.COMPLETED
            else:
                self.status = AgentStatus.FAILED

            return result

        except Exception as exc:
            self.status = AgentStatus.FAILED
            return AgentResult.failure(
                str(exc),
                agent=self.name,
                version=self.version,
            )

    def cancel(self) -> None:
        """Cancel an agent that has not completed."""
        if self.status in {
            AgentStatus.COMPLETED,
            AgentStatus.FAILED,
            AgentStatus.CANCELLED,
        }:
            return

        self.status = AgentStatus.CANCELLED

    @abstractmethod
    def run(self, context: AgentContext) -> AgentResult:
        """Implement the agent-specific deterministic work."""
        raise NotImplementedError
