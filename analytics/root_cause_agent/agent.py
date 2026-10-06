from __future__ import annotations

from typing import Any, Iterable

from .cause_effect import analyze as analyze_cause_effect
from .confidence import estimate
from .contribution import analyze as analyze_contribution
from .drivers import analyze as analyze_drivers
from .preparation import prepare
from .ranking import rank
from .risk_opportunity import analyze as analyze_risk_opportunity
from .validation import validate


class RootCauseIntelligenceAgent:
    agent_id = "advanced_root_cause_intelligence_agent"

    def investigate(
        self,
        target: Iterable[float],
        drivers: dict[str, Iterable[float]],
    ) -> dict[str, Any]:
        prepared = prepare(target, drivers)

        cause_effect = analyze_cause_effect(
            prepared["target"],
            prepared["drivers"],
        )

        driver_analysis = analyze_drivers(cause_effect)
        ranked_causes = rank(driver_analysis)

        validation = validate(ranked_causes)

        strongest = (
            ranked_causes[0]["absolute_correlation"]
            if ranked_causes
            else 0.0
        )

        confidence = estimate(
            validated_count=validation["validated_count"],
            total_driver_count=prepared["driver_count"],
            strongest_correlation=strongest,
        )

        contribution = analyze_contribution(
            prepared["target"],
            prepared["drivers"],
        )

        target_change = (
            prepared["target"][-1] - prepared["target"][0]
        )

        risk_opportunity = analyze_risk_opportunity(
            confidence=confidence["confidence"],
            strongest_correlation=strongest,
            target_change=target_change,
        )

        return {
            "agent_id": self.agent_id,
            "preparation": prepared,
            "cause_effect": cause_effect,
            "drivers": driver_analysis,
            "ranked_causes": ranked_causes,
            "validation": validation,
            "confidence": confidence,
            "contribution": contribution,
            "risk_opportunity": risk_opportunity,
        }
