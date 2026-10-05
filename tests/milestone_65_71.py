"""Integration test for Data Quality Agent milestones 65-71."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from analytics.quality_agent import DataQualityAgent


def main() -> None:
    print("=" * 46)
    print(" DATA QUALITY AGENT — MILESTONES 65–71")
    print("=" * 46)

    frame = pd.DataFrame({
        "product": ["A", "B", "B", "D"],
        "sales": [100.0, 150.0, 150.0, 1000.0],
        "customers": [10.0, None, 15.0, 20.0],
    })

    agent = DataQualityAgent()

    result = agent.analyze(
        frame,
        expected_schema={
            "product": "object",
            "sales": "float64",
            "customers": "float64",
        },
        duplicate_subset=["product"],
    )

    assert result["inspection"]["rows"] == 4
    assert result["inspection"]["columns"] == 3
    print("65 Quality Inspector       : PASS")

    assert result["inspection"]["missing_cells"] == 1
    assert result["missing_data"]["customers"]["missing"] == 1
    print("66 Missing Data Agent      : PASS")

    duplicate_check = result["duplicates"]

    assert duplicate_check["has_duplicates"]
    assert duplicate_check["duplicate_rows"] == 1
    print("67 Duplicate Detection     : PASS")

    assert result["anomalies"]["sales"]["outlier_count"] >= 1
    print("68 Anomaly / Data Error    : PASS")

    assert not result["schema"]["drift"]

    drift = agent.analyze(
        frame,
        expected_schema={
            "product": "object",
            "sales": "float64",
            "customers": "int64",
        },
    )["schema"]

    assert drift["drift"]
    assert "customers" in drift["type_changed"]
    print("69 Schema Drift Agent      : PASS")

    assert len(result["findings"]) >= 3
    assert all(
        "finding" in item and "evidence" in item
        for item in result["findings"]
    )
    print("70 Data Quality Investigator: PASS")

    assert result["agent_id"] == "data-quality-agent"
    assert isinstance(result["findings"], list)
    print("71 Data Quality Agent      : PASS")

    print("-" * 46)
    print("DATA QUALITY AGENT : PASS")
    print("=" * 46)


if __name__ == "__main__":
    main()
