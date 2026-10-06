from __future__ import annotations

from typing import Any


def analyze(
    change: dict[str, Any],
    threshold: dict[str, Any],
    anomalies: dict[str, Any],
    alerts: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "direction": change["direction"],
        "change_rate": change["change_rate"],
        "threshold_breached": threshold["breached"],
        "anomaly_count": anomalies["count"],
        "alert_count": len(alerts),
    }
