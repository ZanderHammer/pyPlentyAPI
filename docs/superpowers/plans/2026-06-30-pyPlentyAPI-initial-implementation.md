# pyPlentyAPI Initial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a working async Python package (`plentymarkets`) with a `PlentyClient` covering Orders, Items, Stock, and Contacts, backed by full unit tests and conventional-commit tooling.

**Architecture:** Single `PlentyClient` entry point owns a shared `_Session` (httpx + auth). Four module classes (`OrdersModule`, `ItemsModule`, `StockModule`, `ContactsModule`) are lazily instantiated as properties and each hold a reference to the shared session. All network I/O is async.

**Tech Stack:** Python 3.12, UV, httpx, pytest, pytest-httpx, pytest-asyncio, commitizen, pre-commit

## Global Constraints

- Python `>=3.11` (pin `3.12` in `.python-version`)
- `asyncio_mode = "auto"` — all async test functions run automatically, no `@pytest.mark.asyncio` needed
- Google-style docstrings on every public method; response dict keys documented exhaustively
- Conventional commits enforced via pre-commit + commitizen (`cz_conventional_commits`)
- `CHANGELOG.md` only ever has an `[Unreleased]` section — never add a release entry
- PlentyMarkets REST API only — not PlentyBase
- No automatic retries — surface errors to the caller

---

### Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.gitignore`
- Create: `CLAUDE.md`
- Create: `CHANGELOG.md`
- Create: `.pre-commit-config.yaml`
- Create: `src/plentymarkets/__init__.py`
- Create: `src/plentymarkets/modules/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

**Interfaces:**
- Produces: `uv run pytest` exits 0 (no tests yet, but setup is correct); `uv run pre-commit run --all-files` exits 0

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p src/plentymarkets/modules tests
```

- [ ] **Step 2: Write `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "plentymarkets"
version = "0.1.0"
description = "Async Python client for the PlentyMarkets REST API"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-httpx>=0.30",
    "pytest-asyncio>=0.23",
    "commitizen>=3.29",
    "pre-commit>=3.7",
    "hatchling>=1.25",
]

[tool.hatch.build.targets.wheel]
packages = ["src/plentymarkets"]

[tool.pytest.ini_options]
asyncio_mode = "auto"

[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
version_files = ["pyproject.toml:version"]
```

- [ ] **Step 3: Write `.python-version`**

```
3.12
```

- [ ] **Step 4: Write `.gitignore`**

```
__pycache__/
*.py[cod]
*.egg-info/
.venv/
dist/
.uv/
uv.lock
.pytest_cache/
.ruff_cache/
```

- [ ] **Step 5: Write `CLAUDE.md`**

```markdown
# pyPlentyAPI — Claude Guide

## Project
Async Python client for the PlentyMarkets REST API. NOT PlentyBase.
Package name: `plentymarkets`. Entry point: `PlentyClient`.

## API Docs
- REST API reference: https://developers.plentymarkets.com/en-gb/plentymarkets-rest-api/index.html
- OpenAPI spec (JSON): https://raw.githubusercontent.com/plentymarkets/api-doc/master/plentymarkets/openApiV3/openApiV3.json

## Setup
```bash
uv sync --extra dev
uv run pre-commit install --hook-type commit-msg
```

## Running tests
```bash
uv run pytest                        # unit tests only
uv run pytest -m integration         # requires live credentials
```

## Conventions
- Conventional commits enforced via commitizen (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`)
- Google-style docstrings on ALL public methods; document every response dict key
- CHANGELOG.md: only ever write to `[Unreleased]` — never add a release section
- CHANGELOG.md: Group changes by module. Use the same prefix as in commit messages.
- Small focused commits, one logical change each

## Package structure
```
src/plentymarkets/
  __init__.py        # exports PlentyClient
  client.py          # PlentyClient
  _session.py        # HTTP session, auth lifecycle
  _exceptions.py     # exception hierarchy
  modules/
    orders.py        # OrdersModule  → /rest/orders
    items.py         # ItemsModule   → /rest/items
    stock.py         # StockModule   → /rest/stock
    contacts.py      # ContactsModule → /rest/accounts/contacts
```

## Auth
POST /rest/login with username+password → accessToken + expiresIn (seconds).
Token sent as `Authorization: Bearer <token>` on every request.
Auto-refreshed when within 60 s of expiry. 401 mid-session → re-login once → retry.
```
```

- [ ] **Step 6: Write `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
```

- [ ] **Step 7: Write `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.29.1
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

- [ ] **Step 8: Write `src/plentymarkets/__init__.py`** (empty placeholder for now)

```python
```

- [ ] **Step 9: Write `src/plentymarkets/modules/__init__.py`** (empty placeholder for now)

```python
```

- [ ] **Step 10: Write `tests/__init__.py`** (empty)

```python
```

- [ ] **Step 11: Write `tests/conftest.py`**

```python
import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "integration: marks tests as requiring live API credentials "
        "(deselect with '-m \"not integration\"')",
    )
```

- [ ] **Step 12: Install dependencies and pre-commit**

```bash
uv sync --extra dev
uv run pre-commit install --hook-type commit-msg
```

- [ ] **Step 13: Verify pytest runs with no errors**

```bash
uv run pytest
```

Expected: `no tests ran` (exit 0)

- [ ] **Step 14: Commit**

```bash
git add pyproject.toml .python-version .gitignore CLAUDE.md CHANGELOG.md \
        .pre-commit-config.yaml src/ tests/
git commit -m "chore: initial project scaffolding"
```

---

### Task 2: Exception Hierarchy

**Files:**
- Create: `src/plentymarkets/_exceptions.py`
- Create: `tests/test_exceptions.py`

**Interfaces:**
- Produces:
  - `PlentyError(Exception)` — base
  - `AuthError(PlentyError)` — 401
  - `NotFoundError(PlentyError)` — 404
  - `RateLimitError(PlentyError)` — 429; `.retry_after: int`
  - `ServerError(PlentyError)` — 5xx
  - `ConnectionError(PlentyError)` — network failures

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_exceptions.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_exceptions.py -v
```

Expected: `ImportError` — module not found

- [ ] **Step 3: Implement `src/plentymarkets/_exceptions.py`**

```python
class PlentyError(Exception):
    """Base exception for all plentymarkets client errors."""


class AuthError(PlentyError):
    """Raised on 401 responses or when login credentials are rejected."""


class NotFoundError(PlentyError):
    """Raised on 404 responses."""


class RateLimitError(PlentyError):
    """Raised on 429 responses.

    Attributes:
        retry_after: Seconds to wait before retrying, taken from the
            ``Retry-After`` response header. ``0`` if the header is absent.
    """

    def __init__(self, message: str, retry_after: int = 0) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class ServerError(PlentyError):
    """Raised on 5xx responses."""


class ConnectionError(PlentyError):
    """Raised when the network is unreachable, DNS fails, or a timeout occurs."""
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_exceptions.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/_exceptions.py tests/test_exceptions.py
git commit -m "feat: add exception hierarchy"
```

---

### Task 3: Session — HTTP Layer and Auth Lifecycle

**Files:**
- Create: `src/plentymarkets/_session.py`
- Create: `tests/test_session.py`

**Interfaces:**
- Consumes: `AuthError`, `NotFoundError`, `RateLimitError`, `ServerError`, `ConnectionError` from `._exceptions`
- Produces:
  - `_Session(base_url: str, username: str, password: str, client: httpx.AsyncClient)`
  - `await session.login() -> None`
  - `await session.logout() -> None`
  - `await session.get(path, **kwargs) -> dict`
  - `await session.post(path, **kwargs) -> dict`
  - `await session.put(path, **kwargs) -> dict`
  - `await session.delete(path, **kwargs) -> dict`
  - `session._access_token: str | None` (inspectable in tests)
  - `session._token_expiry: datetime | None` (settable in tests)

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_session.py
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_session.py -v
```

Expected: `ImportError` — `_session` module not found

- [ ] **Step 3: Implement `src/plentymarkets/_session.py`**

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from ._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

_REFRESH_BUFFER_SECONDS = 60


class _Session:
    """Manages the httpx client, login state, and token lifecycle.

    Args:
        base_url: PlentyMarkets shop base URL, e.g. ``https://your-shop.plentymarkets.com``.
        username: PlentyMarkets back-end user e-mail.
        password: PlentyMarkets back-end user password.
        client: Shared ``httpx.AsyncClient`` instance.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        client: httpx.AsyncClient,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._client = client
        self._access_token: str | None = None
        self._token_expiry: datetime | None = None

    def _is_token_expiring(self) -> bool:
        if self._access_token is None or self._token_expiry is None:
            return True
        return datetime.now(tz=timezone.utc) >= self._token_expiry - timedelta(
            seconds=_REFRESH_BUFFER_SECONDS
        )

    async def login(self) -> None:
        """Authenticate and store the access token.

        Raises:
            AuthError: If the server rejects the credentials (HTTP 401).
        """
        response = await self._client.post(
            f"{self._base_url}/rest/login",
            json={"username": self._username, "password": self._password},
        )
        if response.status_code == 401:
            raise AuthError("Login failed: invalid credentials")
        response.raise_for_status()
        data = response.json()
        self._access_token = data["accessToken"]
        self._token_expiry = datetime.now(tz=timezone.utc) + timedelta(
            seconds=data["expiresIn"]
        )

    async def logout(self) -> None:
        """Invalidate the current session token on the server and clear local state."""
        if self._access_token is None:
            return
        try:
            await self._client.delete(
                f"{self._base_url}/rest/login",
                headers={"Authorization": f"Bearer {self._access_token}"},
            )
        finally:
            self._access_token = None
            self._token_expiry = None

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        if self._is_token_expiring():
            await self.login()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        try:
            response = await self._client.request(
                method,
                f"{self._base_url}{path}",
                headers=headers,
                **kwargs,
            )
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            raise ConnectionError(str(exc)) from exc

        if response.status_code == 401:
            await self.login()
            headers["Authorization"] = f"Bearer {self._access_token}"
            try:
                response = await self._client.request(
                    method,
                    f"{self._base_url}{path}",
                    headers=headers,
                    **kwargs,
                )
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                raise ConnectionError(str(exc)) from exc
            if response.status_code == 401:
                raise AuthError("Authentication failed after token refresh")

        if response.status_code == 404:
            raise NotFoundError(f"{method} {path} returned 404")
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 0))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if response.status_code >= 500:
            raise ServerError(f"Server error {response.status_code}: {method} {path}")

        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    async def get(self, path: str, **kwargs: Any) -> dict:
        """Send a GET request."""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> dict:
        """Send a POST request."""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> dict:
        """Send a PUT request."""
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> dict:
        """Send a DELETE request."""
        return await self._request("DELETE", path, **kwargs)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_session.py -v
```

Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/_session.py tests/test_session.py
git commit -m "feat: add session with login, token lifecycle, and error mapping"
```

---

### Task 4: PlentyClient

**Files:**
- Create: `src/plentymarkets/client.py`
- Modify: `src/plentymarkets/__init__.py`
- Create: `tests/test_client.py`

**Interfaces:**
- Consumes: `_Session` from `._session`; module classes (stubs — just need the names to exist)
- Produces:
  - `PlentyClient(base_url, username, password)`
  - `async with PlentyClient(...) as client:` — logs in on enter, logs out + closes on exit
  - `await client.login()`, `await client.logout()`, `await client.aclose()`
  - `client.orders` → `OrdersModule`
  - `client.items` → `ItemsModule`
  - `client.stock` → `StockModule`
  - `client.contacts` → `ContactsModule`

- [ ] **Step 1: Write stub module classes so imports don't fail**

Create four empty stub files (they will be fully implemented in later tasks):

```python
# src/plentymarkets/modules/orders.py
from __future__ import annotations
from .._session import _Session

class OrdersModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

```python
# src/plentymarkets/modules/items.py
from __future__ import annotations
from .._session import _Session

class ItemsModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

```python
# src/plentymarkets/modules/stock.py
from __future__ import annotations
from .._session import _Session

class StockModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

```python
# src/plentymarkets/modules/contacts.py
from __future__ import annotations
from .._session import _Session

class ContactsModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

- [ ] **Step 2: Write the failing tests**

```python
# tests/test_client.py
import pytest
import httpx
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

from plentymarkets import PlentyClient
from plentymarkets.modules.orders import OrdersModule
from plentymarkets.modules.items import ItemsModule
from plentymarkets.modules.stock import StockModule
from plentymarkets.modules.contacts import ContactsModule

BASE_URL = "https://shop.example.com"


async def test_context_manager_logs_in_and_out(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "tok", "expiresIn": 86400},
    )
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/login",
        status_code=200,
    )

    async with PlentyClient(BASE_URL, "user", "pass"):
        pass

    requests = httpx_mock.get_requests()
    assert requests[0].method == "POST"
    assert requests[1].method == "DELETE"


async def test_orders_property_returns_orders_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.orders, OrdersModule)


async def test_items_property_returns_items_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.items, ItemsModule)


async def test_stock_property_returns_stock_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.stock, StockModule)


async def test_contacts_property_returns_contacts_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.contacts, ContactsModule)


async def test_module_properties_are_lazily_cached(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert client.orders is client.orders
    assert client.items is client.items
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
uv run pytest tests/test_client.py -v
```

Expected: `ImportError` — `PlentyClient` not found

- [ ] **Step 4: Implement `src/plentymarkets/client.py`**

```python
from __future__ import annotations

import httpx

from ._session import _Session
from .modules.contacts import ContactsModule
from .modules.items import ItemsModule
from .modules.orders import OrdersModule
from .modules.stock import StockModule


class PlentyClient:
    """Async client for the PlentyMarkets REST API.

    Use as an async context manager (recommended) or call ``login()``/``aclose()``
    manually.

    Args:
        base_url: Shop base URL, e.g. ``https://your-shop.plentymarkets.com``.
        username: PlentyMarkets back-end user e-mail.
        password: PlentyMarkets back-end user password.

    Example::

        async with PlentyClient(
            base_url="https://your-shop.plentymarkets.com",
            username="user@example.com",
            password="secret",
        ) as client:
            order = await client.orders.get(42)
    """

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self._httpx_client = httpx.AsyncClient()
        self._session = _Session(base_url, username, password, self._httpx_client)
        self._orders: OrdersModule | None = None
        self._items: ItemsModule | None = None
        self._stock: StockModule | None = None
        self._contacts: ContactsModule | None = None

    async def __aenter__(self) -> PlentyClient:
        await self.login()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.logout()
        await self.aclose()

    async def login(self) -> None:
        """Authenticate and acquire an access token."""
        await self._session.login()

    async def logout(self) -> None:
        """Invalidate the current token on the server and clear local state."""
        await self._session.logout()

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._httpx_client.aclose()

    @property
    def orders(self) -> OrdersModule:
        """Access the Orders module (``/rest/orders``)."""
        if self._orders is None:
            self._orders = OrdersModule(self._session)
        return self._orders

    @property
    def items(self) -> ItemsModule:
        """Access the Items module (``/rest/items``)."""
        if self._items is None:
            self._items = ItemsModule(self._session)
        return self._items

    @property
    def stock(self) -> StockModule:
        """Access the Stock module (``/rest/stock``)."""
        if self._stock is None:
            self._stock = StockModule(self._session)
        return self._stock

    @property
    def contacts(self) -> ContactsModule:
        """Access the Contacts module (``/rest/accounts/contacts``)."""
        if self._contacts is None:
            self._contacts = ContactsModule(self._session)
        return self._contacts
```

- [ ] **Step 5: Update `src/plentymarkets/__init__.py`**

```python
from .client import PlentyClient

__all__ = ["PlentyClient"]
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
uv run pytest tests/test_client.py -v
```

Expected: all tests pass

- [ ] **Step 7: Run the full test suite**

```bash
uv run pytest -v
```

Expected: all tests pass

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/client.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/ tests/test_client.py
git commit -m "feat: add PlentyClient with lazy module properties"
```

---

### Task 5: Orders Module

**Files:**
- Modify: `src/plentymarkets/modules/orders.py` (replace stub)
- Create: `tests/test_orders.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.post`, `_Session.put`
- Produces:
  - `await orders.get(order_id: int) -> dict`
  - `await orders.list(page: int = 1, items_per_page: int = 50) -> dict`
  - `await orders.create(data: dict) -> dict`
  - `await orders.update_status(order_id: int, status_id: float) -> dict`
  - `orders.paginate_orders(items_per_page: int = 50) -> AsyncIterator[dict]`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_orders.py
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_get_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42, "statusId": 5.0},
    )
    result = await orders.get(42)
    assert result["id"] == 42


async def test_list_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=25",
        json={"page": 2, "totalsCount": 50, "isLastPage": True, "entries": []},
    )
    result = await orders.list(page=2, items_per_page=25)
    assert result["page"] == 2


async def test_list_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    await orders.list()
    request = httpx_mock.get_request()
    assert "page=1" in str(request.url)
    assert "itemsPerPage=50" in str(request.url)


async def test_create_posts_data(httpx_mock, orders):
    payload = {"typeId": 1, "plentyId": 12345}
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders",
        json={"id": 99, "typeId": 1},
    )
    result = await orders.create(payload)
    assert result["id"] == 99


async def test_update_status_puts_to_order_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42, "statusId": 8.0},
    )
    result = await orders.update_status(42, status_id=8.0)
    assert result["statusId"] == 8.0


async def test_paginate_orders_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [order async for order in orders.paginate_orders(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_orders_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_orders()]
    assert results == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_orders.py -v
```

Expected: `AttributeError` — `OrdersModule` has no methods yet

- [ ] **Step 3: Implement `src/plentymarkets/modules/orders.py`**

```python
from __future__ import annotations

from typing import Any, AsyncIterator

from .._session import _Session


class OrdersModule:
    """Wraps the PlentyMarkets ``/rest/orders`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, order_id: int) -> dict:
        """Get a single order by ID.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The order ID.
            - ``typeId`` (int): Order type. 1=order, 2=delivery, 3=returns,
              4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
              9=multiorder.
            - ``statusId`` (float): Current order status ID (e.g. ``5.0``).
            - ``ownerId`` (int): ID of the user who owns the order.
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``locationId`` (int): Accounting location ID.
            - ``warehouseId`` (int): Warehouse ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``orderItems`` (list[dict]): List of order item dicts.
            - ``addressRelations`` (list[dict]): Billing/delivery address
              relations.
            - ``orderProperties`` (list[dict]): Custom order properties.
            - ``amounts`` (list[dict]): Order amount breakdowns per currency.
            - ``dates`` (list[dict]): Significant dates (e.g. payment due).
            - ``relations`` (list[dict]): Related contacts, warehouses, etc.
        """
        return await self._session.get(f"/rest/orders/{order_id}")

    async def list(self, page: int = 1, items_per_page: int = 50) -> dict:
        """List orders with pagination.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching orders.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Order dicts; same keys as ``get()``.
        """
        return await self._session.get(
            "/rest/orders",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def create(self, data: dict) -> dict:
        """Create a new order.

        Args:
            data: Order payload dict. Required keys vary by order type; at
                minimum include ``typeId`` and ``plentyId``.

        Returns:
            The created order dict; same keys as ``get()``.
        """
        return await self._session.post("/rest/orders", json=data)

    async def update_status(self, order_id: int, status_id: float) -> dict:
        """Update the status of an order.

        Args:
            order_id: The PlentyMarkets order ID.
            status_id: Target status ID (e.g. ``5.0`` = cleared for shipping,
                ``7.0`` = outgoing items booked, ``8.0`` = cancelled).

        Returns:
            The updated order dict; same keys as ``get()``.
        """
        return await self._session.put(
            f"/rest/orders/{order_id}", json={"statusId": status_id}
        )

    async def paginate_orders(
        self, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every order across all pages.

        Args:
            items_per_page: Results per page request (max 250).

        Yields:
            Individual order dicts; same keys as ``get()``.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=items_per_page)
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_orders.py -v
```

Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/modules/orders.py tests/test_orders.py
git commit -m "feat: add OrdersModule (get, list, create, update_status, paginate)"
```

---

### Task 6: Items Module

**Files:**
- Modify: `src/plentymarkets/modules/items.py` (replace stub)
- Create: `tests/test_items.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.post`, `_Session.put`
- Produces:
  - `await items.get(item_id: int) -> dict`
  - `await items.list(page: int = 1, items_per_page: int = 50) -> dict`
  - `await items.create(data: dict) -> dict`
  - `await items.update(item_id: int, data: dict) -> dict`
  - `items.paginate_items(items_per_page: int = 50) -> AsyncIterator[dict]`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_items.py
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.items import ItemsModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def items(session):
    return ItemsModule(session)


async def test_get_calls_correct_url(httpx_mock, items):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items/10",
        json={"id": 10, "position": 0},
    )
    result = await items.get(10)
    assert result["id"] == 10


async def test_list_sends_pagination_params(httpx_mock, items):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items?page=3&itemsPerPage=10",
        json={"page": 3, "totalsCount": 30, "isLastPage": True, "entries": []},
    )
    result = await items.list(page=3, items_per_page=10)
    assert result["page"] == 3


async def test_create_posts_data(httpx_mock, items):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/items",
        json={"id": 55},
    )
    result = await items.create({"vatId": 0, "producingCountryId": 1})
    assert result["id"] == 55


async def test_update_puts_to_item_url(httpx_mock, items):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/items/10",
        json={"id": 10, "position": 1},
    )
    result = await items.update(10, {"position": 1})
    assert result["position"] == 1


async def test_paginate_items_yields_all_items(httpx_mock, items):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 10}, {"id": 11}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 12}],
        },
    )
    results = [i async for i in items.paginate_items(items_per_page=2)]
    assert [r["id"] for r in results] == [10, 11, 12]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_items.py -v
```

Expected: `AttributeError` — `ItemsModule` has no methods yet

- [ ] **Step 3: Implement `src/plentymarkets/modules/items.py`**

```python
from __future__ import annotations

from typing import Any, AsyncIterator

from .._session import _Session


class ItemsModule:
    """Wraps the PlentyMarkets ``/rest/items`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, item_id: int) -> dict:
        """Get a single item by ID.

        Args:
            item_id: The PlentyMarkets item ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The item ID.
            - ``position`` (int): Item sort position.
            - ``manufacturerId`` (int): Manufacturer ID.
            - ``stockType`` (int): Stock type. 0=stocked, 1=production,
              2=colli, 3=special order.
            - ``vatId`` (int): VAT configuration ID.
            - ``producingCountryId`` (int): Country of origin ID.
            - ``condition`` (int): Item condition (0–5).
            - ``conditionApi`` (int): Condition exposed via API (0–5).
            - ``mainVariationId`` (int): ID of the main variation.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``itemProperties`` (list[dict]): Custom item properties.
            - ``texts`` (list[dict]): Multilingual name/description texts.
        """
        return await self._session.get(f"/rest/items/{item_id}")

    async def list(self, page: int = 1, items_per_page: int = 50) -> dict:
        """List items with pagination.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching items.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Item dicts; same keys as ``get()``.
        """
        return await self._session.get(
            "/rest/items",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def create(self, data: dict) -> dict:
        """Create a new item.

        Args:
            data: Item payload dict. Recommended keys: ``vatId``,
                ``producingCountryId``, ``stockType``.

        Returns:
            The created item dict; same keys as ``get()``.
        """
        return await self._session.post("/rest/items", json=data)

    async def update(self, item_id: int, data: dict) -> dict:
        """Update an existing item.

        Args:
            item_id: The PlentyMarkets item ID.
            data: Fields to update (partial update supported).

        Returns:
            The updated item dict; same keys as ``get()``.
        """
        return await self._session.put(f"/rest/items/{item_id}", json=data)

    async def paginate_items(
        self, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every item across all pages.

        Args:
            items_per_page: Results per page request (max 250).

        Yields:
            Individual item dicts; same keys as ``get()``.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=items_per_page)
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_items.py -v
```

Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/modules/items.py tests/test_items.py
git commit -m "feat: add ItemsModule (get, list, create, update, paginate)"
```

---

### Task 7: Stock Module

**Files:**
- Modify: `src/plentymarkets/modules/stock.py` (replace stub)
- Create: `tests/test_stock.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.put`
- Produces:
  - `await stock.get_by_warehouse(warehouse_id: int, page: int = 1, items_per_page: int = 50) -> dict`
  - `await stock.correct(warehouse_id: int, data: dict) -> dict`
  - `stock.paginate_stock(warehouse_id: int, items_per_page: int = 50) -> AsyncIterator[dict]`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_stock.py
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.stock import StockModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def stock(session):
    return StockModule(session)


async def test_get_by_warehouse_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/1/items?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"variationId": 5}]},
    )
    result = await stock.get_by_warehouse(warehouse_id=1)
    assert result["entries"][0]["variationId"] == 5


async def test_get_by_warehouse_sends_pagination_params(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/2/items?page=2&itemsPerPage=10",
        json={"page": 2, "totalsCount": 20, "isLastPage": True, "entries": []},
    )
    result = await stock.get_by_warehouse(warehouse_id=2, page=2, items_per_page=10)
    assert result["page"] == 2


async def test_correct_puts_to_correction_url(httpx_mock, stock):
    payload = {"variationId": 5, "quantity": 10, "reasonId": 301, "warehouseLocationId": 0}
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/stock/warehouses/1/stock/correction",
        json={"success": True},
    )
    result = await stock.correct(warehouse_id=1, data=payload)
    assert result == {"success": True}


async def test_paginate_stock_yields_all_items(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/1/items?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"variationId": 1}, {"variationId": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/1/items?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"variationId": 3}],
        },
    )
    results = [s async for s in stock.paginate_stock(warehouse_id=1, items_per_page=2)]
    assert [r["variationId"] for r in results] == [1, 2, 3]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_stock.py -v
```

Expected: `AttributeError` — `StockModule` has no methods yet

- [ ] **Step 3: Implement `src/plentymarkets/modules/stock.py`**

```python
from __future__ import annotations

from typing import AsyncIterator

from .._session import _Session


class StockModule:
    """Wraps the PlentyMarkets ``/rest/stock`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get_by_warehouse(
        self,
        warehouse_id: int,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict:
        """Get stock levels for all variations in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of variation stock entries.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Stock entry dicts, each with:

                - ``warehouseId`` (int): Warehouse ID.
                - ``itemId`` (int): Item ID.
                - ``variationId`` (int): Variation ID.
                - ``netStock`` (float): Stock available for sale.
                - ``physicalStock`` (float): Total physical stock on hand.
                - ``reservedStock`` (float): Stock reserved by open orders.
                - ``reorderLevel`` (float): Reorder trigger threshold.
                - ``maximumStock`` (float): Maximum stock threshold.
                - ``averagePurchasePrice`` (float): Average net purchase price.
        """
        return await self._session.get(
            f"/rest/stock/warehouses/{warehouse_id}/items",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def correct(self, warehouse_id: int, data: dict) -> dict:
        """Correct the stock of a variation in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            data: Correction payload dict with the following keys:

                - ``variationId`` (int): Variation ID to correct.
                - ``quantity`` (float): New absolute stock quantity.
                - ``reasonId`` (int): Correction reason ID (e.g. 301=stock
                  correction, 304=incoming items).
                - ``warehouseLocationId`` (int): Storage location ID (0 for
                  the warehouse default).

        Returns:
            An empty dict on success (the API returns no body).
        """
        return await self._session.put(
            f"/rest/stock/warehouses/{warehouse_id}/stock/correction",
            json=data,
        )

    async def paginate_stock(
        self, warehouse_id: int, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every stock entry in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual stock entry dicts; same keys as ``get_by_warehouse()``
            entries.
        """
        page = 1
        while True:
            result = await self.get_by_warehouse(
                warehouse_id, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_stock.py -v
```

Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/modules/stock.py tests/test_stock.py
git commit -m "feat: add StockModule (get_by_warehouse, correct, paginate)"
```

---

### Task 8: Contacts Module

**Files:**
- Modify: `src/plentymarkets/modules/contacts.py` (replace stub)
- Create: `tests/test_contacts.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.post`, `_Session.put`
- Produces:
  - `await contacts.get(contact_id: int) -> dict`
  - `await contacts.list(page: int = 1, items_per_page: int = 50) -> dict`
  - `await contacts.create(data: dict) -> dict`
  - `await contacts.update(contact_id: int, data: dict) -> dict`
  - `contacts.paginate_contacts(items_per_page: int = 50) -> AsyncIterator[dict]`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_contacts.py
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.contacts import ContactsModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def contacts(session):
    return ContactsModule(session)


async def test_get_calls_correct_url(httpx_mock, contacts):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts/7",
        json={"id": 7, "firstName": "Max"},
    )
    result = await contacts.get(7)
    assert result["id"] == 7


async def test_list_sends_pagination_params(httpx_mock, contacts):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await contacts.list()
    assert result["page"] == 1


async def test_create_posts_data(httpx_mock, contacts):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/accounts/contacts",
        json={"id": 88, "firstName": "Anna"},
    )
    result = await contacts.create({"firstName": "Anna", "typeId": 1})
    assert result["id"] == 88


async def test_update_puts_to_contact_url(httpx_mock, contacts):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/accounts/contacts/7",
        json={"id": 7, "firstName": "Max Updated"},
    )
    result = await contacts.update(7, {"firstName": "Max Updated"})
    assert result["firstName"] == "Max Updated"


async def test_paginate_contacts_yields_all_contacts(httpx_mock, contacts):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [c async for c in contacts.paginate_contacts(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_contacts.py -v
```

Expected: `AttributeError` — `ContactsModule` has no methods yet

- [ ] **Step 3: Implement `src/plentymarkets/modules/contacts.py`**

```python
from __future__ import annotations

from typing import AsyncIterator

from .._session import _Session


class ContactsModule:
    """Wraps the PlentyMarkets ``/rest/accounts/contacts`` endpoints.

    Note: PlentyMarkets groups contacts under the ``Account`` API tag.
    The root path is ``/rest/accounts/contacts``, not ``/rest/contacts``.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, contact_id: int) -> dict:
        """Get a single contact by ID.

        Args:
            contact_id: The PlentyMarkets contact ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The contact ID.
            - ``number`` (str): External contact number.
            - ``externalId`` (str): External system ID.
            - ``typeId`` (int): Contact type (1=customer, 2=interested party,
              3=sales rep, 4=supplier, 5=manufacturer, 6=partner).
            - ``firstName`` (str): First name.
            - ``lastName`` (str): Last name.
            - ``fullName`` (str): Formatted full name.
            - ``email`` (str): Primary e-mail address.
            - ``phone`` (str): Primary phone number.
            - ``gender`` (str): Gender (``"male"``, ``"female"``, ``"diverse"``).
            - ``lang`` (str): Preferred language code (e.g. ``"de"``, ``"en"``).
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``userId`` (int): Assigned back-end user ID.
            - ``classId`` (int): Customer class ID.
            - ``blocked`` (int): ``0`` = active, ``1`` = blocked.
            - ``rating`` (int): Internal rating (1–5).
            - ``countryId`` (int): Country ID.
            - ``vatNumber`` (str): VAT registration number.
            - ``parentAccountId`` (int): Parent account/company ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.get(f"/rest/accounts/contacts/{contact_id}")

    async def list(self, page: int = 1, items_per_page: int = 50) -> dict:
        """List contacts with pagination.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching contacts.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Contact dicts; same keys as ``get()``.
        """
        return await self._session.get(
            "/rest/accounts/contacts",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def create(self, data: dict) -> dict:
        """Create a new contact.

        Args:
            data: Contact payload dict. Common keys: ``firstName``,
                ``lastName``, ``email``, ``typeId``, ``plentyId``.

        Returns:
            The created contact dict; same keys as ``get()``.
        """
        return await self._session.post("/rest/accounts/contacts", json=data)

    async def update(self, contact_id: int, data: dict) -> dict:
        """Update an existing contact.

        Args:
            contact_id: The PlentyMarkets contact ID.
            data: Fields to update (partial update supported).

        Returns:
            The updated contact dict; same keys as ``get()``.
        """
        return await self._session.put(
            f"/rest/accounts/contacts/{contact_id}", json=data
        )

    async def paginate_contacts(
        self, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every contact across all pages.

        Args:
            items_per_page: Results per page request (max 250).

        Yields:
            Individual contact dicts; same keys as ``get()``.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=items_per_page)
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_contacts.py -v
```

Expected: all tests pass

- [ ] **Step 5: Run the full test suite**

```bash
uv run pytest -v
```

Expected: all tests across all files pass

- [ ] **Step 6: Update `CHANGELOG.md` `[Unreleased]` section**

```markdown
## [Unreleased]

### Added
- `PlentyClient` async context manager with auto-managed token lifecycle
- `_Session` with login, logout, auto-refresh, and 401 re-login
- Exception hierarchy: `PlentyError`, `AuthError`, `NotFoundError`, `RateLimitError`, `ServerError`, `ConnectionError`
- `OrdersModule`: get, list, create, update_status, paginate_orders
- `ItemsModule`: get, list, create, update, paginate_items
- `StockModule`: get_by_warehouse, correct, paginate_stock
- `ContactsModule`: get, list, create, update, paginate_contacts
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/contacts.py tests/test_contacts.py CHANGELOG.md
git commit -m "feat: add ContactsModule (get, list, create, update, paginate)"
```
