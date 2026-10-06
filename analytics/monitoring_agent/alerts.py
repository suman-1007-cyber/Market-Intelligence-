from __future__ import annotations

from typing import Any


def generate(
    threshold_result: dict[str, Any],
    anomaly_result: dict[str, Any],
) -> list[dict[str, Any]]:
    alerts = []

    if threshold_result.get("breached"):
        alerts.append({
            "type": "THRESHOLD_BREACH",
            "severity": "HIGH",
        })

    if anomaly_result.get("count", 0) > 0:
        alerts.append({
            "type": "ANOMALY",
            "severity": "MEDIUM",
        })

    return alerts
