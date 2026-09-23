"""A3: typed retry configuration using TypedDict and built-in generics.

A2 modeled the *decision* to retry. A real HTTP client also needs to
*configure* the policy: how many attempts, how long to wait, which codes
count as transient. This module models that configuration with types a
static checker can verify.

The modern syntax used here:

- ``TypedDict`` documents the exact keys a dictionary must have.
- ``list[float]`` and ``frozenset[int]`` are built-in generics -- no need
  for ``typing.List`` or ``typing.FrozenSet`` in Python 3.9+.
"""

from typing import TypedDict


class RetryConfig(TypedDict):
    """Configuration for retrying a request.

    All keys are required. The static checker will flag a literal that is
    missing one, and will flag reads of keys that do not exist.
    """

    max_attempts: int
    base_delay_seconds: float
    retryable_codes: frozenset[int]


DEFAULT_CONFIG: RetryConfig = {
    "max_attempts": 3,
    "base_delay_seconds": 0.5,
    "retryable_codes": frozenset({408, 429, 500, 502, 503, 504}),
}


def retry_delays(config: RetryConfig) -> list[float]:
    """Return the delay before each retry attempt.

    Exponential backoff: ``base_delay * 2**attempt`` for each retry. A
    config with ``max_attempts=1`` has no retries and therefore no delays.

    Note: this policy is uncapped. In production, cap the result -- unbounded
    exponential backoff is its own denial-of-service hazard.
    """
    return [
        config["base_delay_seconds"] * (2**attempt) for attempt in range(config["max_attempts"] - 1)
    ]


def is_code_retryable(config: RetryConfig, status_code: int) -> bool:
    """Return whether ``status_code`` is retryable under this config."""
    return status_code in config["retryable_codes"]
