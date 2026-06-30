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
  __init__.py        # exports PlentyClient + all TypedDicts
  client.py          # PlentyClient
  _session.py        # HTTP session, auth lifecycle
  _exceptions.py     # exception hierarchy
  _types.py          # TypedDict payload definitions for all write operations
  modules/
    orders.py        # OrdersModule  → /rest/orders
    items.py         # ItemsModule   → /rest/items
    stock.py         # StockModule   → /rest/stock
    contacts.py      # ContactsModule → /rest/accounts/contacts
```

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
