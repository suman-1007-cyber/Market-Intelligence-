"""Duplicate-row detection."""

from typing import Any

import pandas as pd


def detect(
    frame: pd.DataFrame,
    subset: list[str] | None = None,
) -> dict[str, Any]:
    if subset is not None:
        missing = [column for column in subset if column not in frame.columns]
        if missing:
            raise KeyError(f"Duplicate subset columns not found: {missing}")

    mask = frame.duplicated(subset=subset, keep=False)

    return {
        "duplicate_rows": int(frame.duplicated(subset=subset).sum()),
        "duplicate_records_including_first": int(mask.sum()),
        "has_duplicates": bool(mask.any()),
    }
