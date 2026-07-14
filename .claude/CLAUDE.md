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
- **Internal class naming:** files like `_session.py`/`_types.py`/`_exceptions.py` keep a leading underscore (signals "not part of the public API" to humans), but the *classes* they define (`Session`, exception types, etc.) do not — only `plentymarkets/__init__.py`'s `__all__` decides what's public. A leading underscore on a class name (e.g. the old `_Session`) makes Pylance's `reportPrivateUsage` flag every legitimate cross-file import within the package (`client.py`, every `modules/*.py`), which is not useful noise here.
- **Deprecated endpoints are never implemented.** PlentyMarkets marks some endpoints deprecated in the OpenAPI spec's `description` field (`<b>DEPRECATED: Use the following route: ...</b>`) even though they're still live and tagged like any other endpoint. Do not add client methods for these, no matter how the endpoint-coverage tracking is framed ("full coverage," "matches every tagged endpoint," etc.) — a deprecated endpoint is out of scope, not a gap to fill. When surveying an API tag for what to implement next, first check each candidate endpoint's `description` for the deprecation marker and skip it.
  - In `ROADMAP.md`, list a deprecated endpoint's Status as `deprecated (use <replacement route>)` with Code `—` — the same as `planned`, but permanently, not as a queued task. Never flip it to `**implemented**`.
  - In `CHANGELOG.md`, never add a `feat:` line for a deprecated endpoint.
  - If an already-implemented method is later discovered to wrap a deprecated endpoint, remove it (method, tests, TypedDict if unused elsewhere) in a `fix:` or `refactor:` commit rather than leaving it in place.

## Package structure
```
src/plentymarkets/
  __init__.py        # exports PlentyClient + all TypedDicts
  client.py          # PlentyClient
  _session.py        # HTTP session, auth lifecycle
  _exceptions.py     # exception hierarchy
  _types.py          # TypedDict payload definitions for all write operations
  modules/
    orders/           # OrdersModule  → /rest/orders (package: see "Splitting a large module" below)
    pim/              # PimModule     → /rest/pim (package: see "Splitting a large module" below)
    items.py         # ItemsModule   → /rest/items
    stock.py         # StockModule   → /rest/stock
    contacts.py      # ContactsModule → /rest/accounts/contacts
```

## Splitting a large module into a package

When a `modules/<name>.py` file exceeds ~500 lines or covers 5+ distinct
sub-resource groups (e.g. `orders.py`, `pim.py`), convert it to a package
`modules/<name>/` instead of leaving it flat. **Public API stays 100% flat**
— `<Name>Module` still exposes every method directly; only the internals
split, via mixins:

- `__init__.py` — composes `<Name>Module` from all mixins + `<Name>Base`,
  via multiple inheritance. Defines only `__init__`/`__repr__`. This is the
  only file client.py's `from .modules.<name> import <Name>Module` needs.
- `_base.py` — `<Name>Base` class: shared `_session: Session` annotation
  (no `__init__`) + shared helpers (e.g. `_build_params`).
- One file per sub-resource group, each a `<Group>Mixin(<Name>Base)` with
  only that group's `async def` methods, moved verbatim (docstrings unchanged).
  Mixin/base class names do **not** get a leading underscore even though
  they're internal — Pylance's `reportPrivateUsage` flags underscore-prefixed
  names imported across sibling files (it treats each file in the package as
  its own "module"). `__all__ = ["<Name>Module"]` in `__init__.py` already
  keeps them out of `import *`, which is all the privacy signal needed here.

**Import-dot gotcha**: files living directly under `modules/<name>.py` used
2-dot relative imports (`from .._session import ...`). Files inside the new
`modules/<name>/` package are one level deeper and need **3 dots**
(`from ..._session import ...`, `from ..._types import ...`). Sibling
imports within the package use 1 dot (`from ._base import <Name>Base`).
Getting this wrong is a silent `ImportError` only caught at test time — no
ruff/mypy import-order check exists in this repo to catch it.

Split the matching test file the same way: one `tests/test_<name>_<group>.py`
per source group, each with its own copy of the `session`/`<name>` fixtures
(this repo's convention — no shared conftest fixtures).

## TypedDicts
`_types.py` holds `TypedDict` definitions for every method that accepts a `data` dict.
Import them for IDE autocomplete and static type checking — at runtime they are plain dicts.

| TypedDict | Used by |
|---|---|
| `OrderCreatePayload` | `client.orders.create(data)` |
| `ItemCreatePayload` | `client.items.create(data)` |
| `ItemUpdatePayload` | `client.items.update(item_id, data)` |
| `StockCorrectionPayload` | `client.stock.correct(warehouse_id, data)` |
| `ContactCreatePayload` | `client.contacts.create(data)` |
| `ContactUpdatePayload` | `client.contacts.update(contact_id, data)` |

All six are exported from `plentymarkets` directly:
```python
from plentymarkets import OrderCreatePayload, PlentyClient
```

When adding a new module method that accepts a payload dict, add a matching TypedDict
to `_types.py` and export it from `__init__.py`.

## Auth
POST /rest/login with username+password → accessToken + expiresIn (seconds).
Token sent as `Authorization: Bearer <token>` on every request.
Auto-refreshed when within 60 s of expiry. 401 mid-session → re-login once → retry.
```
```
