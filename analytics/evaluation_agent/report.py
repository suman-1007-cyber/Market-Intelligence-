from __future__ import annotations

from typing import Any


def build(
    accuracy: dict[str, Any],
    reliability: dict[str, Any],
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "accuracy": accuracy,
        "reliability": reliability,
        "failure_count": len(failures),
        "failures": failures,
    }
