# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `PlentyClient` async context manager with auto-managed token lifecycle
- `_Session` with login, logout, auto-refresh, and 401 re-login
- Exception hierarchy: `PlentyError`, `AuthError`, `NotFoundError`, `RateLimitError`, `ServerError`, `ConnectionError`
- `OrdersModule`: get, list, create, update_status, paginate_orders
- `ItemsModule`: get, list, create, update, paginate_items
- `StockModule`: get_by_warehouse, correct, paginate_stock
- `ContactsModule`: get, list, create, update, paginate_contacts
