"""Missing-data analysis."""

from typing import Any

import pandas as pd


def analyze(frame: pd.DataFrame) -> dict[str, Any]:
    result = {}

    for column in frame.columns:
        missing = int(frame[column].isna().sum())
        total = len(frame)

        result[str(column)] = {
            "missing": missing,
            "total": int(total),
            "missing_pct": (
                round(missing / total * 100, 4)
                if total else 0.0
            ),
        }

    return result
