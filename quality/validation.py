import pandas as pd

REQUIRED_EVIDENCE = ["source", "retrieved_at"]

def validate_dataframe(df):
    result = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "numeric_columns": int(len(df.select_dtypes(include="number").columns)),
        "valid": True,
        "issues": []
    }

    if len(df.columns) == 0:
        result["valid"] = False
        result["issues"].append("No columns")

    if result["duplicate_rows"]:
        result["issues"].append("Duplicate rows detected")

    return result
