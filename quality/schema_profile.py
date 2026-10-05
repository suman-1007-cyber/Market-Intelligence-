def profile_dataset(rows):
    rows = list(rows)
    columns = sorted({k for r in rows for k in r})
    profile = {
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": {},
    }
    for col in columns:
        values = [r.get(col) for r in rows]
        non_null = [v for v in values if v is not None and v != ""]
        profile["columns"][col] = {
            "null_count": len(values) - len(non_null),
            "non_null_count": len(non_null),
            "unique_count": len({str(v) for v in non_null}),
            "null_rate": (len(values) - len(non_null)) / len(values) if values else 0.0,
        }
    return profile
