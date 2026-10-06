from __future__ import annotations

from datetime import datetime
from typing import Any


def check(timestamp: str, maximum_age_seconds: float) -> dict[str, Any]:
    observed = datetime.fromisoformat(timestamp)
    age = max(0.0, (datetime.now(observed.tzinfo) - observed).total_seconds())

    return {
        "timestamp": timestamp,
        "age_seconds": age,
        "fresh": age <= float(maximum_age_seconds),
    }
