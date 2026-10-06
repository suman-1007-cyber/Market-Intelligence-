from __future__ import annotations

from typing import Any


def collect(
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    failures = []

    for case, result in zip(cases, results):
        if not result.get("matched", False):
            failures.append({
                "case_id": case.get("case_id"),
                "expected": case.get("expected"),
                "actual": result.get("actual"),
            })

    return failures
