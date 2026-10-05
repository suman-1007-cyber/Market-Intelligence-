from semantic.schema_inference import infer_schema
from semantic.field_classification import classify_field
from quality.schema_profile import profile_dataset
from quality.contract_validation import validate_contract
from quality.schema_drift import detect_schema_drift
from quality.ingestion_gate import ingestion_quality_gate

def build_contract(rows, name="dataset", version="1.0"):
    schema = infer_schema(rows)
    fields = []
    for item in schema:
        fields.append({
            **item,
            "semantic_type": classify_field(item["name"], item["data_type"]),
        })

    return {
        "name": name,
        "version": version,
        "fields": fields,
        "primary_key": [],
        "time_fields": [f["name"] for f in fields if f["semantic_type"] == "time"],
        "entity_fields": [f["name"] for f in fields if f["semantic_type"] == "entity"],
        "measure_fields": [f["name"] for f in fields if f["semantic_type"] == "measure"],
        "dimension_fields": [f["name"] for f in fields if f["semantic_type"] == "dimension"],
    }

def run_pipeline(rows, previous_contract=None):
    contract = build_contract(rows)
    profile = profile_dataset(rows)
    validation = validate_contract(rows, contract)
    gate = ingestion_quality_gate(rows, contract)
    drift = detect_schema_drift(previous_contract, contract) if previous_contract else {
        "drift": False, "added": [], "removed": [], "changed": []
    }
    return {
        "contract": contract,
        "profile": profile,
        "validation": validation,
        "quality_gate": gate,
        "schema_drift": drift,
    }
