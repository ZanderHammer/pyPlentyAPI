# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Exception hierarchy: `PlentyError`, `AuthError`, `NotFoundError`, `RateLimitError`, `ServerError`, `ConnectionError`
- `_Session`: async HTTP client with login, token auto-refresh, 401 re-login, and error mapping
- `PlentyClient`: async context manager with lazy `orders`, `items`, `stock`, `contacts` module properties
- `OrdersModule`: `get`, `list`, `create`, `update_status`, `paginate_orders` (`/rest/orders`)
- `ItemsModule`: `get`, `list`, `create`, `update`, `paginate_items` (`/rest/items`)
- `StockModule`: `get_by_warehouse`, `correct`, `paginate_stock` (`/rest/stock/warehouses`)
- `ContactsModule`: `get`, `list`, `create`, `update`, `paginate_contacts` (`/rest/accounts/contacts`)
- `_types`: `TypedDict` payload definitions for all write operations — `OrderCreatePayload`, `ItemCreatePayload`, `ItemUpdatePayload`, `StockCorrectionPayload`, `ContactCreatePayload`, `ContactUpdatePayload`; all exported from `plentymarkets` top-level
- `PlentyClient`, `OrdersModule`, `ItemsModule`, `StockModule`, `ContactsModule`: `__repr__` for readable debug output ([`5ad0e94`](https://github.com/anomalyco/pyPlentyAPI/commit/5ad0e94))

### Fixed
- `_session`: raise `ValueError` when `base_url` contains `/rest`, preventing a silent `JSONDecodeError` from doubled path segments ([`731ff44`](https://github.com/anomalyco/pyPlentyAPI/commit/731ff44))
- All modules, `_session`: replace bare `dict` return annotations with `dict[str, Any]`, resolving `Unknown` type hints in Pylance ([`a47534d`](https://github.com/anomalyco/pyPlentyAPI/commit/a47534d))
