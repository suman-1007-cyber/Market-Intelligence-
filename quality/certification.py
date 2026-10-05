from pathlib import Path
import pandas as pd
from storage.parquet import write

def certify(df, output="storage/silver/certified.parquet"):
    issues = []

    if df.empty:
        issues.append("Dataset is empty")

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count:
        issues.append(f"{duplicate_count} duplicate rows")

    missing_cells = int(df.isna().sum().sum())

    result = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicates": duplicate_count,
        "missing_cells": missing_cells,
        "issues": issues,
        "certified": len(df) > 0 and duplicate_count == 0
    }

    if result["certified"]:
        write(df, output)

    return result
