# pyPlentyAPI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `plentymarkets` async Python package with session management, error handling, TypedDict payloads, and four core modules (Orders, Items, Stock, Contacts).

**Architecture:** `PlentyClient` owns a single `_Session` (httpx-based, auto-auth). Four module classes hold a reference to that session and call it directly. `_types.py` holds all `TypedDict` payload definitions. Tests mock at the httpx transport level via `pytest-httpx`.

**Tech Stack:** Python ≥3.11, httpx ≥0.27, pytest ≥8, pytest-asyncio ≥0.23, pytest-httpx ≥0.30, UV, pre-commit + commitizen.

## Global Constraints

- Python ≥3.11 (uses `Required`/`NotRequired` from `typing`, `X | Y` union syntax)
- All source lives under `src/plentymarkets/`
- `asyncio_mode = "auto"` in pytest — no `@pytest.mark.asyncio` decorator needed
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`
- Google-style docstrings on every public method; document every response key and every payload key
- `CHANGELOG.md`: only ever append to `[Unreleased]`; group by module
- Branch workflow: work on `staging`; `main` is protected
- PlentyMarkets login endpoint: `POST /rest/login` — body `{"username": ..., "password": ...}` — response `{"accessToken": str, "tokenType": "Bearer", "expiresIn": int, "refreshToken": str}`

---

### Task 1: Project scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.pre-commit-config.yaml`
- Create: `CHANGELOG.md`
- Create: `CLAUDE.md`
- Create: `src/plentymarkets/__init__.py` (empty placeholder)
- Create: `src/plentymarkets/client.py` (empty placeholder)
- Create: `src/plentymarkets/_session.py` (empty placeholder)
- Create: `src/plentymarkets/_exceptions.py` (empty placeholder)
- Create: `src/plentymarkets/_types.py` (empty placeholder)
- Create: `src/plentymarkets/modules/__init__.py` (empty)
- Create: `src/plentymarkets/modules/orders.py` (empty placeholder)
- Create: `src/plentymarkets/modules/items.py` (empty placeholder)
- Create: `src/plentymarkets/modules/stock.py` (empty placeholder)
- Create: `src/plentymarkets/modules/contacts.py` (empty placeholder)
- Create: `tests/__init__.py` (empty)
- Create: `tests/conftest.py` (empty placeholder)

**Interfaces:**
- Produces: installable package skeleton; `uv run pytest` exits with "no tests ran"

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[project]
name = "plentymarkets"
version = "0.1.0"
description = "Async Python client for the PlentyMarkets REST API"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-httpx>=0.30",
    "pre-commit>=3.7",
    "commitizen>=3.27",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/plentymarkets"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "integration: requires live PlentyMarkets credentials (set PLENTY_BASE_URL, PLENTY_USERNAME, PLENTY_PASSWORD)",
]

[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
version_files = ["pyproject.toml:version"]
```

- [ ] **Step 2: Create `.python-version`**

```
3.11
```

- [ ] **Step 3: Create `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.27.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

- [ ] **Step 4: Create `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
```

- [ ] **Step 5: Create `CLAUDE.md`**

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
- **Branch workflow:** All changes must branch off `staging` and be merged back into `staging`. `main` is protected and only updated via merges from `staging`.

## Package structure
```
src/plentymarkets/
  __init__.py        # exports PlentyClient
  client.py          # PlentyClient
  _session.py        # HTTP session, auth lifecycle
  _exceptions.py     # exception hierarchy
  _types.py          # TypedDict payload definitions
  modules/
    orders.py        # OrdersModule  → /rest/orders
    items.py         # ItemsModule   → /rest/items
    stock.py         # StockModule   → /rest/stockmanagement/warehouses/{id}/stock
    contacts.py      # ContactsModule → /rest/accounts/contacts
```

## Auth
POST /rest/login with username+password → accessToken + expiresIn (seconds).
Token sent as `Authorization: Bearer <token>` on every request.
Auto-refreshed when within 60 s of expiry. 401 mid-session → re-login once → retry.
```
```

- [ ] **Step 6: Create all empty source files**

```bash
mkdir -p src/plentymarkets/modules tests
touch src/plentymarkets/__init__.py
touch src/plentymarkets/client.py
touch src/plentymarkets/_session.py
touch src/plentymarkets/_exceptions.py
touch src/plentymarkets/_types.py
touch src/plentymarkets/modules/__init__.py
touch src/plentymarkets/modules/orders.py
touch src/plentymarkets/modules/items.py
touch src/plentymarkets/modules/stock.py
touch src/plentymarkets/modules/contacts.py
touch tests/__init__.py
touch tests/conftest.py
```

- [ ] **Step 7: Install dependencies and verify**

```bash
uv sync --extra dev
uv run pytest
```

Expected output: `no tests ran` (or similar, exit 0 or 5).

- [ ] **Step 8: Install pre-commit hook**

```bash
uv run pre-commit install --hook-type commit-msg
```

- [ ] **Step 9: Create staging branch and commit**

```bash
git checkout -b staging
git add pyproject.toml .python-version .pre-commit-config.yaml CHANGELOG.md CLAUDE.md src/ tests/
git commit -m "chore: scaffold project structure and tooling"
```

---

### Task 2: Exception hierarchy

**Files:**
- Modify: `src/plentymarkets/_exceptions.py`
- Create: `tests/test_exceptions.py`

**Interfaces:**
- Produces:
  - `PlentyError(Exception)` — base
  - `AuthError(PlentyError)` — 401
  - `NotFoundError(PlentyError)` — 404
  - `RateLimitError(PlentyError)` — 429, `.retry_after: int`
  - `ServerError(PlentyError)` — 5xx
  - `ConnectionError(PlentyError)` — network failure

- [ ] **Step 1: Write the failing test**

`tests/test_exceptions.py`:
```python
from plentymarkets._exceptions import (
    PlentyError,
    AuthError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ConnectionError,
)


def test_all_errors_are_plenty_error():
    assert issubclass(AuthError, PlentyError)
    assert issubclass(NotFoundError, PlentyError)
    assert issubclass(RateLimitError, PlentyError)
    assert issubclass(ServerError, PlentyError)
    assert issubclass(ConnectionError, PlentyError)


def test_rate_limit_error_exposes_retry_after():
    exc = RateLimitError("rate limited", retry_after=30)
    assert exc.retry_after == 30


def test_rate_limit_error_defaults_retry_after_to_zero():
    exc = RateLimitError("rate limited")
    assert exc.retry_after == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_exceptions.py -v
```

Expected: `ImportError` or `ModuleNotFoundError`.

- [ ] **Step 3: Write the implementation**

`src/plentymarkets/_exceptions.py`:
```python
class PlentyError(Exception):
    """Base exception for all PlentyMarkets API errors."""


class AuthError(PlentyError):
    """Raised on 401 — login failure or invalid/expired token."""


class NotFoundError(PlentyError):
    """Raised on 404 — requested resource does not exist."""


class RateLimitError(PlentyError):
    """Raised on 429 — API rate limit exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying, from the Retry-After
            response header. 0 if the header was absent.
    """

    def __init__(self, message: str, *, retry_after: int = 0) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class ServerError(PlentyError):
    """Raised on 5xx — PlentyMarkets server-side error."""


class ConnectionError(PlentyError):
    """Raised when the network is unreachable, DNS fails, or the request times out."""
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run pytest tests/test_exceptions.py -v
```

Expected: all 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/_exceptions.py tests/test_exceptions.py
git commit -m "feat: add exception hierarchy"
```

---

### Task 3: HTTP session

**Files:**
- Modify: `src/plentymarkets/_session.py`
- Modify: `tests/conftest.py`
- Create: `tests/test_session.py`

**Interfaces:**
- Consumes: `AuthError`, `NotFoundError`, `RateLimitError`, `ServerError`, `ConnectionError` from `_exceptions.py`
- Produces:
  - `_Session(base_url: str, username: str, password: str)`
    - `async login() -> None`
    - `async logout() -> None`
    - `async aclose() -> None`
    - `async get(path: str, **kwargs) -> dict`
    - `async post(path: str, **kwargs) -> dict`
    - `async put(path: str, **kwargs) -> dict`
    - `async delete(path: str, **kwargs) -> dict | None`
    - `_token: str | None` (inspectable in tests)
    - `_token_expiry: datetime | None`

- [ ] **Step 1: Write conftest fixtures**

`tests/conftest.py`:
```python
import pytest

BASE_URL = "https://test.plentymarkets.com"
USERNAME = "test@example.com"
PASSWORD = "secret"

LOGIN_RESPONSE = {
    "accessToken": "test-access-token",
    "tokenType": "Bearer",
    "expiresIn": 86400,
    "refreshToken": "test-refresh-token",
}


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def login_response() -> dict:
    return LOGIN_RESPONSE
```

- [ ] **Step 2: Write the failing tests**

`tests/test_session.py`:
```python
from datetime import datetime, timedelta, timezone

import pytest

from plentymarkets._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from plentymarkets._session import _Session

BASE_URL = "https://test.plentymarkets.com"


@pytest.fixture
def session() -> _Session:
    return _Session(BASE_URL, "user@example.com", "secret")


# --- login ---

async def test_login_posts_credentials(httpx_mock, session, login_response):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    await session.login()
    request = httpx_mock.get_requests()[0]
    assert request.method == "POST"
    import json
    body = json.loads(request.content)
    assert body["username"] == "user@example.com"
    assert body["password"] == "secret"


async def test_login_stores_token(httpx_mock, session, login_response):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    await session.login()
    assert session._token == "test-access-token"
    assert session._token_expiry is not None


async def test_login_401_raises_auth_error(httpx_mock, session):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", status_code=401)
    with pytest.raises(AuthError):
        await session.login()


# --- token injection ---

async def test_request_sends_bearer_token(httpx_mock, session, login_response):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", json={"id": 1})
    await session.get("/rest/orders/1")
    get_request = httpx_mock.get_requests()[1]
    assert get_request.headers["Authorization"] == "Bearer test-access-token"


# --- auto-login ---

async def test_auto_login_on_first_request(httpx_mock, session, login_response):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", json={"id": 1})
    assert session._token is None
    await session.get("/rest/orders/1")
    assert session._token == "test-access-token"


# --- near-expiry refresh ---

async def test_near_expiry_triggers_relogin(httpx_mock, session, login_response):
    # Pre-set token as near-expired (within 60 s)
    session._token = "old-token"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(seconds=30)
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", json={"id": 1})
    await session.get("/rest/orders/1")
    # login was called to refresh
    login_req = httpx_mock.get_requests()[0]
    assert "/rest/login" in str(login_req.url)
    assert session._token == "test-access-token"


async def test_valid_token_not_refreshed(httpx_mock, session, login_response):
    session._token = "valid-token"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", json={"id": 1})
    await session.get("/rest/orders/1")
    # only one request, no login
    assert len(httpx_mock.get_requests()) == 1


# --- 401 mid-session retry ---

async def test_401_triggers_relogin_and_retry(httpx_mock, session, login_response):
    session._token = "expired-token"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", status_code=401)
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", json={"id": 1})
    result = await session.get("/rest/orders/1")
    assert result == {"id": 1}


async def test_401_after_relogin_raises_auth_error(httpx_mock, session, login_response):
    session._token = "expired-token"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", status_code=401)
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", status_code=401)
    with pytest.raises(AuthError):
        await session.get("/rest/orders/1")


# --- error mapping ---

async def test_404_raises_not_found(httpx_mock, session, login_response):
    session._token = "tok"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/999", status_code=404)
    with pytest.raises(NotFoundError):
        await session.get("/rest/orders/999")


async def test_429_raises_rate_limit_with_retry_after(httpx_mock, session):
    session._token = "tok"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/1",
        status_code=429,
        headers={"Retry-After": "60"},
    )
    with pytest.raises(RateLimitError) as exc_info:
        await session.get("/rest/orders/1")
    assert exc_info.value.retry_after == 60


async def test_500_raises_server_error(httpx_mock, session):
    session._token = "tok"
    session._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", status_code=500)
    with pytest.raises(ServerError):
        await session.get("/rest/orders/1")


# --- logout ---

async def test_logout_clears_token(httpx_mock, session, login_response):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/login", json=login_response)
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/logout", status_code=200, json={})
    await session.login()
    await session.logout()
    assert session._token is None
    assert session._token_expiry is None
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
uv run pytest tests/test_session.py -v
```

Expected: `ImportError` from `_session`.

- [ ] **Step 4: Write the implementation**

`src/plentymarkets/_session.py`:
```python
from datetime import datetime, timedelta, timezone

import httpx

from plentymarkets._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

_REFRESH_BEFORE_SECONDS = 60


class _Session:
    """Manages the httpx client and PlentyMarkets auth lifecycle.

    Handles automatic login on first use, proactive token refresh when within
    60 seconds of expiry, and a single re-login retry on unexpected 401 responses.
    """

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._client = httpx.AsyncClient(base_url=self._base_url)
        self._token: str | None = None
        self._token_expiry: datetime | None = None

    async def login(self) -> None:
        """Authenticate with PlentyMarkets and store the access token.

        Raises:
            AuthError: If the server returns 401 (wrong credentials).
            ConnectionError: If the server cannot be reached.
        """
        try:
            response = await self._client.post(
                "/rest/login",
                json={"username": self._username, "password": self._password},
            )
        except httpx.TransportError as exc:
            raise ConnectionError(str(exc)) from exc

        if response.status_code == 401:
            raise AuthError("Login failed: invalid username or password")
        self._raise_for_status(response)

        data = response.json()
        self._token = data["accessToken"]
        self._token_expiry = datetime.now(timezone.utc) + timedelta(
            seconds=data["expiresIn"]
        )

    async def logout(self) -> None:
        """Invalidate the current session on the server and clear local token state."""
        if self._token is None:
            return
        try:
            await self._client.post(
                "/rest/logout",
                headers={"Authorization": f"Bearer {self._token}"},
            )
        except httpx.TransportError:
            pass
        finally:
            self._token = None
            self._token_expiry = None

    async def aclose(self) -> None:
        """Close the underlying httpx client. Call this when not using a context manager."""
        await self._client.aclose()

    async def _ensure_auth(self) -> None:
        if self._token is None or self._token_expiry is None:
            await self.login()
            return
        if datetime.now(timezone.utc) >= self._token_expiry - timedelta(
            seconds=_REFRESH_BEFORE_SECONDS
        ):
            await self.login()

    async def _send(self, method: str, path: str, **kwargs) -> httpx.Response:
        headers = {"Authorization": f"Bearer {self._token}"}
        existing = kwargs.pop("headers", {})
        headers.update(existing)
        try:
            return await self._client.request(method, path, headers=headers, **kwargs)
        except httpx.TransportError as exc:
            raise ConnectionError(str(exc)) from exc

    async def _request(self, method: str, path: str, **kwargs) -> dict | None:
        await self._ensure_auth()
        response = await self._send(method, path, **kwargs)

        if response.status_code == 401:
            await self.login()
            response = await self._send(method, path, **kwargs)
            if response.status_code == 401:
                raise AuthError("Authentication failed after re-login attempt")

        self._raise_for_status(response)

        if not response.content:
            return None
        return response.json()

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        if response.status_code == 401:
            raise AuthError("Unauthorized")
        if response.status_code == 404:
            raise NotFoundError(f"Not found: {response.url}")
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 0))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if response.status_code >= 500:
            raise ServerError(f"Server error {response.status_code}: {response.url}")
        response.raise_for_status()

    async def get(self, path: str, **kwargs) -> dict | list:
        """Send a GET request and return parsed JSON."""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> dict | list:
        """Send a POST request and return parsed JSON."""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> dict | list:
        """Send a PUT request and return parsed JSON."""
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> dict | list | None:
        """Send a DELETE request. Returns parsed JSON or None if body is empty."""
        return await self._request("DELETE", path, **kwargs)
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
uv run pytest tests/test_session.py -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/plentymarkets/_session.py tests/conftest.py tests/test_session.py
git commit -m "feat: add HTTP session with auth lifecycle and error mapping"
```

---

### Task 4: PlentyClient

**Files:**
- Modify: `src/plentymarkets/client.py`
- Modify: `src/plentymarkets/__init__.py`
- Create: `tests/test_client.py`

**Interfaces:**
- Consumes: `_Session` from `_session.py`; module classes (imported lazily inside properties to avoid circular imports)
- Produces:
  - `PlentyClient(base_url: str, username: str, password: str)`
    - `async __aenter__() -> PlentyClient`
    - `async __aexit__(...) -> None`
    - `async login() -> None`
    - `async logout() -> None`
    - `async aclose() -> None`
    - `@property orders -> OrdersModule`
    - `@property items -> ItemsModule`
    - `@property stock -> StockModule`
    - `@property contacts -> ContactsModule`

- [ ] **Step 1: Write the failing tests**

`tests/test_client.py`:
```python
import pytest
from unittest.mock import AsyncMock, patch

from plentymarkets import PlentyClient

BASE_URL = "https://test.plentymarkets.com"


async def test_context_manager_calls_login_and_logout():
    with patch("plentymarkets._session._Session.login", new_callable=AsyncMock) as mock_login, \
         patch("plentymarkets._session._Session.logout", new_callable=AsyncMock) as mock_logout, \
         patch("plentymarkets._session._Session.aclose", new_callable=AsyncMock):
        async with PlentyClient(BASE_URL, "user", "pass"):
            mock_login.assert_awaited_once()
        mock_logout.assert_awaited_once()


async def test_orders_property_returns_orders_module():
    from plentymarkets.modules.orders import OrdersModule
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.orders, OrdersModule)


async def test_items_property_returns_items_module():
    from plentymarkets.modules.items import ItemsModule
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.items, ItemsModule)


async def test_stock_property_returns_stock_module():
    from plentymarkets.modules.stock import StockModule
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.stock, StockModule)


async def test_contacts_property_returns_contacts_module():
    from plentymarkets.modules.contacts import ContactsModule
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.contacts, ContactsModule)


async def test_module_properties_are_cached():
    client = PlentyClient(BASE_URL, "user", "pass")
    assert client.orders is client.orders


def test_plentymarkets_exports_public_api():
    import plentymarkets
    assert hasattr(plentymarkets, "PlentyClient")
    assert hasattr(plentymarkets, "PlentyError")
    assert hasattr(plentymarkets, "AuthError")
    assert hasattr(plentymarkets, "NotFoundError")
    assert hasattr(plentymarkets, "RateLimitError")
    assert hasattr(plentymarkets, "ServerError")
    assert hasattr(plentymarkets, "ConnectionError")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_client.py -v
```

Expected: `ImportError` or `ModuleNotFoundError`.

- [ ] **Step 3: Create empty module classes so imports resolve**

`src/plentymarkets/modules/orders.py`:
```python
from plentymarkets._session import _Session


class OrdersModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

`src/plentymarkets/modules/items.py`:
```python
from plentymarkets._session import _Session


class ItemsModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

`src/plentymarkets/modules/stock.py`:
```python
from plentymarkets._session import _Session


class StockModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

`src/plentymarkets/modules/contacts.py`:
```python
from plentymarkets._session import _Session


class ContactsModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
```

- [ ] **Step 4: Write `client.py`**

`src/plentymarkets/client.py`:
```python
from __future__ import annotations

from typing import TYPE_CHECKING

from plentymarkets._session import _Session

if TYPE_CHECKING:
    from plentymarkets.modules.contacts import ContactsModule
    from plentymarkets.modules.items import ItemsModule
    from plentymarkets.modules.orders import OrdersModule
    from plentymarkets.modules.stock import StockModule


class PlentyClient:
    """Async client for the PlentyMarkets REST API.

    Use as an async context manager (recommended) or call `login()` / `aclose()` manually.

    Args:
        base_url: Base URL of your PlentyMarkets system,
            e.g. ``"https://your-shop.plentymarkets.com"``.
        username: PlentyMarkets back-end username.
        password: PlentyMarkets back-end password.

    Example:
        async with PlentyClient(base_url, username, password) as client:
            order = await client.orders.get(42)
    """

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self._session = _Session(base_url, username, password)
        self._orders: OrdersModule | None = None
        self._items: ItemsModule | None = None
        self._stock: StockModule | None = None
        self._contacts: ContactsModule | None = None

    async def __aenter__(self) -> PlentyClient:
        await self._session.login()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._session.logout()
        await self._session.aclose()

    async def login(self) -> None:
        """Authenticate with PlentyMarkets. Called automatically on first request."""
        await self._session.login()

    async def logout(self) -> None:
        """Invalidate the current session on the server."""
        await self._session.logout()

    async def aclose(self) -> None:
        """Close the underlying HTTP client. Must be called when not using a context manager."""
        await self._session.aclose()

    @property
    def orders(self) -> OrdersModule:
        """Access the Orders module (``/rest/orders``)."""
        if self._orders is None:
            from plentymarkets.modules.orders import OrdersModule
            self._orders = OrdersModule(self._session)
        return self._orders

    @property
    def items(self) -> ItemsModule:
        """Access the Items module (``/rest/items``)."""
        if self._items is None:
            from plentymarkets.modules.items import ItemsModule
            self._items = ItemsModule(self._session)
        return self._items

    @property
    def stock(self) -> StockModule:
        """Access the Stock module (``/rest/stockmanagement/warehouses/{id}/stock``)."""
        if self._stock is None:
            from plentymarkets.modules.stock import StockModule
            self._stock = StockModule(self._session)
        return self._stock

    @property
    def contacts(self) -> ContactsModule:
        """Access the Contacts module (``/rest/accounts/contacts``)."""
        if self._contacts is None:
            from plentymarkets.modules.contacts import ContactsModule
            self._contacts = ContactsModule(self._session)
        return self._contacts
```

- [ ] **Step 5: Write `__init__.py`**

`src/plentymarkets/__init__.py`:
```python
from plentymarkets._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    PlentyError,
    RateLimitError,
    ServerError,
)
from plentymarkets.client import PlentyClient

__all__ = [
    "PlentyClient",
    "PlentyError",
    "AuthError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ConnectionError",
]
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
uv run pytest tests/test_client.py -v
```

Expected: all tests PASS.

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/client.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/ tests/test_client.py
git commit -m "feat: add PlentyClient with lazy module properties"
```

---

### Task 5: TypedDict payload definitions

**Files:**
- Modify: `src/plentymarkets/_types.py`

**Interfaces:**
- Produces (all importable from `plentymarkets._types`):
  - `OrderCreatePayload`, `OrderUpdatePayload`
  - `ItemCreatePayload`, `ItemUpdatePayload`
  - `StockCorrectionEntry`, `StockCorrectionPayload`
  - `ContactCreatePayload`, `ContactUpdatePayload`

No separate test file — TypedDicts are pure type hints (plain dicts at runtime).
Module tests in Tasks 6–9 will import and use them.

- [ ] **Step 1: Write `_types.py`**

`src/plentymarkets/_types.py`:
```python
from typing import NotRequired, Required, TypedDict


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------

class OrderCreatePayload(TypedDict, total=False):
    """Payload for POST /rest/orders.

    Keys:
        typeId: Order type ID. 1=sales order, 2=delivery order, 3=returns,
            4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
            9=multi-order. **Required.**
        plentyId: Client (store) ID the order belongs to. **Required.**
        statusId: Order status ID (decimal, e.g. 3.0 = waiting for payment).
        ownerId: User ID of the order owner.
        lockStatus: Lock state string. ``"unlocked"`` or ``"locked"``.
        orderItems: List of order item dicts (see OrderItem schema).
        properties: List of order property dicts (typeId + value).
        addressRelations: List of address relation dicts
            (typeId 1=billing, 2=delivery; addressId).
        relations: List of relation dicts (referenceType, referenceId, relation).
    """

    typeId: Required[int]
    plentyId: Required[int]
    statusId: NotRequired[float]
    ownerId: NotRequired[int]
    lockStatus: NotRequired[str]
    orderItems: NotRequired[list[dict]]
    properties: NotRequired[list[dict]]
    addressRelations: NotRequired[list[dict]]
    relations: NotRequired[list[dict]]


class OrderUpdatePayload(TypedDict, total=False):
    """Payload for PUT /rest/orders/{orderId}.

    Keys:
        plentyId: Client (store) ID.
        statusId: New order status ID.
        ownerId: New owner user ID.
        orderItems: Updated list of order item dicts.
        properties: Updated list of order property dicts.
        addressRelations: Updated list of address relation dicts.
        relations: Updated list of relation dicts.
    """

    plentyId: NotRequired[int]
    statusId: NotRequired[float]
    ownerId: NotRequired[int]
    orderItems: NotRequired[list[dict]]
    properties: NotRequired[list[dict]]
    addressRelations: NotRequired[list[dict]]
    relations: NotRequired[list[dict]]


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------

class ItemCreatePayload(TypedDict, total=False):
    """Payload for POST /rest/items.

    At minimum, provide ``variations`` with one entry to create a usable item.

    Keys:
        position: Display position in item lists.
        stockType: 0=stocked, 1=noStock, 2=supplier, 3=producedBySelf.
        storeSpecial: Special shop display flag (0=none, 1=specialOffer,
            2=newItem, 3=topItem).
        ownerId: User ID of the item owner.
        manufacturerId: ID of the manufacturer.
        condition: Item condition (0=new, 1=used, 2=boxOpened, 3=newWithDefect,
            4=refurbished).
        conditionApi: Condition exported to marketplaces
            (0=new, 1=used, 2=notSpecified, 3=defective, 4=refurbished).
        customsTariffNumber: Customs tariff / HS code string.
        revenueAccount: Revenue account number for accounting.
        couponRestriction: 0=permitAll, 1=forbidAll, 2=allowCouponsOnly.
        isSubscribable: Whether the item can be subscribed to.
        isShippingPackage: Whether to use package shipping rules.
        flagOne: Item flag 1 (integer, shop-specific).
        flagTwo: Item flag 2 (integer, shop-specific).
        ageRestriction: Age restriction in years (0, 6, 12, 14, 16, 18, 50).
        itemType: ``"Default"``, ``"Bundle"``, ``"BundleItem"``.
        amazonFbaPlatform: 0=none, 1=AMAZON_EU, 2=AMAZON_FE, 3=AMAZON_NA.
        isShippableByAmazon: Whether Amazon can ship this item.
        amazonProductType: Amazon product type number.
        ebayPresetId: eBay listing preset ID.
        ebayCategory: Primary eBay category ID.
        ebayCategory2: Secondary eBay category ID.
        rakutenCategoryId: Rakuten category ID.
        variations: List of variation dicts. Provide at least one variation.
    """

    position: NotRequired[int]
    stockType: NotRequired[int]
    storeSpecial: NotRequired[int]
    ownerId: NotRequired[int]
    manufacturerId: NotRequired[int]
    condition: NotRequired[int]
    conditionApi: NotRequired[int]
    customsTariffNumber: NotRequired[str]
    revenueAccount: NotRequired[int]
    couponRestriction: NotRequired[int]
    isSubscribable: NotRequired[bool]
    isShippingPackage: NotRequired[bool]
    flagOne: NotRequired[int]
    flagTwo: NotRequired[int]
    ageRestriction: NotRequired[int]
    itemType: NotRequired[str]
    amazonFbaPlatform: NotRequired[int]
    isShippableByAmazon: NotRequired[bool]
    amazonProductType: NotRequired[int]
    ebayPresetId: NotRequired[int]
    ebayCategory: NotRequired[int]
    ebayCategory2: NotRequired[int]
    rakutenCategoryId: NotRequired[int]
    variations: NotRequired[list[dict]]


class ItemUpdatePayload(TypedDict, total=False):
    """Payload for PUT /rest/items/{itemId}.

    Keys: same as ItemCreatePayload except ``variations`` (variations are
    managed via their own endpoints after creation).

    Keys:
        position: Display position in item lists.
        stockType: 0=stocked, 1=noStock, 2=supplier, 3=producedBySelf.
        storeSpecial: Special shop display flag.
        ownerId: User ID of the item owner.
        manufacturerId: ID of the manufacturer.
        condition: Item condition (0–4).
        conditionApi: Condition exported to marketplaces (0–4).
        customsTariffNumber: Customs tariff / HS code string.
        revenueAccount: Revenue account number.
        couponRestriction: 0=permitAll, 1=forbidAll, 2=allowCouponsOnly.
        isSubscribable: Whether the item can be subscribed to.
        isShippingPackage: Whether to use package shipping rules.
        flagOne: Item flag 1.
        flagTwo: Item flag 2.
        ageRestriction: Age restriction in years.
        itemType: ``"Default"``, ``"Bundle"``, ``"BundleItem"``.
        amazonFbaPlatform: 0=none, 1=AMAZON_EU, 2=AMAZON_FE, 3=AMAZON_NA.
        isShippableByAmazon: Whether Amazon can ship this item.
        amazonProductType: Amazon product type number.
        ebayPresetId: eBay listing preset ID.
        ebayCategory: Primary eBay category ID.
        ebayCategory2: Secondary eBay category ID.
        rakutenCategoryId: Rakuten category ID.
    """

    position: NotRequired[int]
    stockType: NotRequired[int]
    storeSpecial: NotRequired[int]
    ownerId: NotRequired[int]
    manufacturerId: NotRequired[int]
    condition: NotRequired[int]
    conditionApi: NotRequired[int]
    customsTariffNumber: NotRequired[str]
    revenueAccount: NotRequired[int]
    couponRestriction: NotRequired[int]
    isSubscribable: NotRequired[bool]
    isShippingPackage: NotRequired[bool]
    flagOne: NotRequired[int]
    flagTwo: NotRequired[int]
    ageRestriction: NotRequired[int]
    itemType: NotRequired[str]
    amazonFbaPlatform: NotRequired[int]
    isShippableByAmazon: NotRequired[bool]
    amazonProductType: NotRequired[int]
    ebayPresetId: NotRequired[int]
    ebayCategory: NotRequired[int]
    ebayCategory2: NotRequired[int]
    rakutenCategoryId: NotRequired[int]


# ---------------------------------------------------------------------------
# Stock
# ---------------------------------------------------------------------------

class StockCorrectionEntry(TypedDict, total=False):
    """A single stock correction line within StockCorrectionPayload.

    Keys:
        variationId: Variation ID to correct. **Required.**
        quantity: Target stock quantity (positive = stock in, negative = stock out).
            **Required.**
        storageLocationId: Storage location ID within the warehouse. **Required.**
        reasonId: Correction reason ID (e.g. 301=stocktaking). **Required.**
        batch: Batch number string (if batch management is enabled).
        bestBeforeDate: Best-before date in ISO 8601 format (``"YYYY-MM-DD"``).
    """

    variationId: Required[int]
    quantity: Required[float]
    storageLocationId: Required[int]
    reasonId: Required[int]
    batch: NotRequired[str]
    bestBeforeDate: NotRequired[str]


class StockCorrectionPayload(TypedDict):
    """Payload for PUT /rest/stockmanagement/warehouses/{warehouseId}/stock/correction.

    Keys:
        corrections: List of correction entries. Each entry must include
            ``variationId``, ``quantity``, ``storageLocationId``, and ``reasonId``.
    """

    corrections: list[StockCorrectionEntry]


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------

class ContactCreatePayload(TypedDict, total=False):
    """Payload for POST /rest/accounts/contacts.

    Keys:
        typeId: Contact type ID (1=customer, 2=interested party, 3=sales rep,
            4=supplier, 5=manufacturer, 6=partner).
        referrerId: Referrer ID (float, links to order referrer table).
        title: Title or form of address string.
        firstName: Contact first name.
        lastName: Contact last name.
        email: Primary email address.
        gender: ``"male"``, ``"female"``, or ``"diverse"``.
        lang: Two-letter ISO language code (e.g. ``"de"``, ``"en"``).
        plentyId: Client (store) ID the contact belongs to.
        options: List of contact option dicts (typeId, subTypeId, value, priority).
    """

    typeId: NotRequired[int]
    referrerId: NotRequired[float]
    title: NotRequired[str]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    email: NotRequired[str]
    gender: NotRequired[str]
    lang: NotRequired[str]
    plentyId: NotRequired[int]
    options: NotRequired[list[dict]]


class ContactUpdatePayload(TypedDict, total=False):
    """Payload for PUT /rest/accounts/contacts/{contactId}.

    Keys:
        title: Title or form of address string.
        firstName: Contact first name.
        lastName: Contact last name.
        email: Primary email address.
        gender: ``"male"``, ``"female"``, or ``"diverse"``.
        lang: Two-letter ISO language code (e.g. ``"de"``, ``"en"``).
        options: List of contact option dicts (typeId, subTypeId, value, priority).
    """

    title: NotRequired[str]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    email: NotRequired[str]
    gender: NotRequired[str]
    lang: NotRequired[str]
    options: NotRequired[list[dict]]
```

- [ ] **Step 2: Verify the types import cleanly**

```bash
uv run python -c "from plentymarkets._types import OrderCreatePayload, ItemCreatePayload, StockCorrectionPayload, ContactCreatePayload; print('OK')"
```

Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add src/plentymarkets/_types.py
git commit -m "feat: add TypedDict payload definitions for all core modules"
```

---

### Task 6: Orders module

**Files:**
- Modify: `src/plentymarkets/modules/orders.py`
- Create: `tests/test_orders.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.post`, `_Session.put`; `OrderCreatePayload`, `OrderUpdatePayload` from `_types`
- Produces: `OrdersModule`
  - `async get(order_id: int, *, with_: list[str] | None = None) -> dict`
  - `async list(*, page: int = 1, items_per_page: int = 50, **filters) -> dict`
  - `async create(data: OrderCreatePayload) -> dict`
  - `async update(order_id: int, data: OrderUpdatePayload) -> dict`
  - `async paginate(**filters) -> AsyncGenerator[dict, None]`

- [ ] **Step 1: Write the failing tests**

`tests/test_orders.py`:
```python
from datetime import datetime, timedelta, timezone

import pytest

from plentymarkets._session import _Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://test.plentymarkets.com"

ORDER = {
    "id": 1,
    "typeId": 1,
    "plentyId": 12345,
    "statusId": 3.0,
    "statusName": "Waiting for payment",
    "ownerId": 1,
    "createdAt": "2024-01-01T00:00:00+00:00",
    "updatedAt": "2024-01-01T00:00:00+00:00",
}

LIST_PAGE_1 = {"page": 1, "totalsCount": 2, "isLastPage": False, "entries": [ORDER]}
LIST_PAGE_2 = {"page": 2, "totalsCount": 2, "isLastPage": True, "entries": [{"id": 2, **ORDER}]}
LIST_EMPTY = {"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []}


@pytest.fixture
def session() -> _Session:
    s = _Session(BASE_URL, "user@example.com", "secret")
    s._token = "test-token"
    s._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def module(session) -> OrdersModule:
    return OrdersModule(session)


async def test_get_order(httpx_mock, module):
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/orders/1", json=ORDER)
    result = await module.get(1)
    assert result["id"] == 1


async def test_get_order_passes_with_param(httpx_mock, module):
    url = f"{BASE_URL}/rest/orders/1?with=addresses"
    httpx_mock.add_response(method="GET", url=url, json=ORDER)
    result = await module.get(1, with_=["addresses"])
    assert result is not None


async def test_list_orders_default_pagination(httpx_mock, module):
    url = f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50"
    httpx_mock.add_response(method="GET", url=url, json=LIST_PAGE_1)
    result = await module.list()
    assert result["entries"][0]["id"] == 1


async def test_list_orders_custom_page(httpx_mock, module):
    url = f"{BASE_URL}/rest/orders?page=2&itemsPerPage=25"
    httpx_mock.add_response(method="GET", url=url, json=LIST_PAGE_2)
    result = await module.list(page=2, items_per_page=25)
    assert result["page"] == 2


async def test_create_order(httpx_mock, module):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/orders", json=ORDER)
    result = await module.create({"typeId": 1, "plentyId": 12345})
    assert result["id"] == 1


async def test_create_order_sends_payload(httpx_mock, module):
    import json
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/orders", json=ORDER)
    await module.create({"typeId": 1, "plentyId": 12345})
    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["typeId"] == 1
    assert body["plentyId"] == 12345


async def test_update_order(httpx_mock, module):
    updated = {**ORDER, "statusId": 5.0}
    httpx_mock.add_response(method="PUT", url=f"{BASE_URL}/rest/orders/1", json=updated)
    result = await module.update(1, {"statusId": 5.0})
    assert result["statusId"] == 5.0


async def test_paginate_yields_all_items(httpx_mock, module):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=250",
        json=LIST_PAGE_1,
    )
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=250",
        json=LIST_PAGE_2,
    )
    items = [item async for item in module.paginate()]
    assert len(items) == 2
    assert items[0]["id"] == 1


async def test_paginate_stops_on_empty_page(httpx_mock, module):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=250",
        json=LIST_EMPTY,
    )
    items = [item async for item in module.paginate()]
    assert items == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_orders.py -v
```

Expected: `AttributeError` — module has no methods yet.

- [ ] **Step 3: Write the implementation**

`src/plentymarkets/modules/orders.py`:
```python
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

if TYPE_CHECKING:
    from plentymarkets._types import OrderCreatePayload, OrderUpdatePayload

from plentymarkets._session import _Session


class OrdersModule:
    """Wraps the PlentyMarkets Orders API (``/rest/orders``).

    Attributes:
        _session: Shared HTTP session from PlentyClient.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, order_id: int, *, with_: list[str] | None = None) -> dict:
        """Fetch a single order by ID.

        Args:
            order_id: The numeric order ID.
            with_: Optional list of relations to embed in the response.
                Possible values: ``"addresses"``, ``"relations"``,
                ``"orderItems"``, ``"comments"``, ``"location"``,
                ``"payments"``, ``"documents"``, ``"contactSender"``,
                ``"contactReceiver"``, ``"warehouseSender"``,
                ``"warehouseReceiver"``, ``"tags"``.

        Returns:
            dict with keys:
                id (int): Order ID.
                typeId (int): Order type (1=sales, 2=delivery, 3=returns, etc.).
                statusId (float): Order status ID.
                statusName (str): Human-readable status label.
                ownerId (int): User ID of the owner.
                referrerId (float): Referrer ID.
                createdAt (str): ISO 8601 creation timestamp.
                updatedAt (str): ISO 8601 last-updated timestamp.
                plentyId (int): Client (store) ID.
                locationId (int): Accounting location ID.
                lockStatus (str): ``"unlocked"`` or ``"locked"``.
                isLocked (bool): Whether the order is locked.
                addresses (list[dict]): Present when ``"addresses"`` in ``with_``.
                orderItems (list[dict]): Present when ``"orderItems"`` in ``with_``.
                relations (list[dict]): Present when ``"relations"`` in ``with_``.

        Raises:
            NotFoundError: If the order does not exist.
            AuthError: If authentication fails.
        """
        params: dict = {}
        if with_:
            params["with"] = ",".join(with_)
        return await self._session.get(f"/rest/orders/{order_id}", params=params)

    async def list(
        self,
        *,
        page: int = 1,
        items_per_page: int = 50,
        **filters,
    ) -> dict:
        """List orders with optional filters.

        Args:
            page: Page number (1-based). Defaults to 1.
            items_per_page: Results per page (max 250). Defaults to 50.
            **filters: Additional filter parameters passed as query params.
                Supported keys: ``orderType``, ``contactId``, ``referrerId``,
                ``statusFrom``, ``statusTo``, ``createdAtFrom``, ``createdAtTo``,
                ``updatedAtFrom``, ``updatedAtTo``, ``paidAtFrom``, ``paidAtTo``,
                ``warehouseId``, ``ownerUserId``, ``countryId``, ``orderIds``,
                ``externalOrderId``, ``clientId``, ``paymentStatus``,
                ``parentOrderId``, ``with``.

        Returns:
            dict with keys:
                page (int): Current page number.
                totalsCount (int): Total number of orders matching the filter.
                isLastPage (bool): Whether this is the final page.
                entries (list[dict]): List of order dicts (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        params = {"page": page, "itemsPerPage": items_per_page, **filters}
        return await self._session.get("/rest/orders", params=params)

    async def create(self, data: OrderCreatePayload) -> dict:
        """Create a new order.

        Args:
            data: Order payload. Use ``OrderCreatePayload`` for IDE autocomplete.
                Required keys: ``typeId``, ``plentyId``.
                Optional keys: ``statusId``, ``ownerId``, ``lockStatus``,
                ``orderItems``, ``properties``, ``addressRelations``, ``relations``.

        Returns:
            dict: The created order (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        return await self._session.post("/rest/orders", json=data)

    async def update(self, order_id: int, data: OrderUpdatePayload) -> dict:
        """Update an existing order.

        Args:
            order_id: The numeric order ID to update.
            data: Fields to update. Use ``OrderUpdatePayload`` for IDE autocomplete.
                Optional keys: ``plentyId``, ``statusId``, ``ownerId``,
                ``orderItems``, ``properties``, ``addressRelations``, ``relations``.

        Returns:
            dict: The updated order (same keys as ``get()``).

        Raises:
            NotFoundError: If the order does not exist.
            AuthError: If authentication fails.
        """
        return await self._session.put(f"/rest/orders/{order_id}", json=data)

    async def paginate(self, **filters) -> AsyncGenerator[dict, None]:
        """Async generator that yields every order matching ``filters``.

        Fetches pages of 250 items automatically and yields individual order
        dicts until the API signals the last page.

        Args:
            **filters: Same filter parameters as ``list()``.

        Yields:
            dict: Individual order dict (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=250, **filters)
            for entry in result.get("entries", []):
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_orders.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/modules/orders.py tests/test_orders.py
git commit -m "feat: add OrdersModule (get, list, create, update, paginate)"
```

---

### Task 7: Items module

**Files:**
- Modify: `src/plentymarkets/modules/items.py`
- Create: `tests/test_items.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.post`, `_Session.put`; `ItemCreatePayload`, `ItemUpdatePayload` from `_types`
- Produces: `ItemsModule`
  - `async get(item_id: int, *, lang: str | None = None) -> dict`
  - `async list(*, page: int = 1, items_per_page: int = 50, **filters) -> dict`
  - `async create(data: ItemCreatePayload) -> dict`
  - `async update(item_id: int, data: ItemUpdatePayload) -> dict`
  - `async paginate(**filters) -> AsyncGenerator[dict, None]`

- [ ] **Step 1: Write the failing tests**

`tests/test_items.py`:
```python
from datetime import datetime, timedelta, timezone

import pytest

from plentymarkets._session import _Session
from plentymarkets.modules.items import ItemsModule

BASE_URL = "https://test.plentymarkets.com"

ITEM = {
    "id": 101,
    "itemType": "Default",
    "stockType": 0,
    "ownerId": 1,
    "manufacturerId": None,
    "mainVariationId": 201,
    "createdAt": "2024-01-01T00:00:00+00:00",
    "updatedAt": "2024-01-01T00:00:00+00:00",
}

LIST_PAGE_1 = {"page": 1, "totalsCount": 2, "isLastPage": False, "entries": [ITEM]}
LIST_PAGE_2 = {"page": 2, "totalsCount": 2, "isLastPage": True, "entries": [{"id": 102, **ITEM}]}
LIST_EMPTY = {"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []}


@pytest.fixture
def session() -> _Session:
    s = _Session(BASE_URL, "user@example.com", "secret")
    s._token = "test-token"
    s._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def module(session) -> ItemsModule:
    return ItemsModule(session)


async def test_get_item(httpx_mock, module):
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/items/101", json=ITEM)
    result = await module.get(101)
    assert result["id"] == 101


async def test_get_item_with_lang(httpx_mock, module):
    httpx_mock.add_response(method="GET", url=f"{BASE_URL}/rest/items/101?lang=de", json=ITEM)
    result = await module.get(101, lang="de")
    assert result is not None


async def test_list_items_default_pagination(httpx_mock, module):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/items?page=1&itemsPerPage=50",
        json=LIST_PAGE_1,
    )
    result = await module.list()
    assert result["entries"][0]["id"] == 101


async def test_create_item(httpx_mock, module):
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/items", json=ITEM)
    result = await module.create({"itemType": "Default"})
    assert result["id"] == 101


async def test_create_item_sends_payload(httpx_mock, module):
    import json
    httpx_mock.add_response(method="POST", url=f"{BASE_URL}/rest/items", json=ITEM)
    await module.create({"itemType": "Default", "stockType": 0})
    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["itemType"] == "Default"


async def test_update_item(httpx_mock, module):
    updated = {**ITEM, "ownerId": 2}
    httpx_mock.add_response(method="PUT", url=f"{BASE_URL}/rest/items/101", json=updated)
    result = await module.update(101, {"ownerId": 2})
    assert result["ownerId"] == 2


async def test_paginate_yields_all_items(httpx_mock, module):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/items?page=1&itemsPerPage=250",
        json=LIST_PAGE_1,
    )
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/items?page=2&itemsPerPage=250",
        json=LIST_PAGE_2,
    )
    items = [item async for item in module.paginate()]
    assert len(items) == 2


async def test_paginate_stops_on_empty(httpx_mock, module):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/items?page=1&itemsPerPage=250",
        json=LIST_EMPTY,
    )
    items = [item async for item in module.paginate()]
    assert items == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_items.py -v
```

Expected: `AttributeError` — module has no methods yet.

- [ ] **Step 3: Write the implementation**

`src/plentymarkets/modules/items.py`:
```python
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

if TYPE_CHECKING:
    from plentymarkets._types import ItemCreatePayload, ItemUpdatePayload

from plentymarkets._session import _Session


class ItemsModule:
    """Wraps the PlentyMarkets Items API (``/rest/items``)."""

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, item_id: int, *, lang: str | None = None) -> dict:
        """Fetch a single item by ID.

        Args:
            item_id: The numeric item ID.
            lang: Optional two-letter ISO language code for text fields
                (e.g. ``"de"``, ``"en"``).

        Returns:
            dict with keys:
                id (int): Item ID.
                itemType (str): ``"Default"``, ``"Bundle"``, or ``"BundleItem"``.
                stockType (int): 0=stocked, 1=noStock, 2=supplier, 3=producedBySelf.
                storeSpecial (int | None): Shop display flag.
                ownerId (int): Owner user ID.
                manufacturerId (int | None): Manufacturer ID.
                producingCountryId (int | None): Country of manufacture ID.
                mainVariationId (int): ID of the main variation.
                revenueAccount (int | None): Revenue account number.
                couponRestriction (int): 0=permitAll, 1=forbidAll, 2=allowCouponsOnly.
                condition (int): Item condition (0–4).
                conditionApi (int): Condition for marketplaces (0–4).
                createdAt (str): ISO 8601 creation timestamp.
                updatedAt (str): ISO 8601 last-updated timestamp.
                isSubscribable (bool): Whether the item can be subscribed.
                isSerialNumber (bool): Whether serial number tracking is enabled.
                isShippingPackage (bool): Whether package shipping rules apply.
                amazonFbaPlatform (int): 0=none, 1=EU, 2=FE, 3=NA.
                isShippableByAmazon (bool): Whether Amazon can fulfil this item.
                amazonProductType (int | None): Amazon product type number.
                flagOne (int): Item flag 1.
                flagTwo (int): Item flag 2.
                ageRestriction (int): Age restriction in years.
                feedback (int | None): Average feedback rating.
                customsTariffNumber (str | None): HS / customs tariff code.

        Raises:
            NotFoundError: If the item does not exist.
            AuthError: If authentication fails.
        """
        params: dict = {}
        if lang:
            params["lang"] = lang
        return await self._session.get(f"/rest/items/{item_id}", params=params)

    async def list(
        self,
        *,
        page: int = 1,
        items_per_page: int = 50,
        **filters,
    ) -> dict:
        """List items with optional filters.

        Args:
            page: Page number (1-based). Defaults to 1.
            items_per_page: Results per page (max 250). Defaults to 50.
            **filters: Additional query params. Supported keys:
                ``name``, ``manufacturerId``, ``ownerId``, ``itemType``,
                ``flagOne``, ``flagTwo``, ``condition``, ``updatedBetween``,
                ``variationUpdatedBetween``, ``variationRelatedUpdatedBetween``,
                ``with`` (comma-separated relations: ``"variations"``,
                ``"itemProperties"``, ``"itemCrossSelling"``, ``"itemImages"``,
                ``"itemShippingProfiles"``, ``"ebayTitles"``).

        Returns:
            dict with keys:
                page (int): Current page number.
                totalsCount (int): Total number of items matching the filter.
                isLastPage (bool): Whether this is the final page.
                entries (list[dict]): List of item dicts (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        params = {"page": page, "itemsPerPage": items_per_page, **filters}
        return await self._session.get("/rest/items", params=params)

    async def create(self, data: ItemCreatePayload) -> dict:
        """Create a new item.

        Args:
            data: Item payload. Use ``ItemCreatePayload`` for IDE autocomplete.
                Include ``variations`` with at least one entry to create a usable item.

        Returns:
            dict: The created item (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        return await self._session.post("/rest/items", json=data)

    async def update(self, item_id: int, data: ItemUpdatePayload) -> dict:
        """Update an existing item.

        Args:
            item_id: The numeric item ID to update.
            data: Fields to update. Use ``ItemUpdatePayload`` for IDE autocomplete.

        Returns:
            dict: The updated item (same keys as ``get()``).

        Raises:
            NotFoundError: If the item does not exist.
            AuthError: If authentication fails.
        """
        return await self._session.put(f"/rest/items/{item_id}", json=data)

    async def paginate(self, **filters) -> AsyncGenerator[dict, None]:
        """Async generator that yields every item matching ``filters``.

        Args:
            **filters: Same filter parameters as ``list()``.

        Yields:
            dict: Individual item dict (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=250, **filters)
            for entry in result.get("entries", []):
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_items.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/modules/items.py tests/test_items.py
git commit -m "feat: add ItemsModule (get, list, create, update, paginate)"
```

---

### Task 8: Stock module

**Files:**
- Modify: `src/plentymarkets/modules/stock.py`
- Create: `tests/test_stock.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.put`; `StockCorrectionPayload` from `_types`
- Produces: `StockModule`
  - `async get_by_warehouse(warehouse_id: int, *, page: int = 1, items_per_page: int = 50, **filters) -> dict`
  - `async correct(warehouse_id: int, data: StockCorrectionPayload) -> dict`
  - `async paginate(warehouse_id: int, **filters) -> AsyncGenerator[dict, None]`

- [ ] **Step 1: Write the failing tests**

`tests/test_stock.py`:
```python
from datetime import datetime, timedelta, timezone

import pytest

from plentymarkets._session import _Session
from plentymarkets.modules.stock import StockModule

BASE_URL = "https://test.plentymarkets.com"

STOCK_ENTRY = {
    "variationId": 201,
    "warehouseId": 1,
    "physicalStock": 10.0,
    "reservedStock": 2.0,
    "netStock": 8.0,
    "reorderLevel": 5.0,
    "deltaReorderLevel": 3.0,
    "stockStorageLocation": {"id": 1, "name": "Default"},
    "updatedAt": "2024-01-01T00:00:00+00:00",
}

LIST_PAGE_1 = {"page": 1, "totalsCount": 2, "isLastPage": False, "entries": [STOCK_ENTRY]}
LIST_PAGE_2 = {"page": 2, "totalsCount": 2, "isLastPage": True, "entries": [{**STOCK_ENTRY, "variationId": 202}]}
LIST_EMPTY = {"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []}

CORRECTION_RESULT = [{"variationId": 201, "quantity": 15.0, "warehouseId": 1}]


@pytest.fixture
def session() -> _Session:
    s = _Session(BASE_URL, "user@example.com", "secret")
    s._token = "test-token"
    s._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def module(session) -> StockModule:
    return StockModule(session)


async def test_get_by_warehouse_default_params(httpx_mock, module):
    url = f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=1&itemsPerPage=50"
    httpx_mock.add_response(method="GET", url=url, json=LIST_PAGE_1)
    result = await module.get_by_warehouse(1)
    assert result["entries"][0]["variationId"] == 201


async def test_get_by_warehouse_custom_page(httpx_mock, module):
    url = f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=2&itemsPerPage=100"
    httpx_mock.add_response(method="GET", url=url, json=LIST_PAGE_2)
    result = await module.get_by_warehouse(1, page=2, items_per_page=100)
    assert result["page"] == 2


async def test_correct_stock(httpx_mock, module):
    url = f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock/correction"
    httpx_mock.add_response(method="PUT", url=url, json=CORRECTION_RESULT)
    result = await module.correct(
        1,
        {"corrections": [{"variationId": 201, "quantity": 15.0, "storageLocationId": 1, "reasonId": 301}]},
    )
    assert result[0]["variationId"] == 201


async def test_correct_stock_sends_payload(httpx_mock, module):
    import json
    url = f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock/correction"
    httpx_mock.add_response(method="PUT", url=url, json=CORRECTION_RESULT)
    await module.correct(
        1,
        {"corrections": [{"variationId": 201, "quantity": 15.0, "storageLocationId": 1, "reasonId": 301}]},
    )
    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["corrections"][0]["variationId"] == 201


async def test_paginate_yields_all_entries(httpx_mock, module):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=1&itemsPerPage=250",
        json=LIST_PAGE_1,
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=2&itemsPerPage=250",
        json=LIST_PAGE_2,
    )
    entries = [e async for e in module.paginate(1)]
    assert len(entries) == 2
    assert entries[0]["variationId"] == 201


async def test_paginate_stops_on_empty(httpx_mock, module):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=1&itemsPerPage=250",
        json=LIST_EMPTY,
    )
    entries = [e async for e in module.paginate(1)]
    assert entries == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_stock.py -v
```

Expected: `AttributeError` — module has no methods yet.

- [ ] **Step 3: Write the implementation**

`src/plentymarkets/modules/stock.py`:
```python
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

if TYPE_CHECKING:
    from plentymarkets._types import StockCorrectionPayload

from plentymarkets._session import _Session


class StockModule:
    """Wraps the PlentyMarkets Stock API
    (``/rest/stockmanagement/warehouses/{warehouseId}/stock``).
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get_by_warehouse(
        self,
        warehouse_id: int,
        *,
        page: int = 1,
        items_per_page: int = 50,
        **filters,
    ) -> dict:
        """List stock entries for a specific warehouse.

        Args:
            warehouse_id: The numeric warehouse ID.
            page: Page number (1-based). Defaults to 1.
            items_per_page: Results per page (max 250). Defaults to 50.
            **filters: Additional query params. Supported keys:
                ``variationId`` (int), ``updatedAtFrom`` (ISO 8601 str),
                ``updatedAtTo`` (ISO 8601 str), ``reasonId`` (int),
                ``columns`` (comma-separated list of fields to return).

        Returns:
            dict with keys:
                page (int): Current page number.
                totalsCount (int): Total number of stock entries.
                isLastPage (bool): Whether this is the final page.
                entries (list[dict]): List of stock entry dicts. Each entry has:
                    variationId (int): Variation ID.
                    warehouseId (int): Warehouse ID.
                    physicalStock (float): Total physical quantity on hand.
                    reservedStock (float): Quantity reserved by open orders.
                    netStock (float): Available quantity (physicalStock - reservedStock).
                    reorderLevel (float): Reorder threshold.
                    deltaReorderLevel (float): Gap between net stock and reorder level.
                    stockStorageLocation (dict): Storage location info (id, name).
                    updatedAt (str): ISO 8601 last-updated timestamp.

        Raises:
            NotFoundError: If the warehouse does not exist.
            AuthError: If authentication fails.
        """
        params = {"page": page, "itemsPerPage": items_per_page, **filters}
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock",
            params=params,
        )

    async def correct(self, warehouse_id: int, data: StockCorrectionPayload) -> list:
        """Perform a stock correction for one or more variations in a warehouse.

        Args:
            warehouse_id: The numeric warehouse ID.
            data: Correction payload. Use ``StockCorrectionPayload`` for IDE
                autocomplete. Must include ``corrections`` list. Each correction
                requires: ``variationId``, ``quantity``, ``storageLocationId``,
                ``reasonId``. Optional per-entry keys: ``batch``, ``bestBeforeDate``.

        Returns:
            list[dict]: List of correction result dicts. Each dict has:
                variationId (int): Variation ID.
                quantity (float): New quantity after correction.
                warehouseId (int): Warehouse ID.

        Raises:
            NotFoundError: If the warehouse does not exist.
            AuthError: If authentication fails.
        """
        return await self._session.put(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/correction",
            json=data,
        )

    async def paginate(
        self, warehouse_id: int, **filters
    ) -> AsyncGenerator[dict, None]:
        """Async generator that yields every stock entry for a warehouse.

        Args:
            warehouse_id: The numeric warehouse ID.
            **filters: Same filter parameters as ``get_by_warehouse()``.

        Yields:
            dict: Individual stock entry dict (same keys as entries in ``get_by_warehouse()``).

        Raises:
            NotFoundError: If the warehouse does not exist.
            AuthError: If authentication fails.
        """
        page = 1
        while True:
            result = await self.get_by_warehouse(
                warehouse_id, page=page, items_per_page=250, **filters
            )
            for entry in result.get("entries", []):
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_stock.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/plentymarkets/modules/stock.py tests/test_stock.py
git commit -m "feat: add StockModule (get_by_warehouse, correct, paginate)"
```

---

### Task 9: Contacts module

**Files:**
- Modify: `src/plentymarkets/modules/contacts.py`
- Create: `tests/test_contacts.py`

**Interfaces:**
- Consumes: `_Session.get`, `_Session.post`, `_Session.put`; `ContactCreatePayload`, `ContactUpdatePayload` from `_types`
- Produces: `ContactsModule`
  - `async get(contact_id: int, *, with_: list[str] | None = None) -> dict`
  - `async list(*, page: int = 1, items_per_page: int = 50, **filters) -> dict`
  - `async create(data: ContactCreatePayload) -> dict`
  - `async update(contact_id: int, data: ContactUpdatePayload) -> dict`
  - `async paginate(**filters) -> AsyncGenerator[dict, None]`

- [ ] **Step 1: Write the failing tests**

`tests/test_contacts.py`:
```python
from datetime import datetime, timedelta, timezone

import pytest

from plentymarkets._session import _Session
from plentymarkets.modules.contacts import ContactsModule

BASE_URL = "https://test.plentymarkets.com"

CONTACT = {
    "id": 501,
    "typeId": 1,
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane@example.com",
    "gender": "female",
    "lang": "en",
    "referrerId": 1.0,
    "plentyId": 12345,
    "createdAt": "2024-01-01T00:00:00+00:00",
    "updatedAt": "2024-01-01T00:00:00+00:00",
}

LIST_PAGE_1 = {"page": 1, "totalsCount": 2, "isLastPage": False, "entries": [CONTACT]}
LIST_PAGE_2 = {"page": 2, "totalsCount": 2, "isLastPage": True, "entries": [{"id": 502, **CONTACT}]}
LIST_EMPTY = {"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []}


@pytest.fixture
def session() -> _Session:
    s = _Session(BASE_URL, "user@example.com", "secret")
    s._token = "test-token"
    s._token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def module(session) -> ContactsModule:
    return ContactsModule(session)


async def test_get_contact(httpx_mock, module):
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/rest/accounts/contacts/501", json=CONTACT
    )
    result = await module.get(501)
    assert result["id"] == 501


async def test_get_contact_with_relations(httpx_mock, module):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts/501?with=addresses",
        json=CONTACT,
    )
    result = await module.get(501, with_=["addresses"])
    assert result is not None


async def test_list_contacts_default_pagination(httpx_mock, module):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=50",
        json=LIST_PAGE_1,
    )
    result = await module.list()
    assert result["entries"][0]["id"] == 501


async def test_create_contact(httpx_mock, module):
    httpx_mock.add_response(
        method="POST", url=f"{BASE_URL}/rest/accounts/contacts", json=CONTACT
    )
    result = await module.create({"typeId": 1, "firstName": "Jane", "lastName": "Doe"})
    assert result["id"] == 501


async def test_create_contact_sends_payload(httpx_mock, module):
    import json
    httpx_mock.add_response(
        method="POST", url=f"{BASE_URL}/rest/accounts/contacts", json=CONTACT
    )
    await module.create({"typeId": 1, "firstName": "Jane", "lastName": "Doe"})
    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["firstName"] == "Jane"


async def test_update_contact(httpx_mock, module):
    updated = {**CONTACT, "firstName": "Janet"}
    httpx_mock.add_response(
        method="PUT", url=f"{BASE_URL}/rest/accounts/contacts/501", json=updated
    )
    result = await module.update(501, {"firstName": "Janet"})
    assert result["firstName"] == "Janet"


async def test_paginate_yields_all_contacts(httpx_mock, module):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=250",
        json=LIST_PAGE_1,
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=2&itemsPerPage=250",
        json=LIST_PAGE_2,
    )
    contacts = [c async for c in module.paginate()]
    assert len(contacts) == 2
    assert contacts[0]["id"] == 501


async def test_paginate_stops_on_empty(httpx_mock, module):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=250",
        json=LIST_EMPTY,
    )
    contacts = [c async for c in module.paginate()]
    assert contacts == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_contacts.py -v
```

Expected: `AttributeError` — module has no methods yet.

- [ ] **Step 3: Write the implementation**

`src/plentymarkets/modules/contacts.py`:
```python
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

if TYPE_CHECKING:
    from plentymarkets._types import ContactCreatePayload, ContactUpdatePayload

from plentymarkets._session import _Session


class ContactsModule:
    """Wraps the PlentyMarkets Accounts/Contacts API (``/rest/accounts/contacts``)."""

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, contact_id: int, *, with_: list[str] | None = None) -> dict:
        """Fetch a single contact by ID.

        Args:
            contact_id: The numeric contact ID.
            with_: Optional list of relations to embed. Possible values:
                ``"addresses"``, ``"options"``, ``"relations"``,
                ``"bankAccounts"``, ``"orders"``.

        Returns:
            dict with keys:
                id (int): Contact ID.
                externalId (str | None): External system ID.
                number (str | None): Customer number.
                typeId (int): Contact type (1=customer, 2=interested party,
                    3=sales rep, 4=supplier, 5=manufacturer, 6=partner).
                firstName (str | None): First name.
                lastName (str | None): Last name.
                fullName (str | None): Concatenated full name.
                email (str | None): Primary email address.
                secondaryEmail (str | None): Secondary email address.
                gender (str | None): ``"male"``, ``"female"``, or ``"diverse"``.
                title (str | None): Title or form of address.
                newsletterAllowanceAt (str | None): ISO 8601 timestamp of newsletter opt-in.
                classId (int | None): Contact class ID.
                blocked (int): 0=not blocked, 1=blocked.
                rating (int): Internal rating (0–5).
                lang (str): Two-letter ISO language code.
                referrerId (float): Referrer ID.
                plentyId (int): Client (store) ID.
                userId (int | None): Assigned user ID.
                birthdayAt (str | None): ISO 8601 date of birth.
                lastLoginAt (str | None): ISO 8601 last login timestamp.
                lastOrderAt (str | None): ISO 8601 timestamp of last order.
                createdAt (str): ISO 8601 creation timestamp.
                updatedAt (str): ISO 8601 last-updated timestamp.
                privatePhone (str | None): Private phone number.
                privateMobile (str | None): Private mobile number.
                ebayName (str | None): eBay username.
                addresses (list[dict]): Present when ``"addresses"`` in ``with_``.
                options (list[dict]): Present when ``"options"`` in ``with_``.

        Raises:
            NotFoundError: If the contact does not exist.
            AuthError: If authentication fails.
        """
        params: dict = {}
        if with_:
            params["with"] = ",".join(with_)
        return await self._session.get(
            f"/rest/accounts/contacts/{contact_id}", params=params
        )

    async def list(
        self,
        *,
        page: int = 1,
        items_per_page: int = 50,
        **filters,
    ) -> dict:
        """List contacts with optional filters.

        Args:
            page: Page number (1-based). Defaults to 1.
            items_per_page: Results per page (max 250). Defaults to 50.
            **filters: Additional query params. Supported keys:
                ``fullText`` (str), ``contactEmail`` (str), ``email`` (str),
                ``name`` (str), ``nameOrId`` (str), ``typeId`` (int),
                ``referrerId`` (float), ``plentyId`` (int),
                ``countryId`` (int), ``externalId`` (str), ``number`` (str),
                ``createdAtAfter`` (ISO 8601 str), ``createdAtBefore`` (ISO 8601 str),
                ``updatedAtAfter`` (ISO 8601 str), ``updatedAtBefore`` (ISO 8601 str),
                ``tagIds`` (comma-separated int list), ``with`` (str).

        Returns:
            dict with keys:
                page (int): Current page number.
                totalsCount (int): Total number of contacts matching the filter.
                isLastPage (bool): Whether this is the final page.
                entries (list[dict]): List of contact dicts (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        params = {"page": page, "itemsPerPage": items_per_page, **filters}
        return await self._session.get("/rest/accounts/contacts", params=params)

    async def create(self, data: ContactCreatePayload) -> dict:
        """Create a new contact.

        Args:
            data: Contact payload. Use ``ContactCreatePayload`` for IDE autocomplete.
                Optional keys: ``typeId``, ``referrerId``, ``title``,
                ``firstName``, ``lastName``, ``email``, ``gender``, ``lang``,
                ``plentyId``, ``options``.

        Returns:
            dict: The created contact (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        return await self._session.post("/rest/accounts/contacts", json=data)

    async def update(self, contact_id: int, data: ContactUpdatePayload) -> dict:
        """Update an existing contact.

        Args:
            contact_id: The numeric contact ID to update.
            data: Fields to update. Use ``ContactUpdatePayload`` for IDE autocomplete.
                Optional keys: ``title``, ``firstName``, ``lastName``,
                ``email``, ``gender``, ``lang``, ``options``.

        Returns:
            dict: The updated contact (same keys as ``get()``).

        Raises:
            NotFoundError: If the contact does not exist.
            AuthError: If authentication fails.
        """
        return await self._session.put(
            f"/rest/accounts/contacts/{contact_id}", json=data
        )

    async def paginate(self, **filters) -> AsyncGenerator[dict, None]:
        """Async generator that yields every contact matching ``filters``.

        Args:
            **filters: Same filter parameters as ``list()``.

        Yields:
            dict: Individual contact dict (same keys as ``get()``).

        Raises:
            AuthError: If authentication fails.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=250, **filters)
            for entry in result.get("entries", []):
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_contacts.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
uv run pytest -v
```

Expected: all tests PASS, no failures.

- [ ] **Step 6: Update CHANGELOG.md**

Append under `[Unreleased]`:

```markdown
## [Unreleased]

### feat

- **Session:** HTTP session with Bearer token auth, auto-login, near-expiry refresh, 401 re-login retry, and full error mapping
- **Client:** `PlentyClient` async context manager with lazy module properties (`orders`, `items`, `stock`, `contacts`)
- **Orders:** `OrdersModule` — get, list, create, update, paginate (`/rest/orders`)
- **Items:** `ItemsModule` — get, list, create, update, paginate (`/rest/items`)
- **Stock:** `StockModule` — get_by_warehouse, correct, paginate (`/rest/stockmanagement/warehouses/{id}/stock`)
- **Contacts:** `ContactsModule` — get, list, create, update, paginate (`/rest/accounts/contacts`)
- **Types:** `TypedDict` payload definitions for all core modules (`OrderCreatePayload`, `OrderUpdatePayload`, `ItemCreatePayload`, `ItemUpdatePayload`, `StockCorrectionPayload`, `ContactCreatePayload`, `ContactUpdatePayload`)
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/contacts.py tests/test_contacts.py CHANGELOG.md
git commit -m "feat: add ContactsModule (get, list, create, update, paginate)"
```
