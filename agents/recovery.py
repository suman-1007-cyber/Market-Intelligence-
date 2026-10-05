"""Controlled retry and recovery policies."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    """Retry configuration."""

    max_attempts: int = 3

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")


class RecoveryEngine:
    """Determines whether a failed task may be retried."""

    def __init__(self, policy: RetryPolicy | None = None) -> None:
        self.policy = policy or RetryPolicy()

    def should_retry(self, attempts: int) -> bool:
        return attempts < self.policy.max_attempts
