from datetime import date, datetime

def infer_data_type(values):
    vals = [v for v in values if v is not None and v != ""]
    if not vals:
        return "unknown"
    if all(isinstance(v, bool) for v in vals):
        return "boolean"
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals):
        return "numeric"
    if all(isinstance(v, (datetime, date)) for v in vals):
        return "datetime"
    return "string"

def infer_schema(rows):
    if not rows:
        return []
    names = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                names.append(key)
    result = []
    for name in names:
        values = [row.get(name) for row in rows]
        non_null = [v for v in values if v is not None and v != ""]
        result.append({
            "name": name,
            "data_type": infer_data_type(values),
            "nullable": len(non_null) != len(values),
            "sample_count": len(non_null),
            "unique_count": len({str(v) for v in non_null}),
        })
    return result
