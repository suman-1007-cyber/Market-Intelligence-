from __future__ import annotations

from typing import Any, Iterable

from .cause_effect import analyze as analyze_cause_effect
from .drivers import analyze as analyze_drivers
from .preparation import prepare
from .ranking import rank


class RootCauseInvestigator:
    agent_id = "root_cause_investigator"

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
        ranked_drivers = rank(driver_analysis)

        return {
            "agent_id": self.agent_id,
            "preparation": prepared,
            "cause_effect": cause_effect,
            "drivers": driver_analysis,
            "ranked_causes": ranked_drivers,
        }
