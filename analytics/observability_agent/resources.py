from __future__ import annotations

from typing import Any


def record(
    cpu_seconds: float = 0.0,
    memory_mb: float = 0.0,
    requests: int = 0,
) -> dict[str, Any]:
    return {
        "cpu_seconds": max(0.0, float(cpu_seconds)),
        "memory_mb": max(0.0, float(memory_mb)),
        "requests": max(0, int(requests)),
    }
