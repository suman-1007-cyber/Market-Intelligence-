"""Deterministic numeric anomaly detection."""

from typing import Any

import pandas as pd


def detect(frame: pd.DataFrame) -> dict[str, Any]:
    result = {}

    for column in frame.select_dtypes(include="number").columns:
        series = pd.to_numeric(frame[column], errors="coerce").dropna()

        if series.empty:
            result[str(column)] = {
                "outlier_count": 0,
                "method": "iqr",
            }
            continue

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        mask = (series < lower) | (series > upper)

        result[str(column)] = {
            "outlier_count": int(mask.sum()),
            "lower_bound": lower,
            "upper_bound": upper,
            "method": "iqr",
        }

    return result
