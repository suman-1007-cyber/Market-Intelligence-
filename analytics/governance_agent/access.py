from __future__ import annotations

from typing import Any


def check(
    actor: str,
    resource: str,
    permissions: dict[str, list[str]],
) -> dict[str, Any]:
    if not actor or not resource:
        raise ValueError("actor and resource are required")

    granted = resource in permissions.get(actor, [])

    return {
        "actor": actor,
        "resource": resource,
        "granted": granted,
        "decision": "ALLOW" if granted else "DENY",
    }
