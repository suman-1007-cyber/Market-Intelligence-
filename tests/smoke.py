from pathlib import Path
import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from storage.parquet import write, read
from quality.validation import validate_dataframe
from analytics.market.engine import market_share, market_summary
from analytics.competitive.engine import concentration
from analytics.forecasting.engine import linear_forecast
from analytics.customer.engine import customer_summary
from analytics.pricing.engine import pricing_summary
from analytics.geographic.engine import geography_summary
from analytics.financial.engine import financial_summary
from analytics.trends.engine import growth
from analytics.scenarios.engine import scenario
from analytics.opportunity_risk import assess
from visualization.charts import line, bar
from orchestrator.planner import plan

for directory in [
    "storage/bronze",
    "storage/silver",
    "storage/gold",
    "storage/cache",
    "evidence",
    "reports"
]:
    Path(directory).mkdir(parents=True, exist_ok=True)

df = pd.DataFrame({
    "company": ["A", "B", "C", "A", "B", "C"],
    "value": [100, 80, 60, 120, 90, 70],
    "period": [1, 1, 1, 2, 2, 2],
    "customer": ["x", "y", "z", "x", "y", "z"],
    "price": [10, 12, 15, 11, 13, 16],
    "geography": ["India", "India", "India", "India", "India", "India"],
    "revenue": [100, 80, 60, 120, 90, 70]
})

parquet = write(df, "storage/bronze/smoke.parquet")
loaded = read(parquet)

assert len(loaded) == 6
assert validate_dataframe(loaded)["valid"]
assert len(market_share(loaded)) == 3
assert market_summary(loaded)["total_market"] == 520.0
assert "hhi" in concentration(loaded)
assert len(linear_forecast([10, 12, 14, 16], 4)) == 4
assert customer_summary(loaded)["unique_customers"] == 3
assert pricing_summary(loaded)["average_price"] > 0
assert len(geography_summary(loaded)) == 1
assert financial_summary(loaded)["total_revenue"] == 520.0
assert len(growth(loaded)) == 2
assert abs(scenario(100, {"base": 0.10})["base"] - 110.0) < 1e-9
assert isinstance(assess(growth=0.15)["opportunities"], list)
assert line([10, 12, 14, 16], "reports/smoke_trend.svg").exists()
assert bar(["A", "B"], [100, 80], "reports/smoke_bar.svg").exists()
assert "market" in plan("Tell me about our market")["domains"]

print("==============================================")
print(" MARKET INTELLIGENCE ENGINE SMOKE TEST")
print("==============================================")
print("Parquet storage       : PASS")
print("Data validation       : PASS")
print("Market analytics      : PASS")
print("Competitive analytics : PASS")
print("Customer analytics    : PASS")
print("Financial analytics   : PASS")
print("Pricing analytics     : PASS")
print("Geographic analytics  : PASS")
print("Trend analytics       : PASS")
print("Forecast engine       : PASS")
print("Scenario engine       : PASS")
print("Opportunity/Risk      : PASS")
print("Question planner      : PASS")
print("SVG visualization     : PASS")
print("==============================================")
print("CORE FOUNDATION READY")
print("==============================================")
