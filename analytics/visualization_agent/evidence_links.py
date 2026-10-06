from __future__ import annotations

from typing import Any


def link_visualization(
    visualization: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(visualization, dict):
        raise TypeError("visualization must be a dictionary")
    if not isinstance(evidence, list):
        raise TypeError("evidence must be a list")

    return {
        "visualization": visualization,
        "evidence_count": len(evidence),
        "evidence": evidence,
        "traceable": bool(evidence),
    }
