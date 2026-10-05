"""Deterministic distribution analysis."""

from typing import Any

import pandas as pd


def analyze(frame: pd.DataFrame) -> dict[str, Any]:
    result = {}

    for column in frame.select_dtypes(include="number").columns:
        series = pd.to_numeric(frame[column], errors="coerce").dropna()

        if series.empty:
            continue

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]

        result[str(column)] = {
            "q1": q1,
            "median": float(series.median()),
            "q3": q3,
            "iqr": float(iqr),
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_count": int(len(outliers)),
            "outlier_pct": round(float(len(outliers) / len(series) * 100), 4),
        }

    return result
