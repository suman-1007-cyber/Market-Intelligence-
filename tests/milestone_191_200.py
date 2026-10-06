from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.knowledge_graph_agent.model import create_node, create_edge
from analytics.knowledge_graph_agent.entities import build as build_entities
from analytics.knowledge_graph_agent.evidence import build as build_evidence
from analytics.knowledge_graph_agent.metrics import build as build_metrics
from analytics.knowledge_graph_agent.relationships import build as build_relationships
from analytics.knowledge_graph_agent.lineage import trace
from analytics.knowledge_graph_agent.traversal import neighbors
from analytics.knowledge_graph_agent.consistency import validate
from analytics.knowledge_graph_agent.intelligence import analyze
from analytics.knowledge_graph_agent.agent import KnowledgeEvidenceGraphAgent


node = create_node("company-a", "entity", {"name": "Company A"})
assert node["type"] == "entity"
assert node["data"]["name"] == "Company A"

edge = create_edge("company-a", "evidence-a", "supported_by")
assert edge["relationship"] == "supported_by"

entities = [
    {"id": "company-a", "name": "Company A"},
    {"id": "company-b", "name": "Company B"},
]
entity_nodes = build_entities(entities)
assert len(entity_nodes) == 2
assert entity_nodes[0]["type"] == "entity"

evidence = [
    {"id": "evidence-a", "source": "Source A", "url": "https://example.com/a"},
]
evidence_nodes = build_evidence(evidence)
assert len(evidence_nodes) == 1
assert evidence_nodes[0]["type"] == "evidence"

metrics = [
    {"id": "metric-a", "metric": "revenue", "value": 1000, "unit": "USD"},
]
metric_nodes = build_metrics(metrics)
assert len(metric_nodes) == 1
assert metric_nodes[0]["type"] == "metric"
assert metric_nodes[0]["data"]["value"] == 1000

relationships = [
    {"source": "company-a", "target": "evidence-a", "relationship": "supported_by"},
    {"source": "company-a", "target": "metric-a", "relationship": "has_metric"},
]
edges = build_relationships(relationships)
assert len(edges) == 2

all_nodes = entity_nodes + evidence_nodes + metric_nodes

lineage = trace("company-a", edges)
assert lineage["relationship_count"] == 2

near = neighbors("company-a", edges)
assert set(near) == {"evidence-a", "metric-a"}

consistency = validate(all_nodes, edges)
assert consistency["valid"] is True
assert consistency["invalid_edge_count"] == 0

intelligence = analyze(all_nodes, edges)
assert intelligence["node_count"] == 4
assert intelligence["edge_count"] == 2
assert intelligence["connected"] is True
assert intelligence["node_types"]["entity"] == 2
assert intelligence["node_types"]["evidence"] == 1
assert intelligence["node_types"]["metric"] == 1

result = KnowledgeEvidenceGraphAgent().analyze(
    entities,
    evidence,
    metrics,
    relationships,
)

assert result["agent_id"] == "knowledge-evidence-graph-agent"
assert result["consistency"]["valid"] is True
assert result["intelligence"]["edge_count"] == 2

print("191 Knowledge Graph Data Model      : PASS")
print("192 Entity Nodes                     : PASS")
print("193 Evidence Nodes                   : PASS")
print("194 Metric Nodes                     : PASS")
print("195 Relationship Engine              : PASS")
print("196 Evidence Lineage Graph           : PASS")
print("197 Graph Traversal                  : PASS")
print("198 Graph Consistency                : PASS")
print("199 Graph Intelligence              : PASS")
print("200 Knowledge/Evidence Graph Agent   : PASS")
print("MILESTONE 191-200 : PASS")
