from __future__ import annotations

from typing import Any


def validate(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, str]],
) -> dict[str, Any]:
    node_ids = {
        node.get("id")
        for node in nodes
        if isinstance(node, dict) and node.get("id")
    }

    invalid_edges = [
        edge
        for edge in edges
        if not isinstance(edge, dict)
        or edge.get("source") not in node_ids
        or edge.get("target") not in node_ids
    ]

    return {
        "node_count": len(node_ids),
        "edge_count": len(edges),
        "invalid_edge_count": len(invalid_edges),
        "valid": not invalid_edges,
    }
