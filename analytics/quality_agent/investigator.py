"""Evidence-backed data quality investigation."""

from typing import Any


def investigate(
    inspection: dict[str, Any],
    missing: dict[str, Any],
    duplicates: dict[str, Any],
    anomalies: dict[str, Any],
    schema: dict[str, Any],
) -> list[dict[str, Any]]:
    findings = []

    if inspection["missing_cells"] > 0:
        findings.append({
            "type": "missing_data",
            "severity": "warning",
            "finding": (
                f"Dataset contains {inspection['missing_cells']} "
                "missing cell(s)."
            ),
            "evidence": missing,
        })

    if duplicates["has_duplicates"]:
        findings.append({
            "type": "duplicates",
            "severity": "warning",
            "finding": (
                f"Dataset contains {duplicates['duplicate_rows']} "
                "duplicate row(s)."
            ),
            "evidence": duplicates,
        })

    for column, detail in anomalies.items():
        if detail["outlier_count"] > 0:
            findings.append({
                "type": "anomaly",
                "severity": "warning",
                "finding": (
                    f"{column} contains "
                    f"{detail['outlier_count']} IQR outlier(s)."
                ),
                "evidence": detail,
            })

    if schema["drift"]:
        findings.append({
            "type": "schema_drift",
            "severity": "error",
            "finding": "Dataset schema differs from the expected schema.",
            "evidence": schema,
        })

    return findings
