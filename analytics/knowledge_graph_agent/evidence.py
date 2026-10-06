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

        evidence_id = record.get("id", f"evidence-{index}")
        nodes.append(
            create_node(
                str(evidence_id),
                "evidence",
                {
                    "source": record.get("source", ""),
                    "url": record.get("url", ""),
                },
            )
        )

    return nodes
