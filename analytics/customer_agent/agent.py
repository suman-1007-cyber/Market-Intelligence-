"""Customer Intelligence Agent."""

from dataclasses import dataclass
from typing import Any

from .behavior import analyze as analyze_behavior
from .ltv import calculate
from .opportunity import analyze as analyze_opportunity
from .risk import analyze as analyze_risk
from .segmentation import segment


@dataclass
class CustomerIntelligenceAgent:
    agent_id: str = "customer-intelligence-agent"

    def analyze(
        self,
        profile: dict[str, Any],
        previous_profile: dict[str, Any] | None = None,
        churn_rate: float = 0.0,
        customer_population: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        customer = str(
            profile.get("customer", "")
        ).strip()

        if not customer:
            raise ValueError(
                "Customer profile requires a customer name."
            )

        behavior = analyze_behavior(
            profile,
            previous_profile,
        )

        population = customer_population or [profile]

        segmentation_records = segment(
            population,
            value_field="revenue",
            customer_field="customer",
        )

        segment_lookup = {
            record["customer"]: record["segment"]
            for record in segmentation_records
        }

        segment_name = segment_lookup.get(
            customer,
            "LOW_VALUE",
        )

        opportunity = analyze_opportunity(
            behavior,
            segment=segment_name,
        )

        risk = analyze_risk(
            behavior,
            churn_rate=churn_rate,
        )

        ltv = calculate(
            revenue=float(
                profile.get("revenue", 0.0)
            ),
            gross_margin=0.70,
            retention_rate=max(
                0.0,
                min(0.999999, 1.0 - churn_rate),
            ),
            periods=4,
        )

        return {
            "agent_id": self.agent_id,
            "customer": customer,
            "segment": segment_name,
            "behavior": behavior,
            "ltv": ltv,
            "opportunity": opportunity,
            "risk": risk,
        }
