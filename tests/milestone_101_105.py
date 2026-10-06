"""Milestones 101-105: Customer Intelligence foundation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.customer_agent.churn import analyze as analyze_churn
from analytics.customer_agent.cohorts import analyze as analyze_cohorts
from analytics.customer_agent.profiling import profile
from analytics.customer_agent.retention import analyze as analyze_retention
from analytics.customer_agent.segmentation import segment


records = [
    {
        "customer": "Alpha",
        "revenue": 1000,
        "units": 10,
        "cohort": "2026-Q1",
    },
    {
        "customer": "Beta",
        "revenue": 600,
        "units": 6,
        "cohort": "2026-Q1",
    },
    {
        "customer": "Gamma",
        "revenue": 300,
        "units": 3,
        "cohort": "2026-Q2",
    },
    {
        "customer": "Delta",
        "revenue": 100,
        "units": 1,
        "cohort": "2026-Q2",
    },
]

segments = segment(records)

assert len(segments) == 4
assert segments[0]["customer"] == "Alpha"
assert segments[0]["segment"] == "HIGH_VALUE"
assert segments[-1]["segment"] == "LOW_VALUE"

profiles = profile(records)

assert len(profiles) == 4
assert profiles[0]["customer"] == "Alpha"
assert abs(profiles[0]["revenue"] - 1000.0) < 1e-9
assert profiles[0]["orders"] == 1
assert abs(profiles[0]["average_order_value"] - 1000.0) < 1e-9

cohorts = analyze_cohorts(records)

assert len(cohorts) == 2
assert cohorts[0]["cohort"] == "2026-Q1"
assert cohorts[0]["customers"] == 2
assert cohorts[1]["customers"] == 2

previous = {"Alpha", "Beta", "Gamma"}
current = {"Alpha", "Beta", "Delta"}

retention = analyze_retention(
    current,
    previous,
)

assert retention["retained_customers"] == 2
assert abs(retention["retention_rate"] - (2 / 3)) < 1e-6

churn = analyze_churn(
    current,
    previous,
)

assert churn["churned_customers"] == 1
assert churn["churned_customer_ids"] == ["Gamma"]
assert abs(churn["churn_rate"] - (1 / 3)) < 1e-6

print("101 Customer Segmentation       : PASS")
print("102 Customer Profiling          : PASS")
print("103 Customer Cohort Analysis    : PASS")
print("104 Customer Retention Analysis : PASS")
print("105 Customer Churn Analysis     : PASS")
print("==============================================")
print("MILESTONE 101-105 : PASS")
print("==============================================")
