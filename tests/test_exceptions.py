import pytest
from plentymarkets._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    PlentyError,
    RateLimitError,
    ServerError,
)


def test_all_errors_inherit_plenty_error():
    assert issubclass(AuthError, PlentyError)
    assert issubclass(NotFoundError, PlentyError)
    assert issubclass(RateLimitError, PlentyError)
    assert issubclass(ServerError, PlentyError)
    assert issubclass(ConnectionError, PlentyError)


def test_rate_limit_error_stores_retry_after():
    err = RateLimitError("too many requests", retry_after=30)
    assert err.retry_after == 30


def test_rate_limit_error_retry_after_defaults_to_zero():
    err = RateLimitError("too many requests")
    assert err.retry_after == 0


def test_plenty_error_is_catchable_as_exception():
    with pytest.raises(PlentyError):
        raise AuthError("bad credentials")
