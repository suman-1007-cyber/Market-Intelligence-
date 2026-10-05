def validate_contract(rows, contract):
    errors = []
    warnings = []
    fields = {f["name"]: f for f in contract.get("fields", [])}

    actual = {k for r in rows for k in r}
    required = set(fields)

    missing = sorted(required - actual)
    unexpected = sorted(actual - required)

    for field in missing:
        errors.append({"type": "MISSING_FIELD", "field": field})

    for field in unexpected:
        warnings.append({"type": "UNEXPECTED_FIELD", "field": field})

    for row_no, row in enumerate(rows, 1):
        for name, spec in fields.items():
            value = row.get(name)
            if value is None or value == "":
                if not spec.get("nullable", True):
                    errors.append({"type": "NULL_NOT_ALLOWED", "field": name, "row": row_no})

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "checked_rows": len(rows),
    }
