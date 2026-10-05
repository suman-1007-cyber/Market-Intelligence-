"""Agent execution engine."""

from dataclasses import dataclass
from typing import Any

from .base import Agent
from .context import AgentContext
from .permissions import PermissionEngine
from .result import AgentResult
from .state import StateManager, TaskState
from .tools import ToolRegistry


@dataclass
class ExecutionEngine:
    """Coordinates one agent execution."""

    state: StateManager
    tools: ToolRegistry
    permissions: PermissionEngine

    def invoke_tool(
        self,
        agent_id: str,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:
        if not self.permissions.check_tool(agent_id, tool_name):
            raise PermissionError(
                f"Agent '{agent_id}' is not permitted to use '{tool_name}'."
            )

        return self.tools.invoke(tool_name, **kwargs)

    def run(
        self,
        agent: Agent,
        context: AgentContext,
    ) -> AgentResult:
        task = self.state.get(context.task_id)

        self.state.update(
            context.task_id,
            TaskState.READY,
        )

        self.state.increment_attempt(context.task_id)

        result = agent.execute(context)

        if result.success:
            self.state.update(
                context.task_id,
                TaskState.COMPLETED,
                result=result.data,
                error=None,
            )
        else:
            self.state.update(
                context.task_id,
                TaskState.FAILED,
                result=result.data,
                error=result.error,
            )

        return result
