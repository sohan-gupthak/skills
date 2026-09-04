from src.utils import with_retry, _format_currency


def test_format_currency():
    assert _format_currency(1050) == "$10.50"


def test_with_retry_succeeds_after_transient_failure():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ConnectionError("transient")
        return "ok"

    assert with_retry(flaky, max_attempts=3, base_delay=0) == "ok"
    assert calls["n"] == 2


def test_with_retry_raises_after_max_attempts():
    def always_fails():
        raise ConnectionError("permanent")

    try:
        with_retry(always_fails, max_attempts=2, base_delay=0)
        assert False, "expected ConnectionError"
    except ConnectionError:
        pass


def test_with_retry_does_not_retry_non_matching_exceptions():
    calls = {"n": 0}

    def raises_value_error():
        calls["n"] += 1
        raise ValueError("not transient, should not be retried")

    try:
        with_retry(raises_value_error, max_attempts=3, base_delay=0)
        assert False, "expected ValueError"
    except ValueError:
        pass
    assert calls["n"] == 1, "non-matching exception must propagate on first attempt, not retry"
