from __future__ import annotations

from typing import Any


def trace(
    node_id: str,
    edges: list[dict[str, str]],
) -> dict[str, Any]:
    if not node_id:
        raise ValueError("node_id must not be empty")

    connected = []

    for edge in edges:
        if not isinstance(edge, dict):
            continue

        if edge.get("source") == node_id or edge.get("target") == node_id:
            connected.append(edge)

    return {
        "node_id": node_id,
        "relationship_count": len(connected),
        "relationships": connected,
    }
