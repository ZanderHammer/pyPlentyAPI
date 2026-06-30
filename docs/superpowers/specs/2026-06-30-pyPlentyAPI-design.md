# pyPlentyAPI — Design Spec

**Date:** 2026-06-30
**Status:** Approved

## Overview

A Python package (`plentymarkets`) that wraps the PlentyMarkets REST API. Async-only, built on
`httpx`. Provides namespaced module accessors on a single `PlentyClient` entry point. Covers the
four core modules first (Items, Orders, Stock, Contacts); additional modules added incrementally.

## Scope

- **In scope:** PlentyMarkets REST API only. NOT PlentyBase.
- **Out of scope:** Webhooks, file uploads, any non-REST PlentyMarkets interface.

## Project Tooling

| Tool | Purpose |
|---|---|
| UV | Python version + dependency management |
| pre-commit + commitizen | Enforce conventional commits |
| pytest + pytest-httpx | Unit tests with mocked HTTP layer |
| CHANGELOG.md | "Keep a Changelog" format, unreleased section only |
| Google-style docstrings | Mandatory on all public APIs; must document every response key |

## Package Structure

```
pyPlentyAPI/
├── src/
│   └── plentymarkets/
│       ├── __init__.py          # exports PlentyClient
│       ├── client.py            # PlentyClient + module properties
│       ├── _session.py          # HTTP session, login/refresh/logout
│       ├── _exceptions.py       # exception hierarchy
│       └── modules/
│           ├── orders.py
│           ├── items.py
│           ├── stock.py
│           └── contacts.py
├── tests/
│   ├── conftest.py
│   ├── test_session.py
│   ├── test_orders.py
│   ├── test_items.py
│   ├── test_stock.py
│   └── test_contacts.py
├── docs/
│   └── superpowers/specs/
├── pyproject.toml
├── CHANGELOG.md
├── CLAUDE.md
└── .pre-commit-config.yaml
```

## Authentication & Session Lifecycle

PlentyMarkets uses a login-based session: `POST /rest/login` with username + password returns an
access token (Bearer) and `expiresIn` (seconds). The session stores `login_time + expires_in` as
the absolute expiry and compares against the current time before each request. The token must be
sent on every subsequent request.

**Auto-managed with explicit control (Option C):**
- On first request (or `async with` entry), the client logs in automatically.
- Before every request: if the token is within 60 seconds of expiry, refresh it first.
- If a 401 is received mid-session: re-login once, retry the request. If still 401 → `AuthError`.
- User may also call `await client.login()` / `await client.logout()` explicitly.
- `await client.aclose()` must be called when not using the context manager.

```python
# Context manager (recommended)
async with PlentyClient(
    base_url="https://your-shop.plentymarkets.com",
    username="user@example.com",
    password="secret",
) as client:
    order = await client.orders.get(42)

# Manual control
client = PlentyClient(...)
await client.login()
order = await client.orders.get(42)
await client.logout()
await client.aclose()
```

## Architecture & Data Flow

`PlentyClient` owns a single `_Session` instance and exposes module accessors as lazily-instantiated
properties (`client.orders`, `client.items`, `client.stock`, `client.contacts`). Each module holds a
reference to the shared `_Session` and calls it directly.

```
client.orders.get(42)
  └─► OrdersModule._session.get("/rest/orders/42")
        └─► _Session._request()
              ├─ inject Authorization: Bearer <token>
              ├─ if token near expiry → refresh → continue
              └─► httpx.AsyncClient.request()
                    └─► PlentyMarkets REST API
                          └─► dict returned up the chain
```

**Pagination:** list methods accept `page: int` and `items_per_page: int`. Each module also exposes
a `paginate_*()` async generator that yields individual items (not pages) across all pages
automatically until the API returns an empty page.

## Error Handling

All exceptions inherit from `PlentyError`:

```
PlentyError
├── AuthError          — 401; login failure or invalid/expired token
├── NotFoundError      — 404
├── RateLimitError     — 429; exposes .retry_after (int seconds, if header present)
├── ServerError        — 5xx
└── ConnectionError    — network unreachable, DNS failure, timeout
```

No automatic retries in the library. `RateLimitError.retry_after` gives callers the information
needed to implement their own backoff strategy.

## Testing Strategy

**Unit tests** (`pytest` + `pytest-httpx`): mock `httpx` at the transport level. Tests exercise
the real auth logic, error handling, and request formation — no live server required.

Test coverage targets:
- Auth flow: login, token injection, near-expiry refresh, 401 re-login, logout
- Error mapping: each HTTP status → correct exception type
- Request formation: correct URL, method, headers, query params per module method
- Pagination: `paginate_*()` generators yield correct pages and stop at last page

**Integration tests** (`@pytest.mark.integration`): skipped by default; require real credentials
set via environment variables. Run manually with `pytest -m integration`.

## Core Modules — Initial Scope

> Note: PlentyMarkets uses the tag `Account` for customer/contact management.
> Contacts are accessed via `/rest/accounts/contacts`, not a `/contacts` root.

| API Tag | Python module | Key endpoints |
|---|---|---|
| `Order` | `client.orders` | get, list, create, update status, paginate |
| `Item` | `client.items` | get, list, create, update, paginate |
| `Stock` | `client.stock` | get by warehouse, correct stock, paginate |
| `Account` | `client.contacts` | get contact, list contacts, create, update, paginate |

Additional endpoints within each module are added incrementally as needed.

## Full API Module Overview

See [ROADMAP.md](../../../ROADMAP.md) for the complete list of all 53 PlentyMarkets REST API
modules with descriptions and implementation status.

## Conventions

- Conventional commits enforced via pre-commit + commitizen
- Small, focused commits (one logical change per commit)
- Google-style docstrings on all public methods; response dict keys fully documented
- `CHANGELOG.md` follows "Keep a Changelog"; only the `[Unreleased]` section is ever written to
  (releases are tagged manually by the maintainer)
