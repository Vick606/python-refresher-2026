"""A3: tests for the typed retry configuration.

Prediction answer: at runtime, TypedDict is just dict -- reading a missing
key raises KeyError like any dict. A static checker warns about the missing
key *before* you run, which is the whole point of the annotation. Runtime
safety is not enforced by TypedDict; only the shape is described.
"""

from units.a3_retry_config import (
    DEFAULT_CONFIG,
    RetryConfig,
    is_code_retryable,
    retry_delays,
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
