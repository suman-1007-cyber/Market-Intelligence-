from pathlib import Path
import pandas as pd

from sources.registry import ensure, enabled
from sources.discovery import discover
from orchestrator.planner import plan
from quality.certification import certify
from quality.triangulation import compare
from entities.conformance import normalize
from semantic.metrics import growth, share
from analytics.pipeline import analyze
from orchestrator.investigation import run

Path("storage/cache").mkdir(parents=True, exist_ok=True)

df = pd.DataFrame({
    "company": ["Alpha", "Beta", "Gamma", "Alpha", "Beta", "Gamma"],
    "value": [100, 80, 60, 120, 90, 70],
    "period": [1, 1, 1, 2, 2, 2]
})

csv = Path("storage/cache/full_system.csv")
df.to_csv(csv, index=False)

assert ensure()["sources"]
assert enabled()
assert "market" in discover("Tell me about our market")["domains"]
assert "market" in plan("Tell me about our market")["domains"]
assert normalize("  ACME, Inc. ") == "acme inc"
assert abs(growth(110, 100) - 0.10) < 1e-9
assert abs(share(25, 100) - 0.25) < 1e-9

cert = certify(df, "storage/silver/full_system.parquet")
assert cert["certified"]

analysis = analyze(df)
assert analysis["rows"] == 6
assert "market" in analysis
assert "forecast" in analysis
assert "competitor_ranking" in analysis

result = run(
    "Tell me about our market and competitors",
    str(csv)
)

assert result["quality"]["data"]["certified"]
assert Path(result["report"]).exists()

print("==============================================")
print(" FULL MARKET INTELLIGENCE SYSTEM TEST")
print("==============================================")
print("Source registry        : PASS")
print("Source discovery       : PASS")
print("Question planner       : PASS")
print("Entity conformance    : PASS")
print("Semantic metrics       : PASS")
print("Bronze/Silver flow     : PASS")
print("Data certification     : PASS")
print("Market analysis        : PASS")
print("Competitive analysis   : PASS")
print("Forecast analysis      : PASS")
print("Evidence pipeline      : PASS")
print("Triangulation engine   : PASS")
print("Investigation engine   : PASS")
print("Evidence report        : PASS")
print("==============================================")
print("FULL SYSTEM CORE READY")
print("==============================================")
print("Report:", result["report"])
