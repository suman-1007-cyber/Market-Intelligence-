"""Pricing Intelligence Agent."""

from typing import Any

from .intelligence import analyze


class PricingIntelligenceAgent:
    agent_id = "pricing-intelligence-agent"

    def analyze(
        self,
        current_price: float,
        cost: float,
        units: float,
        competitor_prices: list[float],
        old_price: float,
        new_price: float,
        old_quantity: float,
        new_quantity: float,
        list_price: float | None = None,
        candidate_prices: list[float] | None = None,
        expected_units: list[float] | None = None,
    ) -> dict[str, Any]:
        result = analyze(
            current_price=current_price,
            cost=cost,
            units=units,
            competitor_prices=competitor_prices,
            old_price=old_price,
            new_price=new_price,
            old_quantity=old_quantity,
            new_quantity=new_quantity,
            list_price=list_price,
            candidate_prices=candidate_prices,
            expected_units=expected_units,
        )

        result["agent_id"] = self.agent_id
        return result
