from __future__ import annotations

from typing import Any

from .model import create_node


def build(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise TypeError("records must be a list")

    nodes = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue

        entity_id = record.get("id", record.get("name", f"entity-{index}"))
        name = record.get("name", entity_id)

        nodes.append(
            create_node(
                str(entity_id),
                "entity",
                {"name": str(name)},
            )
        )

    return nodes
