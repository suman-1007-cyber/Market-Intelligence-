def required_columns(df, columns):
    missing = [c for c in columns if c not in df.columns]
    return {"valid": not missing, "missing": missing}
