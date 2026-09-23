"""A2: regression tests for the conservative HTTP retry policy.

The retry policy is deliberately narrow: only known-transient HTTP status
codes are retried. Retrying everything amplifies cost and can trigger
rate-limit bans; retrying nothing mishandles transient failures. These
tests pin that boundary so it cannot drift silently.

Least-obvious retryable code: 408 Request Timeout. It looks like a
client-side problem (the client was too slow), but from the server's
perspective it is a transient network condition that often resolves on
retry. Retrying it is the industry-standard behavior.
"""

from units.a2_retry_policy import should_retry


def test_retryable_status_codes_are_retried() -> None:
    """Transient timeout, throttling, and server errors should be retried."""
    assert should_retry(408) is True  # Request Timeout
    assert should_retry(429) is True  # Too Many Requests
    assert should_retry(500) is True  # Internal Server Error
    assert should_retry(503) is True  # Service Unavailable


def test_non_retryable_status_codes_are_not_retried() -> None:
    """Successful and client-error responses do not become transient on repetition."""
    assert should_retry(200) is False  # OK
    assert should_retry(400) is False  # Bad Request
    assert should_retry(401) is False  # Unauthorized
    assert should_retry(404) is False  # Not Found
