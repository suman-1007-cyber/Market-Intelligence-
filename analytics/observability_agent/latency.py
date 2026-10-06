from __future__ import annotations

from typing import Any


def measure(start: float, end: float) -> dict[str, Any]:
    start = float(start)
    end = float(end)

    elapsed = max(0.0, end - start)

    return {
        "start": start,
        "end": end,
        "elapsed_seconds": elapsed,
    }
