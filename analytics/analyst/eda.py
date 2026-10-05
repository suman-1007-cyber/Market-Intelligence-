"""Deterministic automatic exploratory data analysis."""

from typing import Any

import pandas as pd


def profile(frame: pd.DataFrame) -> dict[str, Any]:
    numeric = frame.select_dtypes(include="number")
    categorical = frame.select_dtypes(exclude="number")

    columns = {}
    for name in frame.columns:
        series = frame[name]
        columns[str(name)] = {
            "dtype": str(series.dtype),
            "rows": int(len(series)),
            "missing": int(series.isna().sum()),
            "missing_pct": round(float(series.isna().mean() * 100), 4),
            "unique": int(series.nunique(dropna=True)),
        }

    return {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "numeric_columns": [str(c) for c in numeric.columns],
        "categorical_columns": [str(c) for c in categorical.columns],
        "columns_detail": columns,
    }
