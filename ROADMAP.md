# Roadmap

All 53 modules available in the PlentyMarkets REST API. Modules marked **[core]** are in the
initial implementation scope. All others are planned for future incremental additions.

| API Tag | Description | Status |
|---|---|---|
| `Account` | Customer accounts and contacts — addresses, contact data, bank details | **[core]** |
| `Accounting` | VAT configurations, financial accounts, revenue bookings | planned |
| `AddressDesign` | Address label templates and print format settings | planned |
| `AuditLog` | Change history and audit trail for system actions | planned |
| `Authentication` | Login/logout and token management | internal (used by `_session.py`) |
| `Authorization` | User roles, permissions, and access rights | planned |
| `BI` | Business intelligence — reports and analytics data | planned |
| `Basket` | Shopping cart / basket management for webshop visitors | planned |
| `Batch` | Batch processing and bulk operations across resources | planned |
| `Blog` | Blog posts and categories published in the webshop | planned |
| `Board` | Task boards (Kanban-style) for internal team workflows | planned |
| `Boards` | Board management — creating and configuring boards | planned |
| `Catalog` | Data catalogues for flexible export/import field mappings | planned |
| `Category` | Product and content categories used in webshop and items | planned |
| `Cloud` | Cloud storage and file management | planned |
| `Comment` | Comments attachable to orders, contacts, and tickets | planned |
| `Configuration` | System-wide settings and global configuration values | planned |
| `Document` | Order documents — invoices, delivery notes, return slips | planned |
| `ElasticSync` | Data import/sync mappings (Data Exchange / ElasticSync) | planned |
| `Export` | Data export formats, fields, and export jobs | planned |
| `ExportSettings` | Settings and saved configurations for exports | planned |
| `Feedback` | Customer product reviews and ratings | planned |
| `Fulfillment` | Shipping labels, package tracking, shipping service providers | planned |
| `Item` | Product catalogue — items, variations, images, attributes, prices | **[core]** |
| `LegalInformation` | Legal texts — terms of service, privacy policy, cancellation rights | planned |
| `Listing` | eBay/marketplace listing templates and active listings | planned |
| `Log` | System log entries and error/debug logs | planned |
| `MailTemplates` | Email templates for automated system notifications | planned |
| `Market` | Marketplace integrations — Amazon, eBay, Otto, etc. | planned |
| `Messenger` | Internal messaging between system users | planned |
| `Newsletter` | Newsletter recipient lists and subscription management | planned |
| `Order` | Orders, order items, order properties, and status management | **[core]** |
| `OrderSummary` | Aggregated order statistics and revenue summaries | planned |
| `Payment` | Payments, payment methods, and booking payments to orders | planned |
| `Pim` | Product Information Management — PIM-specific item operations | planned — [endpoints documented](#pim--restpim) |
| `PluginMultilingualism` | Plugin translation strings and multilingual content | planned |
| `PluginSet` | Plugin set management and deployment to clients | planned |
| `Plugins` | Plugin installation, configuration, and lifecycle | planned |
| `Property` | Item and contact properties — property groups and values | planned |
| `Returns` | Return orders, return reasons, and return processing | planned |
| `ShopBuilder` | Webshop layout and drag-and-drop page builder configuration | planned |
| `Stock` | Item stock levels, stock movements, and manual corrections | **[core]** |
| `StockManagement` | Warehouse-level stock redistribution and incoming goods | planned |
| `Sync` | Data synchronisation jobs and field mapping configuration | planned |
| `Tag` | Tags for labelling orders, contacts, variations, etc. | planned |
| `Ticket` | Support tickets and helpdesk case management | planned |
| `TicketMessage` | Messages and replies within support tickets | planned |
| `Todo` | Internal to-do tasks and user assignments | planned |
| `User` | System users, user accounts, and preferences | planned |
| `Warehouse` | Warehouse configuration, storage locations, rack management | planned |
| `Webstore` | Webshop settings, themes, plugins, and client configuration | planned |
| `Wizard` | Setup wizards for guided first-time configuration | planned |
| `plentyMarketplace` | plentyMarkets plugin marketplace integration | planned |

---

## Planned Endpoint Details

Endpoints discovered from the OpenAPI spec, grouped by module. Updated as each module is researched.

### `Pim` — `/rest/pim/`

#### Variations

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/variations` | GET, PUT, DELETE (all **implemented**) | List/filter variations (70+ filter params, `with` for eager-loading includes); bulk update and delete | **implemented** |
| `/rest/pim/variations/scroll` | GET | Cursor-based scroll through all variations; use for full-catalogue iteration | **implemented** |
| `/rest/pim/variations/bases` | PUT | Bulk create/update variation base data | **implemented** |
| `/rest/pim/variations/additional_skus` | PUT, DELETE | Bulk create/update/delete variation additional SKUs | **implemented** |
| `/rest/pim/variations/barcodes` | PUT, DELETE | Bulk create/update/delete variation barcodes | **implemented** |
| `/rest/pim/variations/bundle_components` | PUT, DELETE | Bulk create/update/delete bundle components on variations | **implemented** |
| `/rest/pim/variations/categories` | PUT, DELETE | Bulk create/update/delete category links on variations | **implemented** |
| `/rest/pim/variations/clients` | PUT, DELETE | Bulk create/delete client (store) visibility on variations | **implemented** |
| `/rest/pim/variations/comments` | PUT, DELETE | Bulk create/update/delete variation comments | **implemented** |
| `/rest/pim/variations/default_categories` | PUT, DELETE | Bulk create/update/delete default category per client on variations | **implemented** |
| `/rest/pim/variations/images` | PUT, DELETE | Bulk create/delete image links on variations | **implemented** |
| `/rest/pim/variations/market_ident_numbers` | PUT, DELETE | Bulk create/update/delete market identifier numbers (MINs) | **implemented** |
| `/rest/pim/variations/markets` | PUT, DELETE | Bulk create/delete market availability on variations | **implemented** |
| `/rest/pim/variations/properties` | PUT, DELETE | Bulk create/update/delete variation properties | **implemented** |
| `/rest/pim/variations/sales_prices` | PUT, DELETE | Bulk create/update/delete sales price links on variations | **implemented** |
| `/rest/pim/variations/skus` | PUT, DELETE | Bulk create/update/delete SKUs on variations | **implemented** |
| `/rest/pim/variations/supplier` | PUT, DELETE | Bulk create/update/delete supplier links on variations | **implemented** |
| `/rest/pim/variations/tags` | PUT, DELETE | Bulk create/delete tags on variations | **implemented** |
| `/rest/pim/variations/warehouses` | PUT, DELETE | Bulk create/update/delete warehouse stock links on variations | **implemented** |

#### Attributes

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/attributes` | GET, PUT, POST, DELETE (all **implemented**) | Search, create, update, and delete attributes (defines variation axes like colour, size) | **implemented** |
| `/rest/pim/attributes/{id}` | GET | Get one attribute by ID | **implemented** |
| `/rest/pim/attributes/names` | GET, PUT, POST, DELETE (all **implemented**) | Manage multilingual attribute display names | **implemented** |
| `/rest/pim/attributes/values` | GET, PUT, POST, DELETE (all **implemented**) | Manage attribute values (e.g. "Red", "Blue" for a colour attribute) | **implemented** |
| `/rest/pim/attributes/values/{id}` | GET | Get one attribute value by ID | **implemented** |
| `/rest/pim/attributes/values/names` | GET, PUT, POST, DELETE (all **implemented**) | Manage multilingual display names for attribute values | **implemented** |

#### Categories

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/categories` | GET | Search categories (filter by ID, type, level, name) | **implemented** |
| `/rest/pim/categories/{id}` | GET | Get one category by ID | **implemented** |
| `/rest/pim/categories/branches` | GET | Search category branches (full path from root to leaf) | planned |
| `/rest/pim/categories/clients` | GET | Search which clients (stores) have each category active | planned |
| `/rest/pim/categories/details` | GET | Search category detail records (multilingual names, descriptions, meta data) | planned |
| `/rest/pim/categories/properties` | GET | Search category property links | planned |

#### Sales Prices

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/sales_prices` | GET, PUT, POST, DELETE | Search, create, update, and delete sales price configurations | partial |
| `/rest/pim/sales_prices/{id}` | GET | Get one sales price configuration by ID | **implemented** |

#### Barcodes

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/barcodes` | GET, PUT, POST, DELETE | Search, create, update, and delete barcode type configurations | planned |
| `/rest/pim/barcodes/duplicates` | GET | List all variations that share a duplicate barcode value | planned |
| `/rest/pim/barcodes/duplicates/count` | GET | Count of duplicate barcodes across the catalogue | planned |
| `/rest/pim/barcodes/duplicates/settings` | GET | Settings controlling barcode duplicate detection behaviour | planned |

#### Item Serial Numbers

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/item-serial-numbers` | GET, PUT, POST, DELETE | Search, create, update, and delete serial numbers assigned to item variations | planned |

#### Item Lookups

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/items/{id}/attributes` | GET | Get all attributes linked to a given item | planned |
| `/rest/pim/items/{id}/combinations` | GET | Get all valid variation combinations (attribute value sets) for a given item | planned |

#### Amazon Product Types

| Endpoint | Methods | Description | Status |
|---|---|---|---|
| `/rest/pim/amazon-product-types` | GET | List Amazon product type definitions available for attribute mapping | planned |
