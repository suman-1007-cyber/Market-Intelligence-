"""Integration test for Data Analyst Agent milestones 49-56."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from analytics.analyst import DataAnalyst
from analytics.analyst.discovery import discover


def main() -> None:
    print("=" * 46)
    print(" DATA ANALYST AGENT — MILESTONES 49–56")
    print("=" * 46)

    test_dir = Path("storage/cache/analyst_test")
    test_dir.mkdir(parents=True, exist_ok=True)

    csv_path = test_dir / "sample.csv"
    csv_path.write_text(
        "product,sales,customers\n"
        "A,100,10\n"
        "B,150,15\n"
        "C,200,20\n"
        "D,500,25\n"
    )

    discovered = discover(test_dir)
    assert any(item["name"] == "sample.csv" for item in discovered)
    print("49 Dataset Discovery       : PASS")

    frame = pd.read_csv(csv_path)

    analyst = DataAnalyst()
    result = analyst.analyze(frame)

    assert result["profile"]["rows"] == 4
    assert result["profile"]["columns"] == 3
    print("50 Automatic EDA           : PASS")

    assert "sales" in result["statistics"]
    assert result["statistics"]["sales"]["mean"] == 237.5
    print("51 Statistical Analysis    : PASS")

    assert result["relationships"]["strongest"] is not None
    print("52 Relationship Analysis   : PASS")

    assert "sales" in result["distributions"]
    assert result["distributions"]["sales"]["outlier_count"] >= 1
    print("53 Distribution Analysis   : PASS")

    assert result["findings"]
    print("54 Insight Detection       : PASS")

    finding = result["findings"][0]
    assert "finding" in finding
    assert "evidence" in finding
    assert "calculation" in finding
    print("55 Evidence-backed Findings: PASS")

    assert result["agent_id"] == "data-analyst"
    assert isinstance(result["findings"], list)
    print("56 Data Analyst Agent      : PASS")

    print("-" * 46)
    print("DATA ANALYST AGENT : PASS")
    print("=" * 46)


if __name__ == "__main__":
    main()
