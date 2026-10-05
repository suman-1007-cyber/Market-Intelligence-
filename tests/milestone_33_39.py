import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orchestrator.pipeline_33_39 import run_pipeline, build_contract

rows = [
    {"company": "Alpha", "region": "India", "year": 2024, "revenue": 1000},
    {"company": "Beta", "region": "India", "year": 2025, "revenue": 1250},
]

result = run_pipeline(rows)
contract = result["contract"]

assert contract["name"] == "dataset"
assert "company" in contract["entity_fields"]
assert "region" in [f["name"] for f in contract["fields"] if f["semantic_type"] == "geography"]
assert "year" in contract["time_fields"]
assert "revenue" in contract["measure_fields"]
assert result["profile"]["row_count"] == 2
assert result["profile"]["column_count"] == 4
assert result["validation"]["valid"] is True
assert result["quality_gate"]["status"] == "PASS"

previous = build_contract([
    {"company": "A", "year": 2024, "revenue": 10}
])
drift = run_pipeline(rows, previous)["schema_drift"]
assert drift["drift"] is True
assert "region" in drift["added"]

bad_rows = [
    {"company": "A", "year": 2024}
]
bad_contract = {
    "fields": [
        {"name": "company", "data_type": "string", "nullable": False},
        {"name": "revenue", "data_type": "numeric", "nullable": False},
    ]
}
from quality.contract_validation import validate_contract
bad = validate_contract(bad_rows, bad_contract)
assert bad["valid"] is False

print("=" * 46)
print(" MARKET INTELLIGENCE MILESTONES 33-39")
print("=" * 46)
print("33 Data Contract model          : PASS")
print("34 Schema inference             : PASS")
print("35 Dataset profiling            : PASS")
print("36 Semantic field classification: PASS")
print("37 Contract validation          : PASS")
print("38 Schema drift detection       : PASS")
print("39 Ingestion quality gate       : PASS")
print("----------------------------------------------")
print("MILESTONES 33-39 : PASS")
print("----------------------------------------------")
print("Data Contract & Schema Intelligence READY")
print("=" * 46)
