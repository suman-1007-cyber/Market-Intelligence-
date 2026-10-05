
def validate(rows):
    if not rows:
        return {
            "valid": False,
            "rows": [],
            "errors": ["empty_table"],
            "quality_score": 0.0
        }

    headers = list(rows[0].keys())
    errors = []
    cleaned = []

    if any(not str(h).strip() for h in headers):
        errors.append("blank_header")

    for number, row in enumerate(rows, 1):
        clean = {
            str(k).strip(): "" if v is None else str(v).strip()
            for k, v in row.items()
        }

        if not any(clean.values()):
            errors.append(f"empty_row:{number}")
            continue

        clean["_row_number"] = number
        cleaned.append(clean)

    score = len(cleaned) / len(rows) if rows else 0

    return {
        "valid": bool(cleaned) and not errors,
        "rows": cleaned,
        "headers": headers,
        "errors": errors,
        "quality_score": round(score, 4)
    }

def infer_types(rows):
    result = {}

    for key in rows[0] if rows else []:
        values = [
            r.get(key, "")
            for r in rows
            if str(r.get(key, "")).strip()
        ]

        numeric = 0

        for value in values:
            try:
                float(str(value).replace(",", ""))
                numeric += 1
            except Exception:
                pass

        result[key] = (
            "numeric"
            if values and numeric == len(values)
            else "text"
        )

    return result
