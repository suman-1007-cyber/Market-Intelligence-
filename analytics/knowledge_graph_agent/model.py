from __future__ import annotations

from typing import Any


def create_node(node_id: str, node_type: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    if not node_id:
        raise ValueError("node_id must not be empty")
    if not node_type:
        raise ValueError("node_type must not be empty")

    return {
        "id": str(node_id),
        "type": str(node_type),
        "data": data or {},
    }


def create_edge(
    source: str,
    target: str,
    relationship: str,
) -> dict[str, str]:
    if not source or not target or not relationship:
        raise ValueError("source, target and relationship are required")

    return {
        "source": str(source),
        "target": str(target),
        "relationship": str(relationship),
    }
