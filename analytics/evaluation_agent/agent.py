from __future__ import annotations

from typing import Any

from .scoring import score
from .accuracy import calculate
from .failures import collect
from .regression import compare
from .reliability import assess
from .report import build
from .intelligence import analyze


class AgentEvaluationAgent:
    agent_id = "agent-evaluation-agent"

    def evaluate(
        self,
        cases: list[dict[str, Any]],
        actual_values: list[Any],
        previous_accuracy: float = 0.0,
    ) -> dict[str, Any]:
        results = []

        for case, actual in zip(cases, actual_values):
            result = score(case["expected"], actual)
            result["actual"] = actual
            results.append(result)

        scores = [result["score"] for result in results]
        accuracy = calculate(scores)
        failures = collect(cases, results)

        regression = compare(
            previous_accuracy,
            accuracy["accuracy"],
        )

        reliability = assess(
            accuracy["accuracy"],
            len(failures),
        )

        report = build(
            accuracy,
            reliability,
            failures,
        )

        intelligence = analyze(
            accuracy,
            reliability,
            regression,
        )

        return {
            "agent_id": self.agent_id,
            "results": results,
            "accuracy": accuracy,
            "failures": failures,
            "regression": regression,
            "reliability": reliability,
            "report": report,
            "intelligence": intelligence,
        }
