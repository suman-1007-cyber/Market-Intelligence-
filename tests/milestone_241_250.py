from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.workflow_agent.workflow import create
from analytics.workflow_agent.planner import plan
from analytics.workflow_agent.validation import validate
from analytics.workflow_agent.dependencies import resolve
from analytics.workflow_agent.sequencer import sequence
from analytics.workflow_agent.results import record
from analytics.workflow_agent.recovery import recover
from analytics.workflow_agent.status import assess
from analytics.workflow_agent.intelligence import analyze
from analytics.workflow_agent.agent import WorkflowActionAgent


actions = [
    {
        "action_id": "a",
        "name": "collect_data",
    },
    {
        "action_id": "b",
        "name": "analyze_data",
        "depends_on": ["a"],
    },
]

workflow = create("workflow-1", actions)
assert workflow["workflow_id"] == "workflow-1"
assert workflow["action_count"] == 2

planned = plan(actions)
assert planned[0]["sequence"] == 1
assert planned[0]["status"] == "PLANNED"

validation = validate(planned)
assert validation["valid"] is True
assert validation["errors"] == []

invalid = validate([{"name": "missing_id"}])
assert invalid["valid"] is False

resolved = resolve([
    {
        "action_id": "a",
        "name": "collect",
        "status": "COMPLETED",
    },
    {
        "action_id": "b",
        "name": "analyze",
        "depends_on": ["a"],
        "status": "PLANNED",
    },
])

assert resolved[1]["ready"] is True

ordered = sequence(actions)
assert [item["action_id"] for item in ordered] == ["a", "b"]

result_ok = record(
    "a",
    True,
    output={"rows": 10},
)
assert result_ok["status"] == "COMPLETED"

result_fail = record(
    "b",
    False,
    error="temporary failure",
)
assert result_fail["status"] == "FAILED"

recovery_retry = recover(
    result_fail,
    retryable=True,
)
assert recovery_retry["recovery_action"] == "RETRY"

recovery_stop = recover(
    result_fail,
    retryable=False,
)
assert recovery_stop["recovery_action"] == "STOP"

status = assess(
    [result_ok, result_fail],
    total_actions=2,
)
assert status["status"] == "FAILED"
assert status["completed"] == 1
assert status["failed"] == 1

intel = analyze(
    validation,
    status,
    [recovery_retry],
)
assert intel["workflow_status"] == "FAILED"
assert intel["retry_count"] == 1
assert intel["needs_attention"] is True

agent_result = WorkflowActionAgent().execute(
    workflow_id="workflow-1",
    actions=actions,
    results=[
        result_ok,
        result_fail,
    ],
)

assert agent_result["agent_id"] == "workflow-action-agent"
assert agent_result["validation"]["valid"] is True
assert agent_result["ordered"][0]["action_id"] == "a"
assert agent_result["ordered"][1]["action_id"] == "b"
assert agent_result["status"]["status"] == "FAILED"
assert agent_result["intelligence"]["needs_attention"] is True

print("241 Workflow Definition             : PASS")
print("242 Action Planning                 : PASS")
print("243 Action Validation               : PASS")
print("244 Dependency Resolution           : PASS")
print("245 Execution Sequencing            : PASS")
print("246 Action Result Tracking          : PASS")
print("247 Recovery Handling               : PASS")
print("248 Workflow Status                 : PASS")
print("249 Workflow Intelligence            : PASS")
print("250 Workflow / Action Agent         : PASS")
print("MILESTONE 241-250 : PASS")
