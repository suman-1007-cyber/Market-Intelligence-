from __future__ import annotations

from typing import Any

from .executive_summary import build as build_summary
from .recommendations import build as build_recommendations
from .risks import extract as extract_risks
from .opportunities import extract as extract_opportunities


def summarize(findings: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")

    return {
        "executive_summary": build_summary(findings),
        "recommendations": build_recommendations(findings),
        "risks": extract_risks(findings),
        "opportunities": extract_opportunities(findings),
    }
