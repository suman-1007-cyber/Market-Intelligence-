"""Deterministic relationship and correlation analysis."""

from typing import Any

import pandas as pd


def analyze(frame: pd.DataFrame) -> dict[str, Any]:
    numeric = frame.select_dtypes(include="number")

    if numeric.shape[1] < 2:
        return {"correlations": [], "strongest": None}

    corr = numeric.corr()

    pairs = []
    columns = list(corr.columns)

    for i, left in enumerate(columns):
        for right in columns[i + 1:]:
            value = corr.loc[left, right]
            if pd.isna(value):
                continue
            pairs.append({
                "left": str(left),
                "right": str(right),
                "correlation": float(value),
                "absolute_correlation": float(abs(value)),
            })

    pairs.sort(key=lambda item: item["absolute_correlation"], reverse=True)

    return {
        "correlations": pairs,
        "strongest": pairs[0] if pairs else None,
    }
