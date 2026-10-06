from __future__ import annotations

from typing import Any

from .findings import collect
from .prioritization import prioritize
from .evidence import attach
from .report import build as build_report
from .intelligence import summarize


class ReportingExecutiveAgent:
    agent_id = "reporting-executive-agent"

    def analyze(
        self,
        findings: list[dict[str, Any]],
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        collected = collect(findings)
        prioritized = prioritize(collected["findings"])
        linked = attach(prioritized, evidence)
        report = build_report(linked, evidence)

        return {
            "agent_id": self.agent_id,
            "report": report,
            "intelligence": summarize(linked),
        }
