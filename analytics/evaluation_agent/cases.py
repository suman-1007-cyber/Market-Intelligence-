from __future__ import annotations

from typing import Any


def create(
    case_id: str,
    input_data: Any,
    expected: Any,
) -> dict[str, Any]:
    if not case_id:
        raise ValueError("case_id must not be empty")

    return {
        "case_id": str(case_id),
        "input": input_data,
        "expected": expected,
    }
