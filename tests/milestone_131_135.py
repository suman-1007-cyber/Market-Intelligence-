from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.forecasting_agent import (
    prepare,
    decompose,
    detect,
    select,
    forecast,
)


values = [100, 110, 120, 130, 140]

prepared = prepare(values)
assert prepared["valid"]
assert prepared["count"] == 5
assert prepared["last"] == 140.0

decomposition = decompose(values)
assert len(decomposition["trend"]) == 5
assert len(decomposition["residual"]) == 5

seasonality = detect(values, period=2)
assert isinstance(seasonality["detected"], bool)
assert 0.0 <= seasonality["strength"] <= 1.0

selection = select(
    trend_detected=True,
    seasonality_detected=False,
    history_length=len(values),
)
assert selection["selected_model"] == "TREND_BASELINE"

baseline = forecast(
    values,
    periods=3,
    model="TREND_BASELINE",
)
assert baseline["predictions"] == [150.0, 160.0, 170.0]

print("131 Forecast Data Preparation : PASS")
print("132 Time-Series Decomposition : PASS")
print("133 Trend & Seasonality       : PASS")
print("134 Forecast Model Selection  : PASS")
print("135 Baseline Forecast Engine  : PASS")
print("MILESTONE 131-135 : PASS")
