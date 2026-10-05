def ingestion_quality_gate(rows, contract):
    from quality.contract_validation import validate_contract
    result = validate_contract(rows, contract)
    return {
        "status": "PASS" if result["valid"] else "BLOCK",
        "accepted": result["valid"],
        "errors": result["errors"],
        "warnings": result["warnings"],
        "rows": len(rows),
    }
