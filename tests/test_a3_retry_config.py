"""A3: tests for the typed retry configuration.

Prediction answer: without @runtime_checkable, isinstance(obj, DelayStrategy)
raises TypeError -- the Protocol exists for static checking only. With the
decorator, isinstance returns True if the object has all the protocol's
method *names*, regardless of their signatures. It does not verify argument
types or return types, so a typo'd signature still passes isinstance. The
static checker catches those; the runtime check does not.
"""

from units.a3_retry_config import (
    DEFAULT_CONFIG,
    ConstantDelay,
    DelayStrategy,
    ExponentialDelay,
    LinearDelay,
    RetryConfig,
    is_code_retryable,
    retry_delays,
    retry_delays_with,
)


def test_default_config_has_expected_shape() -> None:
    """Every required key exists and has the expected type."""
    assert DEFAULT_CONFIG["max_attempts"] == 3
    assert DEFAULT_CONFIG["base_delay_seconds"] == 0.5
    assert isinstance(DEFAULT_CONFIG["retryable_codes"], frozenset)
    assert 408 in DEFAULT_CONFIG["retryable_codes"]


def test_retry_delays_grow_exponentially() -> None:
    config: RetryConfig = {
        "max_attempts": 4,
        "base_delay_seconds": 0.5,
        "retryable_codes": frozenset(),
    }
    assert retry_delays(config) == [0.5, 1.0, 2.0]


def test_single_attempt_has_no_delays() -> None:
    """max_attempts=1 means one try and no retries -- an empty delay list."""
    config: RetryConfig = {
        "max_attempts": 1,
        "base_delay_seconds": 0.5,
        "retryable_codes": frozenset(),
    }
    assert retry_delays(config) == []


def test_retryable_codes_respect_config() -> None:
    """The policy must consult the config, not the hard-coded A2 constant."""
    config: RetryConfig = {
        "max_attempts": 1,
        "base_delay_seconds": 0.5,
        "retryable_codes": frozenset({429}),
    }
    assert is_code_retryable(config, 429) is True
    assert is_code_retryable(config, 500) is False


def test_strategies_satisfy_protocol_structurally() -> None:
    """All three classes satisfy DelayStrategy without inheriting from it."""
    for strategy in (ExponentialDelay(), ConstantDelay(), LinearDelay()):
        assert isinstance(strategy, DelayStrategy)


def test_exponential_strategy_matches_original_policy() -> None:
    """The new strategy-based path must reproduce the original exponential policy."""
    config: RetryConfig = {
        "max_attempts": 4,
        "base_delay_seconds": 0.5,
        "retryable_codes": frozenset(),
    }
    assert retry_delays_with(config, ExponentialDelay(base_seconds=0.5)) == retry_delays(config)


def test_constant_strategy_produces_flat_delays() -> None:
    config: RetryConfig = {
        "max_attempts": 3,
        "base_delay_seconds": 0.5,
        "retryable_codes": frozenset(),
    }
    assert retry_delays_with(config, ConstantDelay(seconds=0.25)) == [0.25, 0.25]


def test_linear_strategy_produces_linear_delays() -> None:
    config: RetryConfig = {
        "max_attempts": 4,
        "base_delay_seconds": 0.5,
        "retryable_codes": frozenset(),
    }
    assert retry_delays_with(config, LinearDelay(base_seconds=0.5)) == [0.5, 1.0, 1.5]


def test_duck_typed_object_satisfies_protocol() -> None:
    """An unrelated class with the right method shape also satisfies the Protocol."""

    class FixedDelay:
        def delay_for(self, attempt: int) -> float:
            return 0.0

    config: RetryConfig = {
        "max_attempts": 3,
        "base_delay_seconds": 999.0,
        "retryable_codes": frozenset(),
    }
    # No inheritance, no registration -- only the method shape matters.
    assert retry_delays_with(config, FixedDelay()) == [0.0, 0.0]
