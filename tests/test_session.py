import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    PlentyError,
    RateLimitError,
    ServerError,
)

BASE_URL = "https://shop.example.com"


def make_session(httpx_mock) -> _Session:
    """Helper: create a _Session backed by a mocked httpx client."""
    client = httpx.AsyncClient()
    return _Session(BASE_URL, "user@test.com", "password", client)


# --- login ---

async def test_login_sends_credentials(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "tok123", "expiresIn": 86400},
    )
    session = make_session(httpx_mock)
    await session.login()

    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert "username" in request.content.decode()


async def test_login_stores_token(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "tok123", "expiresIn": 86400},
    )
    session = make_session(httpx_mock)
    await session.login()

    assert session._access_token == "tok123"


async def test_login_stores_expiry(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "tok", "expiresIn": 3600},
    )
    session = make_session(httpx_mock)
    before = datetime.now(tz=timezone.utc)
    await session.login()
    after = datetime.now(tz=timezone.utc)

    assert session._token_expiry is not None
    expected_low = before + timedelta(seconds=3600)
    expected_high = after + timedelta(seconds=3600)
    assert expected_low <= session._token_expiry <= expected_high


async def test_login_raises_auth_error_on_401(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        status_code=401,
        json={"error": "Unauthorized"},
    )
    session = make_session(httpx_mock)

    with pytest.raises(AuthError):
        await session.login()


# --- _is_token_expiring ---

def test_is_token_expiring_when_no_token():
    client = httpx.AsyncClient()
    session = _Session(BASE_URL, "u", "p", client)
    assert session._is_token_expiring() is True


def test_is_token_expiring_when_well_within_expiry():
    client = httpx.AsyncClient()
    session = _Session(BASE_URL, "u", "p", client)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    assert session._is_token_expiring() is False


def test_is_token_expiring_when_within_buffer():
    client = httpx.AsyncClient()
    session = _Session(BASE_URL, "u", "p", client)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(seconds=30)
    assert session._is_token_expiring() is True


# --- _request: happy path ---

async def test_request_injects_auth_header(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42},
    )
    session = make_session(httpx_mock)
    session._access_token = "test-token"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    await session.get("/rest/orders/42")

    request = httpx_mock.get_request()
    assert request.headers["Authorization"] == "Bearer test-token"


async def test_request_auto_logs_in_when_no_token(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "fresh-token", "expiresIn": 86400},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/1",
        json={"id": 1},
    )
    session = make_session(httpx_mock)
    result = await session.get("/rest/orders/1")

    assert result == {"id": 1}
    assert session._access_token == "fresh-token"


# --- _request: 401 re-login ---

async def test_request_relogins_on_401_and_retries(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/1",
        status_code=401,
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "new-token", "expiresIn": 86400},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/1",
        json={"id": 1},
    )
    session = make_session(httpx_mock)
    session._access_token = "old-token"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    result = await session.get("/rest/orders/1")

    assert result == {"id": 1}
    assert session._access_token == "new-token"


async def test_request_raises_auth_error_after_double_401(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/1",
        status_code=401,
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "new-token", "expiresIn": 86400},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/1",
        status_code=401,
    )
    session = make_session(httpx_mock)
    session._access_token = "old-token"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    with pytest.raises(AuthError):
        await session.get("/rest/orders/1")


# --- _request: error mapping ---

async def test_request_raises_not_found_on_404(httpx_mock):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/orders/99", status_code=404
    )
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    with pytest.raises(NotFoundError):
        await session.get("/rest/orders/99")


async def test_request_raises_rate_limit_on_429(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders",
        status_code=429,
        headers={"Retry-After": "60"},
    )
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    with pytest.raises(RateLimitError) as exc_info:
        await session.get("/rest/orders")

    assert exc_info.value.retry_after == 60


async def test_request_raises_server_error_on_500(httpx_mock):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/orders", status_code=500
    )
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    with pytest.raises(ServerError):
        await session.get("/rest/orders")


async def test_request_raises_connection_error_on_network_failure(httpx_mock):
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    with pytest.raises(ConnectionError):
        await session.get("/rest/orders")


# --- logout ---

async def test_logout_clears_token(httpx_mock):
    httpx_mock.add_response(method="DELETE", url=f"{BASE_URL}/rest/login", status_code=200)
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    await session.logout()

    assert session._access_token is None
    assert session._token_expiry is None


async def test_logout_is_noop_when_not_logged_in(httpx_mock):
    session = make_session(httpx_mock)
    await session.logout()  # must not raise or make any network calls

    assert httpx_mock.get_requests() == []


async def test_logout_clears_token_even_when_delete_fails(httpx_mock):
    httpx_mock.add_exception(httpx.ConnectError("gone"))
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    with pytest.raises(Exception):
        await session.logout()

    assert session._access_token is None
    assert session._token_expiry is None


async def test_request_returns_empty_dict_for_no_content(httpx_mock):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/1",
        status_code=204,
        content=b"",
    )
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    result = await session.delete("/rest/orders/1")
    assert result == {}


async def test_login_raises_server_error_on_500(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        status_code=500,
    )
    session = make_session(httpx_mock)
    with pytest.raises(ServerError):
        await session.login()


async def test_login_raises_connection_error_on_network_failure(httpx_mock):
    httpx_mock.add_exception(httpx.ConnectError("refused"))
    session = make_session(httpx_mock)
    with pytest.raises(ConnectionError):
        await session.login()


async def test_request_raises_plenty_error_on_unhandled_4xx(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders",
        status_code=403,
    )
    session = make_session(httpx_mock)
    session._access_token = "tok"
    session._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    with pytest.raises(PlentyError):
        await session.get("/rest/orders")
