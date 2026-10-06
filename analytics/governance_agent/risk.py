from __future__ import annotations

from typing import Any


def assess(
    policy_valid: bool,
    access_valid: bool,
    secrets_valid: bool,
) -> dict[str, Any]:
    failures = sum(
        not value
        for value in (
            policy_valid,
            access_valid,
            secrets_valid,
        )
    )

    if failures == 0:
        level = "LOW"
    elif failures == 1:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "failure_count": failures,
        "risk_level": level,
    }
