"""Data Analyst Agent orchestration."""

from dataclasses import dataclass
from typing import Any

import pandas as pd

from .eda import profile
from .findings import AnalystFinding
from .insights import detect
from .relationships import analyze as analyze_relationships
from .statistics import analyze as analyze_statistics
from .distributions import analyze as analyze_distributions


@dataclass
class DataAnalyst:
    """Deterministic analyst over a tabular dataset."""

    agent_id: str = "data-analyst"

    def analyze(self, frame: pd.DataFrame) -> dict[str, Any]:
        dataset_profile = profile(frame)
        statistics = analyze_statistics(frame)
        relationships = analyze_relationships(frame)
        distributions = analyze_distributions(frame)

        raw_findings = detect(
            dataset_profile,
            statistics,
            relationships,
            distributions,
        )

        findings = [
            AnalystFinding(
                finding=item["finding"],
                finding_type=item["type"],
                evidence=item["evidence"],
                calculation="Deterministic pandas calculation.",
            ).to_dict()
            for item in raw_findings
        ]

        return {
            "agent_id": self.agent_id,
            "profile": dataset_profile,
            "statistics": statistics,
            "relationships": relationships,
            "distributions": distributions,
            "findings": findings,
        }
