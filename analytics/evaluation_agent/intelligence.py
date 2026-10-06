from __future__ import annotations

from typing import Any


def analyze(
    accuracy: dict[str, Any],
    reliability: dict[str, Any],
    regression: dict[str, Any],
) -> dict[str, Any]:
    return {
        "accuracy": accuracy["accuracy"],
        "reliability": reliability["reliability"],
        "regression_direction": regression["direction"],
        "needs_attention": reliability["reliability"] == "LOW"
        or regression["direction"] == "REGRESSED",
    }
