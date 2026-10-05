"""Decision Intelligence Agent."""

from dataclasses import dataclass
from typing import Any

from .engine import evaluate
from .intelligence import synthesize
from .recommendation import recommend
from .risk import analyze
from .scoring import rank, validate_criteria


@dataclass
class DecisionIntelligenceAgent:
    agent_id: str = "decision-intelligence-agent"

    def decide(
        self,
        alternatives: list[dict[str, Any]],
        criteria: dict[str, float],
        risk_factors: dict[str, float] | None = None,
        minimum_score: float = 0.60,
    ) -> dict[str, Any]:
        criteria_validation = validate_criteria(criteria)

        if not criteria_validation["valid"]:
            raise ValueError(
                "; ".join(criteria_validation["errors"])
            )

        evaluation = evaluate(
            alternatives,
            criteria,
        )

        ranked = rank(evaluation)

        recommendation = recommend(
            ranked,
            minimum_score=minimum_score,
        )

        risk = analyze(
            ranked,
            risk_factors=risk_factors,
        )

        intelligence = synthesize(
            ranked,
            recommendation,
            risk,
        )

        return {
            "agent_id": self.agent_id,
            "criteria": criteria_validation,
            "evaluation": ranked,
            "recommendation": recommendation,
            "risk": risk,
            "intelligence": intelligence,
        }
