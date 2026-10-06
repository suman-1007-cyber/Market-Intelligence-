from __future__ import annotations

from typing import Any

from .model import create_edge


def build(
    relationships: list[dict[str, Any]],
) -> list[dict[str, str]]:
    if not isinstance(relationships, list):
        raise TypeError("relationships must be a list")

    edges = []
    for item in relationships:
        if not isinstance(item, dict):
            continue

        source = item.get("source")
        target = item.get("target")
        relationship = item.get("relationship")

        if source and target and relationship:
            edges.append(
                create_edge(
                    str(source),
                    str(target),
                    str(relationship),
                )
            )

    return edges
