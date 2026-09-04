"""Order charge and refund flows against the payment provider."""

from src.utils import with_retry


class ProviderError(Exception):
    pass


def charge_order(provider_client, order_id, amount_cents, idempotency_key):
    """Charge an order. The provider treats idempotency_key as a dedup key
    for 24h, so retries with the same key are safe from double-charging.
    """

    def _do_charge():
        return provider_client.charge(
            amount_cents=amount_cents,
            idempotency_key=idempotency_key,
        )

    return with_retry(_do_charge, max_attempts=3, retry_on=(ConnectionError, TimeoutError, ProviderError))


def refund_order(provider_client, order_id, amount_cents, idempotency_key):
    """Refund a previously charged order."""

    def _do_refund():
        return provider_client.refund(
            order_id=order_id,
            amount_cents=amount_cents,
            idempotency_key=idempotency_key,
        )

    return with_retry(_do_refund, max_attempts=3, retry_on=(ConnectionError, TimeoutError, ProviderError))
