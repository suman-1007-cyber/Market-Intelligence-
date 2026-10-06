from __future__ import annotations

from typing import Any


def matches(
    model: dict[str, Any],
    required_capability: str,
) -> bool:
    if not isinstance(model, dict):
        return False

    capabilities = model.get("capabilities", [])
    return str(required_capability) in capabilities
