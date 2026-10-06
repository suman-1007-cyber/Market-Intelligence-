from __future__ import annotations

from typing import Any


def neighbors(
    node_id: str,
    edges: list[dict[str, str]],
) -> list[str]:
    if not node_id:
        raise ValueError("node_id must not be empty")

    result = []

    for edge in edges:
        if not isinstance(edge, dict):
            continue

        if edge.get("source") == node_id:
            result.append(edge["target"])
        elif edge.get("target") == node_id:
            result.append(edge["source"])

    return result
