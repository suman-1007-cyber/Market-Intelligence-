from __future__ import annotations

from typing import Any


def validate_dashboard(dashboard: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(dashboard, dict):
        raise TypeError("dashboard must be a dictionary")

    required = {"metrics", "charts"}
    missing = sorted(required - set(dashboard))

    return {
        "valid": not missing,
        "missing": missing,
    }
