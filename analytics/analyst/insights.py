"""Deterministic insight detection."""

from typing import Any


def detect(
    profile: dict[str, Any],
    statistics: dict[str, Any],
    relationships: dict[str, Any],
    distributions: dict[str, Any],
) -> list[dict[str, Any]]:
    findings = []

    for column, stats in statistics.items():
        if stats["max"] > stats["min"]:
            change = stats["max"] - stats["min"]
            findings.append({
                "type": "range",
                "column": column,
                "finding": f"{column} spans {change:g} units.",
                "value": change,
                "evidence": {
                    "min": stats["min"],
                    "max": stats["max"],
                },
            })

    strongest = relationships.get("strongest")
    if strongest:
        findings.append({
            "type": "relationship",
            "columns": [
                strongest["left"],
                strongest["right"],
            ],
            "finding": (
                f"{strongest['left']} and {strongest['right']} "
                f"have correlation {strongest['correlation']:.4f}."
            ),
            "value": strongest["correlation"],
            "evidence": strongest,
        })

    for column, distribution in distributions.items():
        if distribution["outlier_count"]:
            findings.append({
                "type": "outlier",
                "column": column,
                "finding": (
                    f"{column} contains "
                    f"{distribution['outlier_count']} IQR outlier(s)."
                ),
                "value": distribution["outlier_count"],
                "evidence": distribution,
            })

    for column, detail in profile["columns_detail"].items():
        if detail["missing"] > 0:
            findings.append({
                "type": "missing_data",
                "column": column,
                "finding": (
                    f"{column} contains {detail['missing']} "
                    f"missing value(s)."
                ),
                "value": detail["missing"],
                "evidence": detail,
            })

    return findings
