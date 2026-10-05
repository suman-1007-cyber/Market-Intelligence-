"""Market Intelligence Agent."""

from dataclasses import dataclass
from typing import Any

from .intelligence import synthesize
from .opportunity import analyze as analyze_opportunity
from .sizing import analyze as analyze_sizing
from .trends import analyze as analyze_trend


@dataclass
class MarketIntelligenceAgent:
    agent_id: str = "market-intelligence-agent"

    def analyze(
        self,
        market_size: float,
        previous_size: float | None = None,
        trend_values: list[float] | None = None,
        competition_level: float = 0.5,
        trend_strength: float | None = None,
        period: str | None = None,
    ) -> dict[str, Any]:
        sizing = analyze_sizing(
            market_size,
            previous_size,
            period,
        )

        series = trend_values or [float(market_size)]

        trend = analyze_trend(series)

        inferred_trend_strength = (
            float(trend_strength)
            if trend_strength is not None
            else (
                1.0
                if trend["direction"] == "UP"
                else 0.0
                if trend["direction"] == "DOWN"
                else 0.5
            )
        )

        growth = sizing.get("growth_rate")

        if growth is None:
            growth = 0.0

        opportunity = analyze_opportunity(
            growth,
            float(market_size),
            competition_level,
            inferred_trend_strength,
        )

        intelligence = synthesize(
            sizing,
            trend,
            opportunity,
        )

        return {
            "agent_id": self.agent_id,
            "sizing": sizing,
            "trend": trend,
            "opportunity": opportunity,
            "intelligence": intelligence,
        }
