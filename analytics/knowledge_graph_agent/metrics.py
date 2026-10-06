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

        metric_id = record.get("id", record.get("metric", f"metric-{index}"))
        nodes.append(
            create_node(
                str(metric_id),
                "metric",
                {
                    "metric": record.get("metric", ""),
                    "value": record.get("value"),
                    "unit": record.get("unit", ""),
                },
            )
        )

    return nodes
