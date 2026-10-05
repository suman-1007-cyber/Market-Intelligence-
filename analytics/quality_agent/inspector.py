"""Deterministic dataset quality inspection."""

from typing import Any

import pandas as pd


def inspect(frame: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "column_names": [str(column) for column in frame.columns],
        "duplicate_rows": int(frame.duplicated().sum()),
        "missing_cells": int(frame.isna().sum().sum()),
        "column_types": {
            str(column): str(dtype)
            for column, dtype in frame.dtypes.items()
        },
    }
