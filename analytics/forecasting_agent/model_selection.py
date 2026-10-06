from __future__ import annotations

from typing import Any


def select(
    trend_detected: bool,
    seasonality_detected: bool,
    history_length: int,
) -> dict[str, Any]:
    if history_length <= 0:
        raise ValueError("history_length must be positive")

    if seasonality_detected:
        model = "SEASONAL_BASELINE"
    elif trend_detected:
        model = "TREND_BASELINE"
    else:
        model = "NAIVE_BASELINE"

    return {
        "selected_model": model,
        "reason": (
            "SEASONALITY_PRESENT"
            if seasonality_detected
            else "TREND_PRESENT"
            if trend_detected
            else "NO_STRONG_PATTERN"
        ),
        "history_length": int(history_length),
    }
