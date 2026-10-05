import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Integrated tests for Agent Control Plane milestones 41–48."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents import (
    Agent,
    AgentContext,
    AgentContract,
    AgentOrchestrator,
    AgentResult,
    ExecutionEngine,
    PermissionEngine,
    PermissionPolicy,
    RecoveryEngine,
    RetryPolicy,
    StateManager,
    TaskState,
    ToolDefinition,
    ToolRegistry,
    TraceRecorder,
)


class TestAgent(Agent):
    name = "test-analytics-agent"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult.ok(
            {"received": context.input_data},
            task_id=context.task_id,
        )


def add(a, b):
    return a + b


def main():
    # 41 — Agent Contract
    contract = AgentContract(
        agent_id="test-analytics-agent",
        name="Test Analytics Agent",
        version="1.0.0",
        description="Deterministic test agent.",
        capabilities=("analytics",),
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )

    assert contract.validate_input({"x": 1})
    assert not contract.validate_input("invalid")
    assert contract.supports("analytics")
    assert not contract.supports("web")

    # 42 — Tool Registry
    tools = ToolRegistry()
    tools.register(
        ToolDefinition(
            name="add",
            description="Add two numbers.",
            handler=add,
        )
    )

    assert tools.has("add")
    assert tools.invoke("add", a=2, b=3) == 5
    assert tools.list_tools() == ["add"]

    # 43 — Permission Engine
    permissions = PermissionEngine()
    permissions.register(
        PermissionPolicy(
            agent_id="test-analytics-agent",
            allowed_tools={"add"},
        )
    )

    assert permissions.check_tool("test-analytics-agent", "add")
    assert not permissions.check_tool("test-analytics-agent", "delete")

    assert not permissions.check_tool("unknown-agent", "add")

    # 44 — State Manager
    state = StateManager()
    state.create("task-41-48", "test-analytics-agent")

    assert state.get("task-41-48").state == TaskState.CREATED

    state.update("task-41-48", TaskState.READY)
    assert state.get("task-41-48").state == TaskState.READY

    # 45 — Execution Engine
    execution = ExecutionEngine(
        state=state,
        tools=tools,
        permissions=permissions,
    )

    agent = TestAgent()

    result = execution.run(
        agent,
        AgentContext(
            task_id="task-41-48",
            input_data={"question": "test"},
        ),
    )

    assert result.success
    assert result.data["received"]["question"] == "test"
    assert state.get("task-41-48").state == TaskState.COMPLETED

    # 46 — Recovery
    recovery = RecoveryEngine(RetryPolicy(max_attempts=3))

    assert recovery.should_retry(1)
    assert recovery.should_retry(2)
    assert not recovery.should_retry(3)

    # 47 — Trace
    trace = TraceRecorder()
    trace.record("trace-test", "started", agent="test")
    trace.record("trace-test", "completed", success=True)

    events = trace.for_task("trace-test")

    assert len(events) == 2
    assert events[0].event == "started"
    assert events[1].event == "completed"

    # 48 — Orchestrator
    orchestrator = AgentOrchestrator(
        execution=execution,
        state=state,
        recovery=recovery,
        trace=trace,
    )

    orchestrator.register(agent)

    assert orchestrator.has_agent("test-analytics-agent")
    assert orchestrator.list_agents() == ["test-analytics-agent"]

    result = orchestrator.run(
        "test-analytics-agent",
        AgentContext(
            task_id="orchestrated-task",
            input_data={"question": "market"},
        ),
    )

    assert result.success
    assert state.get("orchestrated-task").state == TaskState.COMPLETED

    execution_trace = trace.for_task("orchestrated-task")

    assert len(execution_trace) == 2
    assert execution_trace[0].event == "execution_started"
    assert execution_trace[1].event == "execution_completed"

    print("=" * 46)
    print(" AGENT CONTROL PLANE — MILESTONES 41–48")
    print("=" * 46)
    print("41 Agent Contract       : PASS")
    print("42 Tool Registry        : PASS")
    print("43 Permission Engine    : PASS")
    print("44 State Manager        : PASS")
    print("45 Execution Engine     : PASS")
    print("46 Retry / Recovery     : PASS")
    print("47 Trace / Observability: PASS")
    print("48 Agent Orchestrator   : PASS")
    print("----------------------------------------------")
    print("AGENT CONTROL PLANE : PASS")
    print("=" * 46)


if __name__ == "__main__":
    main()
