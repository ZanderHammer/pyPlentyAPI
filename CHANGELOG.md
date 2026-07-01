# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Pim

- feat: `PimModule.list_variations` — search and filter variations via `GET /rest/pim/variations`
- feat: `PimModule.paginate_variations` — cursor-based async iterator via `GET /rest/pim/variations/scroll`
- feat: `PimModule.update_variation_bases` — bulk variation update via `PUT /rest/pim/variations/bases`

## [0.1.2] - 2026-06-30

### Changed
- `pyproject`: rename PyPI distribution from `plentymarkets` to `plentymarkets-api-client` — the import package stays `plentymarkets` (`from plentymarkets import PlentyClient`)
- `pyproject`: add full PyPI metadata — `readme`, `license`, `authors`, `keywords`, `classifiers`, `project.urls` (Homepage, Repository, Issues, Changelog)

### Added
- `plentymarkets`: PEP 561 `py.typed` marker so downstream type checkers pick up the package's type hints

## [0.1.1] - 2026-06-30

### CI
- `release`: publish built distributions to PyPI via `uv publish` after the Codeberg release build ([`c450759`](https://codeberg.org/ZanderHammer/pyPlentyAPI/commit/c450759))
- `release`: use the matching `CHANGELOG.md` `## [VERSION]` section as the Codeberg release body instead of a generic link ([`07730aa`](https://codeberg.org/ZanderHammer/pyPlentyAPI/commit/07730aa))

### Chore
- `commitizen`: add `scripts/bump_changelog.py` as a `pre_bump_hook` to version the `[Unreleased]` section into `## [VERSION] - DATE` automatically on `cz bump` ([`bc4728c`](https://codeberg.org/ZanderHammer/pyPlentyAPI/commit/bc4728c))

## [0.1.0] - 2026-06-30

### Added
- Exception hierarchy: `PlentyError`, `AuthError`, `NotFoundError`, `RateLimitError`, `ServerError`, `ConnectionError`
- `_Session`: async HTTP client with login, token auto-refresh, 401 re-login, and error mapping
- `PlentyClient`: async context manager with lazy `orders`, `items`, `stock`, `contacts` module properties
- `OrdersModule`: `get`, `list`, `create`, `update_status`, `paginate_orders` (`/rest/orders`)
- `ItemsModule`: `get`, `list`, `create`, `update`, `paginate_items` (`/rest/items`)
- `StockModule`: `get_by_warehouse`, `correct`, `paginate_stock` (`/rest/stock/warehouses`)
- `ContactsModule`: `get`, `list`, `create`, `update`, `paginate_contacts` (`/rest/accounts/contacts`)
- `_types`: `TypedDict` payload definitions for all write operations — `OrderCreatePayload`, `ItemCreatePayload`, `ItemUpdatePayload`, `StockCorrectionPayload`, `ContactCreatePayload`, `ContactUpdatePayload`; all exported from `plentymarkets` top-level
- `PlentyClient`, `OrdersModule`, `ItemsModule`, `StockModule`, `ContactsModule`: `__repr__` for readable debug output ([`5ad0e94`](https://codeberg.org/ZanderHammer/pyPlentyAPI/commit/5ad0e94))

### Fixed
- `_session`: raise `ValueError` when `base_url` contains `/rest`, preventing a silent `JSONDecodeError` from doubled path segments ([`731ff44`](https://codeberg.org/ZanderHammer/pyPlentyAPI/commit/731ff44))
- All modules, `_session`: replace bare `dict` return annotations with `dict[str, Any]`, resolving `Unknown` type hints in Pylance ([`a47534d`](https://codeberg.org/ZanderHammer/pyPlentyAPI/commit/a47534d))
