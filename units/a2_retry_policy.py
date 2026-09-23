"""A2: model a conservative retry decision for an external HTTP service.

A retry is appropriate only when a failure is likely transient. Retrying every
4xx response is wrong: most client errors will not succeed on a second attempt.

Run:
    uv run python units/a2_retry_policy.py
"""

RETRYABLE_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})


def should_retry(status_code: int) -> bool:
    """Return whether a known transient HTTP status is safe to retry."""
    return status_code in RETRYABLE_STATUS_CODES


def main() -> None:
    """Print representative retry decisions."""
    for status_code in (200, 400, 401, 404, 408, 429, 500, 503):
        print(f"{status_code}: retry={should_retry(status_code)}")


if __name__ == "__&#8203;main__":
    main()
