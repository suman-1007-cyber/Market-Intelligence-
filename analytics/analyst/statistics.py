"""Deterministic statistical analysis."""

from typing import Any

import pandas as pd


def analyze(frame: pd.DataFrame) -> dict[str, Any]:
    result = {}

    for column in frame.select_dtypes(include="number").columns:
        series = pd.to_numeric(frame[column], errors="coerce").dropna()

        if series.empty:
            continue

        result[str(column)] = {
            "count": int(series.count()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std(ddof=1)) if len(series) > 1 else 0.0,
            "min": float(series.min()),
            "max": float(series.max()),
            "sum": float(series.sum()),
        }

    return result
