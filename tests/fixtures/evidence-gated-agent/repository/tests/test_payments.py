from src.payments import charge_order, refund_order, ProviderError


class FakeProvider:
    def __init__(self, fail_times=0):
        self.charges = []
        self.refunds = []
        self.fail_times = fail_times

    def charge(self, amount_cents, idempotency_key):
        if self.fail_times > 0:
            self.fail_times -= 1
            raise ProviderError("transient provider error")
        self.charges.append((amount_cents, idempotency_key))
        return {"status": "succeeded", "amount_cents": amount_cents}

    def refund(self, order_id, amount_cents, idempotency_key):
        self.refunds.append((order_id, amount_cents, idempotency_key))
        return {"status": "succeeded"}


def test_charge_order_uses_idempotency_key():
    provider = FakeProvider()
    result = charge_order(provider, "order_1", 500, "idem_1")
    assert result["status"] == "succeeded"
    assert provider.charges == [(500, "idem_1")]


def test_refund_order():
    provider = FakeProvider()
    result = refund_order(provider, "order_1", 500, "idem_refund_1")
    assert result["status"] == "succeeded"


def test_charge_order_retries_on_provider_error():
    """Regression test for the with_retry narrowing: payments' ProviderError
    must still be retried even though with_retry's default retry_on no
    longer includes it."""
    provider = FakeProvider(fail_times=1)
    result = charge_order(provider, "order_1", 500, "idem_2")
    assert result["status"] == "succeeded"
    assert provider.charges == [(500, "idem_2")]
