from __future__ import annotations

from typing import Any


def analyze(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, str]],
) -> dict[str, Any]:
    node_types: dict[str, int] = {}

    for node in nodes:
        if not isinstance(node, dict):
            continue

        node_type = str(node.get("type", "unknown"))
        node_types[node_type] = node_types.get(node_type, 0) + 1

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_types": node_types,
        "connected": bool(edges),
    }
