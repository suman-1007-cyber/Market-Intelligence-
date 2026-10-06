from __future__ import annotations

from typing import Any

from .normalization import normalize
from .opportunity import analyze as analyze_opportunity
from .preparation import prepare
from .profiling import profile
from .regional import analyze as analyze_regional
from .risk import analyze as analyze_risk
from .segment_opportunity import analyze as analyze_segment_opportunity
from .segmentation import segment
from .trends import detect


class GeospatialSegmentationAgent:
    agent_id = "geospatial_segmentation_intelligence_agent"

    def analyze(
        self,
        geographic_records: list[dict[str, Any]],
        customers: list[dict[str, Any]],
        value_field: str = "sales",
        customer_value_field: str = "revenue",
    ) -> dict[str, Any]:
        prepared = prepare(geographic_records)
        normalized = normalize(prepared["records"])

        regional = analyze_regional(
            normalized,
            value_field,
        )

        regional_trends = {}

        for region, data in regional.items():
            regional_trends[region] = detect(
                [data["minimum"], data["maximum"]]
            )

        geographic_opportunities = {}

        for region, data in regional.items():
            growth = regional_trends[region]["change_rate"]

            geographic_opportunities[region] = (
                analyze_opportunity(
                    growth_rate=growth,
                    market_value=data["total"],
                )
            )

        segmented = segment(
            customers,
            value_field=customer_value_field,
        )

        segment_profiles = profile(
            segmented,
            value_field=customer_value_field,
        )

        segment_intelligence = {}

        for name, segment_profile in segment_profiles.items():
            segment_intelligence[name] = (
                analyze_segment_opportunity(
                    segment_profile
                )
            )

        geographic_risk = {}

        for region, data in regional.items():
            geographic_risk[region] = analyze_risk(
                growth_rate=regional_trends[region]["change_rate"],
                volatility=0.0,
                concentration=0.0,
            )

        return {
            "agent_id": self.agent_id,
            "geographic": {
                "preparation": prepared,
                "regional": regional,
                "trends": regional_trends,
                "opportunities": geographic_opportunities,
                "risk": geographic_risk,
            },
            "segmentation": {
                "customers": segmented,
                "profiles": segment_profiles,
                "intelligence": segment_intelligence,
            },
        }
