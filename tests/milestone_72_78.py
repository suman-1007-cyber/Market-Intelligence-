"""Integration test for Semantic Intelligence milestones 72-78."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.semantic_agent import SemanticIntelligenceAgent
from analytics.semantic_agent.dependencies import build, dependencies
from analytics.semantic_agent.dimensions import resolve as resolve_dimension
from analytics.semantic_agent.entities import resolve as resolve_entity
from analytics.semantic_agent.metrics import resolve as resolve_metric
from analytics.semantic_agent.validation import validate


def main() -> None:
    print("=" * 46)
    print(" SEMANTIC INTELLIGENCE — MILESTONES 72–78")
    print("=" * 46)

    entity = resolve_entity("customers")
    assert entity["resolved"]
    assert entity["canonical"] == "customer"
    print("72 Semantic Entity Resolver : PASS")

    dimension = resolve_dimension("country")
    assert dimension["resolved"]
    assert dimension["canonical"] == "geography"
    print("73 Business Dimension      : PASS")

    metric = resolve_metric("average_price")
    assert metric["resolved"]
    assert metric["unit"] == "currency_per_unit"
    print("74 Metric Definition        : PASS")

    graph = build({
        "average_price": {
            "dependencies": ["revenue", "units"]
        }
    })
    assert dependencies(graph, "average_price") == ["revenue", "units"]
    print("75 Metric Dependency Graph : PASS")

    query = {
        "metric": "revenue",
        "entity": "customers",
        "dimensions": ["country", "year"],
    }

    agent = SemanticIntelligenceAgent()
    result = agent.analyze(query)

    assert result["resolution"]["resolved"]
    print("76 Semantic Query Resolver : PASS")

    validation = validate(result["resolution"])
    assert validation["valid"]
    print("77 Semantic Validation      : PASS")

    assert result["agent_id"] == "semantic-intelligence-agent"
    assert "revenue" in result["metric_dependencies"]
    print("78 Semantic Intelligence   : PASS")

    print("-" * 46)
    print("SEMANTIC INTELLIGENCE : PASS")
    print("=" * 46)


if __name__ == "__main__":
    main()
