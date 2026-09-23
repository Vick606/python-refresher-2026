"""A3: typed retry configuration using TypedDict and built-in generics.

A2 modeled the *decision* to retry. A real HTTP client also needs to
*configure* the policy: how many attempts, how long to wait, which codes
count as transient. This module models that configuration with types a
static checker can verify.

The modern syntax used here:

- ``TypedDict`` documents the exact keys a dictionary must have.
- ``list[float]`` and ``frozenset[int]`` are built-in generics -- no need
  for ``typing.List`` or ``typing.FrozenSet`` in Python 3.9+.
- ``Protocol`` describes a shape rather than a base class, so any object
  with a compatible method satisfies the type without inheriting from it.

Delay strategies are swappable at runtime, which matters under load: a
service can lengthen delays when it detects a rate-limit or abuse pattern,
without any caller changing. Swapping a hard-coded backoff for a
circuit-breaker or a "jittered" strategy is a one-line change.
"""

from typing import Protocol, TypedDict, runtime_checkable


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


@runtime_checkable
class DelayStrategy(Protocol):
    """Compute the delay before a given retry attempt.

    Any object with a compatible ``delay_for`` method satisfies this
    Protocol -- inheritance is not required. This is structural typing:
    the shape is what matters, not the class hierarchy.
    """

    def delay_for(self, attempt: int) -> float: ...


class ExponentialDelay:
    """Double the base delay on each attempt: base, 2*base, 4*base, ..."""

    def __init__(self, base_seconds: float = 0.5) -> None:
        self.base_seconds = base_seconds

    def delay_for(self, attempt: int) -> float:
        return self.base_seconds * (2**attempt)


class ConstantDelay:
    """Same delay before every retry."""

    def __init__(self, seconds: float = 0.5) -> None:
        self.seconds = seconds

    def delay_for(self, attempt: int) -> float:
        return self.seconds


class LinearDelay:
    """Delay grows linearly: base, 2*base, 3*base, ..."""

    def __init__(self, base_seconds: float = 0.5) -> None:
        self.base_seconds = base_seconds

    def delay_for(self, attempt: int) -> float:
        return self.base_seconds * (attempt + 1)


def retry_delays_with(config: RetryConfig, strategy: DelayStrategy) -> list[float]:
    """Return the delay before each retry attempt, using ``strategy``.

    The same list length as ``retry_delays``: ``max_attempts - 1`` entries.
    ``retry_delays`` remains as the fixed exponential policy; this function
    lets callers choose the policy at runtime.
    """
    return [strategy.delay_for(attempt) for attempt in range(config["max_attempts"] - 1)]
