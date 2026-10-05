"""Agent orchestration layer."""

from dataclasses import dataclass

from .base import Agent
from .context import AgentContext
from .execution import ExecutionEngine
from .recovery import RecoveryEngine
from .result import AgentResult
from .state import StateManager, TaskState
from .trace import TraceRecorder


@dataclass
class RegisteredAgent:
    agent: Agent


class AgentOrchestrator:
    """Central coordinator for registered agents."""

    def __init__(
        self,
        execution: ExecutionEngine,
        state: StateManager,
        recovery: RecoveryEngine,
        trace: TraceRecorder,
    ) -> None:
        self.execution = execution
        self.state = state
        self.recovery = recovery
        self.trace = trace
        self._agents: dict[str, RegisteredAgent] = {}

    def register(self, agent: Agent) -> None:
        agent_id = getattr(agent, "name", None)

        if not agent_id:
            raise ValueError("Agent must define a name.")

        if agent_id in self._agents:
            raise ValueError(f"Agent already registered: {agent_id}")

        self._agents[agent_id] = RegisteredAgent(agent)

    def has_agent(self, agent_id: str) -> bool:
        return agent_id in self._agents

    def list_agents(self) -> list[str]:
        return sorted(self._agents)

    def run(
        self,
        agent_id: str,
        context: AgentContext,
    ) -> AgentResult:
        if agent_id not in self._agents:
            raise KeyError(f"Agent not registered: {agent_id}")

        agent = self._agents[agent_id].agent

        if context.task_id not in {
            task.task_id for task in self.state.list_tasks()
        }:
            self.state.create(
                context.task_id,
                agent_id,
            )

        self.trace.record(
            context.task_id,
            "execution_started",
            agent=agent_id,
        )

        result = self.execution.run(agent, context)

        self.trace.record(
            context.task_id,
            "execution_completed",
            agent=agent_id,
            success=result.success,
            state=TaskState.COMPLETED.value
            if result.success
            else TaskState.FAILED.value,
        )

        return result
