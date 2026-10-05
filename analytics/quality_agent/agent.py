"""Data Quality Agent orchestration."""

from dataclasses import dataclass
from typing import Any

import pandas as pd

from .anomalies import detect as detect_anomalies
from .duplicates import detect as detect_duplicates
from .inspector import inspect
from .investigator import investigate
from .missing import analyze as analyze_missing
from .schema import compare


@dataclass
class DataQualityAgent:
    """Deterministic data-quality investigation agent."""

    agent_id: str = "data-quality-agent"

    def analyze(
        self,
        frame: pd.DataFrame,
        expected_schema: dict[str, str] | None = None,
        duplicate_subset: list[str] | None = None,
    ) -> dict[str, Any]:
        inspection = inspect(frame)
        missing = analyze_missing(frame)
        duplicates = detect_duplicates(
            frame,
            subset=duplicate_subset,
        )
        anomalies = detect_anomalies(frame)

        actual_schema = inspection["column_types"]

        schema_result = compare(
            expected_schema or actual_schema,
            actual_schema,
        )

        findings = investigate(
            inspection,
            missing,
            duplicates,
            anomalies,
            schema_result,
        )

        return {
            "agent_id": self.agent_id,
            "inspection": inspection,
            "missing_data": missing,
            "duplicates": duplicates,
            "anomalies": anomalies,
            "schema": schema_result,
            "findings": findings,
        }
