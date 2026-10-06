from __future__ import annotations

from typing import Any

from .entities import build as build_entities
from .evidence import build as build_evidence
from .metrics import build as build_metrics
from .relationships import build as build_relationships
from .consistency import validate
from .intelligence import analyze


class KnowledgeEvidenceGraphAgent:
    agent_id = "knowledge-evidence-graph-agent"

    def analyze(
        self,
        entities: list[dict[str, Any]],
        evidence: list[dict[str, Any]],
        metrics: list[dict[str, Any]],
        relationships: list[dict[str, Any]],
    ) -> dict[str, Any]:
        entity_nodes = build_entities(entities)
        evidence_nodes = build_evidence(evidence)
        metric_nodes = build_metrics(metrics)

        nodes = entity_nodes + evidence_nodes + metric_nodes
        edges = build_relationships(relationships)

        consistency = validate(nodes, edges)
        intelligence = analyze(nodes, edges)

        return {
            "agent_id": self.agent_id,
            "nodes": nodes,
            "edges": edges,
            "consistency": consistency,
            "intelligence": intelligence,
        }
