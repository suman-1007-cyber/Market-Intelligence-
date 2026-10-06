from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.monitoring_agent.baseline import establish
from analytics.monitoring_agent.change import detect
from analytics.monitoring_agent.thresholds import check
from analytics.monitoring_agent.anomalies import detect as detect_anomalies
from analytics.monitoring_agent.freshness import check as check_freshness
from analytics.monitoring_agent.alerts import generate
from analytics.monitoring_agent.status import summarize
from analytics.monitoring_agent.intelligence import analyze
from analytics.monitoring_agent.agent import ContinuousMonitoringAgent


values = [100, 110, 120, 130]

baseline = establish(values)
assert baseline["count"] == 4
assert baseline["latest"] == 130
assert abs(baseline["mean"] - 115) < 1e-9

change = detect(120, 130)
assert change["direction"] == "UP"
assert change["change"] == 10
assert abs(change["change_rate"] - (10 / 120)) < 1e-9

threshold = check(130, minimum=90, maximum=125)
assert threshold["breached"] is True
assert threshold["status"] == "BREACH"

anomalies = detect_anomalies([10, 10, 10, 30], threshold=1.5)
assert anomalies["count"] == 1
assert anomalies["anomalies"] == [3]

freshness = check_freshness(
    "2026-01-01T00:00:00+00:00",
    maximum_age_seconds=10**12,
)
assert freshness["fresh"] is True

alerts = generate(threshold, anomalies)
assert len(alerts) == 2
assert alerts[0]["type"] == "THRESHOLD_BREACH"
assert alerts[1]["type"] == "ANOMALY"

status = summarize(alerts, True)
assert status["status"] == "ALERT"
assert status["alert_count"] == 2

intel = analyze(change, threshold, anomalies, alerts)
assert intel["direction"] == "UP"
assert intel["threshold_breached"] is True
assert intel["anomaly_count"] == 1

result = ContinuousMonitoringAgent().analyze(
    values,
    minimum=90,
    maximum=125,
    anomaly_threshold=1.5,
    fresh=True,
)

assert result["agent_id"] == "continuous-monitoring-agent"
assert result["status"]["status"] == "ALERT"
assert result["intelligence"]["alert_count"] == 1

print("181 Monitoring Baseline           : PASS")
print("182 Change Detection               : PASS")
print("183 Threshold Monitoring           : PASS")
print("184 Anomaly Detection              : PASS")
print("185 Freshness Monitoring            : PASS")
print("186 Alert Generation                : PASS")
print("187 Monitoring Status               : PASS")
print("188 Monitoring Intelligence         : PASS")
print("189 Monitoring Integration          : PASS")
print("190 Continuous Monitoring Agent     : PASS")
print("MILESTONE 181-190 : PASS")
