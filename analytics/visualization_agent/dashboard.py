from __future__ import annotations

from typing import Any


def build(metrics: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metrics, dict):
        raise TypeError("metrics must be a dictionary")

    cards = []
    for name, value in metrics.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            cards.append({
                "name": str(name),
                "value": float(value),
            })

    return {
        "kpi_count": len(cards),
        "cards": cards,
    }
