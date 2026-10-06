from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.root_cause_agent import (
    prepare,
    correlation,
    analyze,
    analyze_drivers,
    rank,
    RootCauseInvestigator,
)


target = [10, 20, 30, 40, 50]

drivers = {
    "marketing": [1, 2, 3, 4, 5],
    "price": [5, 4, 3, 2, 1],
    "noise": [2, 5, 1, 4, 3],
}

prepared = prepare(target, drivers)

assert prepared["rows"] == 5
assert prepared["driver_count"] == 3

positive = correlation(
    target,
    drivers["marketing"],
)

negative = correlation(
    target,
    drivers["price"],
)

assert abs(positive - 1.0) < 1e-9
assert abs(negative + 1.0) < 1e-9

cause_effect = analyze(target, drivers)

assert cause_effect["marketing"]["direction"] == "POSITIVE"
assert cause_effect["price"]["direction"] == "NEGATIVE"

driver_analysis = analyze_drivers(cause_effect)

assert driver_analysis[0]["driver"] in {"marketing", "price"}
assert driver_analysis[0]["absolute_correlation"] == 1.0

ranked = rank(driver_analysis)

assert ranked[0]["rank"] == 1
assert ranked[0]["strength"] == "HIGH"

investigator = RootCauseInvestigator()

result = investigator.investigate(
    target,
    drivers,
)

assert result["agent_id"] == "root_cause_investigator"
assert "cause_effect" in result
assert "drivers" in result
assert "ranked_causes" in result
assert len(result["ranked_causes"]) == 3

print("141 Root Cause Data Preparation : PASS")
print("142 Cause & Effect Detection    : PASS")
print("143 Driver Analysis             : PASS")
print("144 Root Cause Ranking          : PASS")
print("145 Root Cause Investigation    : PASS")
print("MILESTONE 141-145 : PASS")
