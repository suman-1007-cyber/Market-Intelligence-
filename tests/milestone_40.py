import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Milestone 40 — Agent Runtime tests."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents import Agent, AgentContext, AgentResult, AgentStatus


class EchoAgent(Agent):
    """Small deterministic test agent."""

    name = "echo-test-agent"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult.ok(
            context.input_data,
            task_id=context.task_id,
        )


class FailingAgent(Agent):
    """Test agent for controlled failure handling."""

    name = "failing-test-agent"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult.failure(
            "controlled test failure",
            task_id=context.task_id,
        )


def main() -> None:
    agent = EchoAgent()

    assert agent.status == AgentStatus.CREATED

    context = AgentContext(
        task_id="milestone-40-test",
        input_data={"question": "test"},
    )

    agent.prepare(context)
    assert agent.status == AgentStatus.READY

    result = agent.execute()
    assert result.success is True
    assert result.data == {"question": "test"}
    assert agent.status == AgentStatus.COMPLETED

    failed = FailingAgent()
    failed_result = failed.execute(
        AgentContext(
            task_id="milestone-40-failure-test",
            input_data="failure",
        )
    )

    assert failed_result.success is False
    assert failed_result.error == "controlled test failure"
    assert failed.status == AgentStatus.FAILED

    cancelled = EchoAgent()
    cancelled.cancel()
    assert cancelled.status == AgentStatus.CANCELLED

    print("=" * 46)
    print(" MILESTONE 40 — AGENT RUNTIME")
    print("=" * 46)
    print("Agent contract       : PASS")
    print("Context model        : PASS")
    print("Result model         : PASS")
    print("Lifecycle management : PASS")
    print("Successful execution : PASS")
    print("Failure handling     : PASS")
    print("Cancellation         : PASS")
    print("----------------------------------------------")
    print("MILESTONE 40 : PASS")
    print("=" * 46)


if __name__ == "__main__":
    main()
