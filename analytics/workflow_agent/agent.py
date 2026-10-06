from __future__ import annotations

from typing import Any

from .workflow import create
from .planner import plan
from .validation import validate
from .sequencer import sequence
from .results import record
from .recovery import recover
from .status import assess
from .intelligence import analyze


class WorkflowActionAgent:
    agent_id = "workflow-action-agent"

    def execute(
        self,
        workflow_id: str,
        actions: list[dict[str, Any]],
        results: list[dict[str, Any]] | None = None,
        retryable: bool = True,
    ) -> dict[str, Any]:
        workflow = create(workflow_id, actions)
        planned = plan(actions)
        validation = validate(planned)

        if validation["valid"]:
            ordered = sequence(planned)
        else:
            ordered = planned

        action_results = results or []

        recovery = [
            recover(result, retryable=retryable)
            for result in action_results
        ]

        workflow_status = assess(
            action_results,
            len(ordered),
        )

        intelligence = analyze(
            validation,
            workflow_status,
            recovery,
        )

        return {
            "agent_id": self.agent_id,
            "workflow": workflow,
            "planned": planned,
            "ordered": ordered,
            "validation": validation,
            "results": action_results,
            "recovery": recovery,
            "status": workflow_status,
            "intelligence": intelligence,
        }
