# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.3.1] - 2026-07-13

### Pim

- refactor: split `PimModule` into a `modules/pim/` package (mixins per sub-resource group: variations, variation identifiers/taxonomy/commerce, attributes, attribute names, attribute values, categories, sales prices, barcodes, item serial numbers, lookups) — no public API change

## [0.3.0] - 2026-07-13

### Stock

- feat: `StockModule.list_stock` / `paginate_all_stock` — list/iterate stock levels across all warehouses via `GET /rest/stockmanagement/stock`
- feat: `StockModule.list_stock_archive_years` — list archive years of stock movements via `GET /rest/stockmanagement/stock/archives`
- feat: `StockModule.list_stock_by_type` / `paginate_stock_by_type` — list/iterate stock by warehouse type via `GET /rest/stockmanagement/stock/types/{type}`
- feat: `StockModule.redistribute_stock` — move stock between warehouses via `PUT /rest/stockmanagement/stock/redistribute`
- feat: `StockRedistributionPayload`, `VariationStockRedistributionPayload` — TypedDicts for `redistribute_stock`
- feat: `StockModule.list_warehouses` — list warehouses via `GET /rest/stockmanagement/warehouses`
- feat: `StockModule.create_warehouse` — create a warehouse via `POST /rest/stockmanagement/warehouses`
- feat: `StockModule.get_warehouse` — get one warehouse via `GET /rest/stockmanagement/warehouses/{warehouseId}`
- feat: `StockModule.get_storage_location` — get one storage location via `GET /rest/stockmanagement/warehouses/{warehouseId}/management/storageLocations/{storageLocationId}`
- feat: `WarehouseCreatePayload` — TypedDict for `create_warehouse`
- feat: `StockModule.book_incoming_items` — book incoming stock via `PUT /rest/stockmanagement/warehouses/{warehouseId}/stock/bookIncomingItems`
- feat: `StockModule.book_outgoing_items` — book outgoing stock via `PUT /rest/stockmanagement/warehouses/{warehouseId}/stock/bookOutgoingItems`
- feat: `StockModule.unpack_variation` — unpack a bundle/set variation via `PUT /rest/stockmanagement/warehouses/{warehouseId}/stock/unpackVariation`
- feat: `StockModule.book_stocktaking` — book a stocktaking correction via `PUT /rest/stockmanagement/warehouses/{warehouseId}/{warehouseLocationId}/stock/bookStocktaking`
- feat: `StockModule.list_stock_movements` / `paginate_stock_movements` — list/iterate stock movement history via `GET /rest/stockmanagement/warehouses/{warehouseId}/stock/movements`
- feat: `StockModule.list_stock_by_storage_location` / `paginate_stock_by_storage_location` — list/iterate stock per storage location via `GET /rest/stockmanagement/warehouses/{warehouseId}/stock/storageLocations`
- feat: `StockModule.list_stock_by_storage_location_pim` / `paginate_stock_by_storage_location_pim` — list/iterate stock per storage location with linked PIM entry via `GET /rest/stockmanagement/warehouses/{warehouseId}/stock/storageLocationsPim`
- feat: `StockIntakePayload`, `VariationStockIntakePayload`, `StockDischargePayload`, `VariationStockDischargePayload`, `UnpackVariationPayload` — TypedDicts for the stock booking endpoints
- `Stock` reaches full endpoint coverage (17/17) under the `StockManagement` API tag

### Order

- feat: `OrdersModule.delete` — delete an order via `DELETE /rest/orders/{orderId}`
- feat: `OrdersModule.cancel` — cancel an order via `PUT /rest/orders/{orderId}/cancel`
- feat: `OrdersModule.get_family` — get an order's family info via `GET /rest/orders/{orderId}/family`
- feat: `OrdersModule.get_my_account_url` — get an order's "My Account" URL via `GET /rest/orders/{orderId}/my_account_url`
- feat: `OrdersModule.search` / `paginate_search` — filterable order search (unlike `list`, which only paginates) via `GET`/`POST /rest/orders/search`
- feat: `OrdersModule.list_status_definitions` / `paginate_status_definitions` — search order status definitions via `GET /rest/orders/statuses`
- feat: `OrdersModule.list_all_status_definitions` — list every order status definition via `GET /rest/orders/statuses/all`
- feat: `OrdersModule.create_status_definition` — create an order status definition via `POST /rest/orders/statuses`
- feat: `OrdersModule.get_status_definition` — get one order status definition via `GET /rest/orders/statuses/{statusId}`
- feat: `OrdersModule.rename_status_definition` — update an order status definition's translated names via `PUT /rest/orders/statuses/{statusId}`
- feat: `OrdersModule.delete_status_definition` — delete an order status definition via `DELETE /rest/orders/statuses/{statusId}`
- feat: `OrdersModule.update_status_definition_properties` — bulk-update color/visibility properties across several order status definitions via `POST /rest/orders/statuses/group_functions`
- feat: `OrderStatusNamePayload` — TypedDict for `create_status_definition`/`rename_status_definition`
- feat: `OrdersModule.list_status_history` / `paginate_status_history` — search order status history via `GET /rest/orders/status-history`
- feat: `OrdersModule.get_order_status_history` — get a single order's status history via `GET /rest/orders/{orderId}/status-history`
- feat: `OrdersModule.list_date_types` — list order date types via `GET /rest/orders/dates/types`
- feat: `OrdersModule.get_date_type` — get one order date type via `GET /rest/orders/dates/types/{typeId}`
- feat: `OrdersModule.list_date_type_names` — list translated names of an order date type via `GET /rest/orders/dates/types/{typeId}/names`
- feat: `OrdersModule.get_date_type_name` — get one translated name of an order date type via `GET /rest/orders/dates/types/{typeId}/names/{lang}`
- feat: `OrdersModule.list_order_dates` — list all dates recorded on an order via `GET /rest/orders/{orderId}/dates`
- feat: `OrdersModule.get_order_date` — get a single date recorded on an order via `GET /rest/orders/{orderId}/dates/{typeId}`
- feat: `OrdersModule.search_item_transactions` / `paginate_item_transactions` — search order item transactions via `GET /rest/orders/items/transactions`
- feat: `OrdersModule.update_item_transaction` — update an order item transaction via `PUT /rest/orders/items/transactions/{transactionId}`
- feat: `OrdersModule.delete_item_transaction` — delete an order item transaction via `DELETE /rest/orders/items/transactions/{transactionId}`
- feat: `OrdersModule.book_item_transactions` — bulk-book order item transactions by ID via `POST /rest/orders/items/transactions/booking`
- feat: `OrdersModule.list_item_transactions` — list transactions of a single order item via `GET /rest/orders/items/{orderItemId}/transactions`
- feat: `OrdersModule.create_item_transaction` — create a transaction for an order item via `POST /rest/orders/items/{orderItemId}/transactions`
- feat: `OrderItemTransactionCreatePayload` — TypedDict for `create_item_transaction`
- feat: `OrdersModule.book_item_in` — book a single order item's full quantity in via `POST /rest/orders/items/{orderItemId}/booking`
- feat: `OrdersModule.list_order_items` / `paginate_order_items` — list an order's items via `GET /rest/orders/{orderId}/items`
- feat: `OrdersModule.delete_order_item` — delete an order item via `DELETE /rest/orders/{orderId}/items/{orderItemId}`
- feat: `OrdersModule.list_order_serial_numbers` — list all serial numbers on an order via `GET /rest/orders/{orderId}/items/serialNumbers`
- feat: `OrdersModule.list_order_item_serial_numbers` — list serial numbers of a single order item via `GET /rest/orders/{orderId}/items/{orderItemId}/serialNumbers`
- feat: `OrdersModule.create_order_item_serial_number` — create and bind a serial number to an order item via `POST /rest/orders/{orderId}/items/{orderItemId}/serialNumbers`
- feat: `OrdersModule.list_order_package_numbers` — list an order's package numbers via `GET /rest/orders/{orderId}/packagenumbers`
- feat: `OrdersModule.attach_order_item_warehouse_locations` — attach warehouse locations to order items via `POST /rest/orders/{orderId}/items/warehouse_locations/attach`
- feat: `OrdersModule.detach_order_item_warehouse_locations` — detach warehouse locations from order items via `POST /rest/orders/{orderId}/items/warehouse_locations/detach`
- feat: `OrdersModule.generate_order_item_reorders` — generate reorder(s) for an order's items via `POST /rest/orders/{orderId}/items/reorders/generate`
- feat: `OrdersModule.create_order_reorder` — create a reorder from a parent order via `POST /rest/orders/{orderId}/reorders`
- feat: `OrdersModule.generate_order_reorders` — generate reorder(s) for an order via `POST /rest/orders/{orderId}/reorders/generate`
- feat: `OrdersModule.validate_order_reorders` — validate an order's items before creating a reorder via `POST /rest/orders/{orderId}/reorders/generate/validate`
- feat: `OrdersModule.create_order_transactions` — bulk-create item transactions for an order's items via `POST /rest/orders/{orderId}/transactions`
- feat: `OrderTransactionsCreatePayload` — TypedDict for `create_order_transactions`
- `Order` reaches 45/307 endpoint coverage under the `Order` API tag (order item transactions, items, serial numbers, warehouse locations & reorders milestone)
- refactor: split `OrdersModule` into a `modules/orders/` package (mixins per sub-resource group: core, statuses, status history, dates, transactions, order items, reorders) — no public API change


## [0.2.1] - 2026-07-01

### Stock

- fix: `StockModule.get_by_warehouse` — corrected stale endpoint `GET /rest/stock/warehouses/{warehouseId}/items` (no longer exists in the API) to `GET /rest/stockmanagement/warehouses/{warehouseId}/stock`; response entry fields updated to match the current `Stock` schema (e.g. `netStock`/`physicalStock` → `stockNet`/`stockPhysical`)
- fix: `StockModule.correct` — corrected stale endpoint `PUT /rest/stock/warehouses/{warehouseId}/stock/correction` (no longer exists in the API) to `PUT /rest/stockmanagement/warehouses/{warehouseId}/stock/correction`
- fix: `StockCorrectionPayload` — only `quantity` is actually required by the API; `warehouseLocationId` renamed to `storageLocationId`; added optional `reasonId`, `batch`, `bestBeforeDate`, and bulk `corrections` keys to match the live schema
- feat: `VariationStockCorrectionPayload` — TypedDict for entries in `StockCorrectionPayload.corrections`, for bulk stock correction across several variations in one request

## [0.2.0] - 2026-07-01

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
- feat: `PimModule.list_attribute_names` — search attribute names via `GET /rest/pim/attributes/names`
- feat: `PimModule.create_attribute_names` — bulk create attribute names via `POST /rest/pim/attributes/names`
- feat: `PimModule.update_attribute_names` — bulk update attribute names via `PUT /rest/pim/attributes/names`
- feat: `PimModule.delete_attribute_names` — bulk delete attribute names via `DELETE /rest/pim/attributes/names`
- feat: `PimModule.list_attribute_values` — search attribute values via `GET /rest/pim/attributes/values`
- feat: `PimModule.create_attribute_values` — bulk create attribute values via `POST /rest/pim/attributes/values`
- feat: `PimModule.update_attribute_values` — bulk update attribute values via `PUT /rest/pim/attributes/values`
- feat: `PimModule.delete_attribute_values` — bulk delete attribute values via `DELETE /rest/pim/attributes/values`
- feat: `PimModule.get_attribute_value` — get one attribute value via `GET /rest/pim/attributes/values/{id}`
- feat: `PimModule.list_attribute_value_names` — search attribute value names via `GET /rest/pim/attributes/values/names`
- feat: `PimModule.create_attribute_value_names` — bulk create attribute value names via `POST /rest/pim/attributes/values/names`
- feat: `PimModule.update_attribute_value_names` — bulk update attribute value names via `PUT /rest/pim/attributes/values/names`
- feat: `PimModule.delete_attribute_value_names` — bulk delete attribute value names via `DELETE /rest/pim/attributes/values/names`
- feat: `PimModule.list_sales_prices` — search sales prices via `GET /rest/pim/sales_prices`
- feat: `PimModule.get_sales_price` — get one sales price via `GET /rest/pim/sales_prices/{id}`
- feat: `PimModule.create_sales_prices` — bulk create sales price configurations via `POST /rest/pim/sales_prices`
- feat: `PimModule.update_sales_prices` — bulk update sales price configurations via `PUT /rest/pim/sales_prices`
- feat: `PimModule.delete_sales_prices` — bulk delete sales price configurations via `DELETE /rest/pim/sales_prices`
- feat: `PimModule.list_barcodes` — search barcode configurations via `GET /rest/pim/barcodes`
- feat: `PimModule.create_barcodes` — bulk create barcode configurations via `POST /rest/pim/barcodes`
- feat: `PimModule.update_barcodes` — bulk update barcode configurations via `PUT /rest/pim/barcodes`
- feat: `PimModule.delete_barcodes` — bulk delete barcode configurations via `DELETE /rest/pim/barcodes`
- feat: `PimModule.list_barcode_duplicates` — list duplicate barcodes via `GET /rest/pim/barcodes/duplicates`
- feat: `PimModule.count_barcode_duplicates` — count duplicate barcodes via `GET /rest/pim/barcodes/duplicates/count`
- feat: `PimModule.get_barcode_duplicate_settings` — get duplicate-detection settings via `GET /rest/pim/barcodes/duplicates/settings`
- feat: `PimModule.list_category_branches` — search category branches via `GET /rest/pim/categories/branches`
- feat: `PimModule.list_category_clients` — search category client visibility via `GET /rest/pim/categories/clients`
- feat: `PimModule.list_category_details` — search category detail records via `GET /rest/pim/categories/details`
- feat: `PimModule.list_category_properties` — search category property links via `GET /rest/pim/categories/properties`
- feat: `PimModule.list_item_serial_numbers` — search item serial numbers via `GET /rest/pim/item-serial-numbers`
- feat: `PimModule.create_item_serial_numbers` — bulk create item serial numbers via `POST /rest/pim/item-serial-numbers`
- feat: `PimModule.update_item_serial_numbers` — bulk update item serial numbers via `PUT /rest/pim/item-serial-numbers`
- feat: `PimModule.delete_item_serial_numbers` — bulk delete item serial numbers via `DELETE /rest/pim/item-serial-numbers`
- feat: `PimModule.get_item_attributes` — get attributes linked to an item via `GET /rest/pim/items/{id}/attributes`
- feat: `PimModule.get_item_combinations` — get valid variation combinations for an item via `GET /rest/pim/items/{id}/combinations`
- feat: `PimModule.list_amazon_product_types` — list Amazon product types via `GET /rest/pim/amazon-product-types`

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
