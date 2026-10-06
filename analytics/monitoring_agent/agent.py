from __future__ import annotations

from typing import Any

from .baseline import establish
from .change import detect
from .thresholds import check as check_threshold
from .anomalies import detect as detect_anomalies
from .alerts import generate
from .status import summarize
from .intelligence import analyze


class ContinuousMonitoringAgent:
    agent_id = "continuous-monitoring-agent"

    def analyze(
        self,
        values: list[float],
        minimum: float | None = None,
        maximum: float | None = None,
        anomaly_threshold: float = 2.0,
        fresh: bool = True,
    ) -> dict[str, Any]:
        baseline = establish(values)
        change = detect(values[-2], values[-1]) if len(values) >= 2 else {
            "previous": values[-1],
            "current": values[-1],
            "change": 0.0,
            "change_rate": 0.0,
            "direction": "FLAT",
        }
        threshold = check_threshold(values[-1], minimum, maximum)
        anomalies = detect_anomalies(values, anomaly_threshold)
        alerts = generate(threshold, anomalies)
        status = summarize(alerts, fresh)

        return {
            "agent_id": self.agent_id,
            "baseline": baseline,
            "change": change,
            "threshold": threshold,
            "anomalies": anomalies,
            "alerts": alerts,
            "status": status,
            "intelligence": analyze(
                change,
                threshold,
                anomalies,
                alerts,
            ),
        }
