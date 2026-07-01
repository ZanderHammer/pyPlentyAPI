# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Pim

- feat: `PimModule.list_variations` — search and filter variations via `GET /rest/pim/variations`
- feat: `PimModule.paginate_variations` — cursor-based async iterator via `GET /rest/pim/variations/scroll`
- feat: `PimModule.update_variation_bases` — bulk variation update via `PUT /rest/pim/variations/bases`
- feat: `PimModule.create_variations` — bulk create/update variations via `PUT /rest/pim/variations`
- feat: `PimModule.delete_variations` — bulk delete variations via `DELETE /rest/pim/variations`
- feat: `PimModule.update_variation_additional_skus` / `delete_variation_additional_skus` — `/rest/pim/variations/additional_skus`
- feat: `PimModule.update_variation_barcodes` / `delete_variation_barcodes` — `/rest/pim/variations/barcodes`
- feat: `PimModule.update_variation_bundle_components` / `delete_variation_bundle_components` — `/rest/pim/variations/bundle_components`
- feat: `PimModule.update_variation_categories` / `delete_variation_categories` — `/rest/pim/variations/categories`
- feat: `PimModule.update_variation_clients` / `delete_variation_clients` — `/rest/pim/variations/clients`
- feat: `PimModule.update_variation_comments` / `delete_variation_comments` — `/rest/pim/variations/comments`
- feat: `PimModule.update_variation_default_categories` / `delete_variation_default_categories` — `/rest/pim/variations/default_categories`
- feat: `PimModule.update_variation_images` / `delete_variation_images` — `/rest/pim/variations/images`
- feat: `PimModule.update_variation_market_ident_numbers` / `delete_variation_market_ident_numbers` — `/rest/pim/variations/market_ident_numbers`
- feat: `PimModule.update_variation_markets` / `delete_variation_markets` — `/rest/pim/variations/markets`
- feat: `PimModule.update_variation_properties` / `delete_variation_properties` — `/rest/pim/variations/properties`
- feat: `PimModule.update_variation_sales_prices` / `delete_variation_sales_prices` — `/rest/pim/variations/sales_prices`
- feat: `PimModule.update_variation_skus` / `delete_variation_skus` — `/rest/pim/variations/skus`
- feat: `PimModule.update_variation_supplier` / `delete_variation_supplier` — `/rest/pim/variations/supplier`
- feat: `PimModule.update_variation_tags` / `delete_variation_tags` — `/rest/pim/variations/tags`
- feat: `PimModule.update_variation_warehouses` / `delete_variation_warehouses` — `/rest/pim/variations/warehouses`
- feat: `PimModule.list_categories` — search categories via `GET /rest/pim/categories`
- feat: `PimModule.get_category` — get one category via `GET /rest/pim/categories/{id}`
- feat: `PimModule.list_attributes` — search attributes via `GET /rest/pim/attributes`
- feat: `PimModule.get_attribute` — get one attribute via `GET /rest/pim/attributes/{id}`
- feat: `PimModule.create_attributes` — bulk create attributes via `POST /rest/pim/attributes`
- feat: `PimModule.update_attributes` — bulk update attributes via `PUT /rest/pim/attributes`
- feat: `PimModule.delete_attributes` — bulk delete attributes via `DELETE /rest/pim/attributes`
- feat: `PimModule.list_sales_prices` — search sales prices via `GET /rest/pim/sales_prices`
- feat: `PimModule.get_sales_price` — get one sales price via `GET /rest/pim/sales_prices/{id}`

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
