from __future__ import annotations

from typing import Any, Iterable

from .baseline import forecast
from .confidence import estimate
from .evaluation import evaluate
from .risk_opportunity import analyze
from .scenarios import generate


class ForecastingAgent:
    agent_id = "advanced_forecasting_agent"

    def analyze(
        self,
        actual: Iterable[float],
        predicted: Iterable[float],
        baseline: Iterable[float],
        growth_rates: Iterable[float] = (0.0, 0.10, -0.10),
    ) -> dict[str, Any]:
        actual_values = [float(value) for value in actual]
        predicted_values = [float(value) for value in predicted]
        baseline_values = [float(value) for value in baseline]

        evaluation = evaluate(actual_values, predicted_values)
        confidence = estimate(evaluation["errors"])

        if len(baseline_values) >= 2 and baseline_values[0] != 0:
            growth_rate = (
                baseline_values[-1] - baseline_values[0]
            ) / abs(baseline_values[0])
        else:
            growth_rate = 0.0

        scenarios = generate(baseline_values, growth_rates)

        risk_opportunity = analyze(
            confidence=confidence["confidence"],
            growth_rate=growth_rate,
            uncertainty=confidence["uncertainty"],
        )

        return {
            "agent_id": self.agent_id,
            "evaluation": evaluation,
            "confidence": confidence,
            "scenarios": scenarios,
            "risk_opportunity": risk_opportunity,
        }

    def forecast_baseline(
        self,
        values: Iterable[float],
        periods: int = 1,
        model: str = "NAIVE_BASELINE",
    ) -> dict[str, Any]:
        return forecast(values, periods=periods, model=model)
