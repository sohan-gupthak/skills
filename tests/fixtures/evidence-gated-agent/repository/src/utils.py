"""Shared utilities used across the order and refund services."""

import time


def _format_currency(amount_cents):
    """Format an integer cent amount as a display string. Private helper."""
    dollars = amount_cents / 100
    formatted = f"${dollars:.2f}"
    return formatted


def with_retry(fn, *, max_attempts=3, base_delay=0.1, retry_on=(ConnectionError, TimeoutError)):
    """Call fn with exponential backoff retry.

    Used by src/payments.py (order charge + refund flows) and
    src/api/public.py (profile fetch from the internal directory service).

    Only retries exceptions in `retry_on`; anything else propagates on the
    first attempt. Callers whose failure signal isn't a builtin transient
    exception (e.g. payments.ProviderError) must pass it explicitly via
    `retry_on` - the default here does not know about domain-specific
    exception types.
    """
    attempt = 0
    last_exc = None
    while attempt < max_attempts:
        try:
            return fn()
        except retry_on as exc:
            last_exc = exc
            attempt += 1
            time.sleep(base_delay * attempt)
    raise last_exc
