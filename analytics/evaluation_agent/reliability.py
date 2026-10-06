from __future__ import annotations

from typing import Any


def assess(
    accuracy: float,
    failure_count: int,
) -> dict[str, Any]:
    accuracy = max(0.0, min(1.0, float(accuracy)))
    failure_count = max(0, int(failure_count))

    if accuracy >= 0.90 and failure_count == 0:
        level = "HIGH"
    elif accuracy >= 0.70:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "accuracy": accuracy,
        "failure_count": failure_count,
        "reliability": level,
    }
