from __future__ import annotations

from typing import Any


def validate(
    ranked_causes: list[dict[str, Any]],
    minimum_correlation: float = 0.40,
) -> dict[str, Any]:
    if minimum_correlation < 0:
        raise ValueError("minimum_correlation must be non-negative")

    valid = [
        cause
        for cause in ranked_causes
        if float(cause["absolute_correlation"]) >= minimum_correlation
    ]

    return {
        "validated_causes": valid,
        "validated_count": len(valid),
        "valid": bool(valid),
        "minimum_correlation": minimum_correlation,
    }
