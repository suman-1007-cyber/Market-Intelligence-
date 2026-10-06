from __future__ import annotations

from typing import Any


def validate(
    policy: dict[str, Any],
    access: dict[str, Any],
    secret_scan: dict[str, Any],
) -> dict[str, Any]:
    policy_ok = policy.get("allowed") is True
    access_ok = access.get("granted") is True
    secrets_ok = secret_scan.get("secret_detected") is False

    return {
        "policy_valid": policy_ok,
        "access_valid": access_ok,
        "secrets_valid": secrets_ok,
        "valid": policy_ok and access_ok and secrets_ok,
    }
