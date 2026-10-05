"""Competitive Intelligence Agent."""

from dataclasses import dataclass
from typing import Any

from .benchmark import benchmark
from .discovery import discover
from .intelligence import synthesize
from .profiling import profile
from .threats import analyze


@dataclass
class CompetitiveIntelligenceAgent:
    agent_id: str = "competitive-intelligence-agent"

    def analyze(
        self,
        records: list[dict[str, Any]],
        benchmark_metric: str = "market_share",
    ) -> dict[str, Any]:
        discovered = discover(records)

        profiles = profile(records)

        benchmarks = benchmark(
            profiles,
            benchmark_metric,
        )

        benchmark_values = [
            item["value"]
            for item in benchmarks["benchmarks"]
        ]

        market_average = (
            sum(benchmark_values) / len(benchmark_values)
            if benchmark_values
            else None
        )

        leader_share = (
            benchmark_values[0]
            if benchmark_values
            else None
        )

        assessments = [
            analyze(
                item,
                market_average_share=market_average,
                leader_share=leader_share,
            )
            for item in profiles
        ]

        intelligence = synthesize(
            discovered,
            profiles,
            benchmarks,
            assessments,
        )

        return {
            "agent_id": self.agent_id,
            "discovery": discovered,
            "profiles": profiles,
            "benchmarks": benchmarks,
            "assessments": assessments,
            "intelligence": intelligence,
        }
