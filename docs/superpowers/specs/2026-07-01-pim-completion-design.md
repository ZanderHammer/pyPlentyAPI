# PIM Module Completion — Design Spec

**Date:** 2026-07-01
**Status:** Approved

## Overview

`PimModule` (`client.pim`) currently covers 9 of the ~44 operations under the PlentyMarkets `Pim`
API tag: variation search/scroll/bulk-base-update, and read-only lookups for categories,
attributes, and sales prices (see `docs/superpowers/plans/2026-07-01-pim-module.md`, commits
`be57a50`..`af3d616`). This spec covers implementing every remaining `/rest/pim/*` endpoint so the
`Pim` module reaches full API coverage, then bumping the package version `0.1.2` → `0.2.0`.

Endpoint inventory confirmed directly against the OpenAPI spec
(`https://raw.githubusercontent.com/plentymarkets/api-doc/master/plentymarkets/openApiV3/openApiV3.json`):
41 `/rest/pim/*` paths total, matching `ROADMAP.md`'s existing table exactly. 9 operations already
implemented; 8 endpoint groups (~35 methods) remain.

## Scope

- **In scope:** All remaining `/rest/pim/*` endpoints listed in `ROADMAP.md` under the `Pim`
  section that are not already marked `**implemented**`.
- **Out of scope:** Any non-`Pim`-tagged endpoint. No changes to other modules. No changes to
  `_session.py` auth/retry behavior.

## Architecture (unchanged from existing PimModule)

- All new methods added directly to the existing `PimModule` class in
  `src/plentymarkets/modules/pim.py`. No new module, no new `client.py` property, no nested
  accessor classes — matches the flat-class pattern used by `OrdersModule`, `ItemsModule`,
  `StockModule`, `ContactsModule`.
- Every write method (PUT/POST) that accepts a `data` payload gets a matching `TypedDict` in
  `_types.py` (`total=False`, `Required[...]` for mandatory keys per CLAUDE.md convention),
  exported from `__init__.py`.
- Every read method reuses the existing `PimModule._build_params(filters, with_)` helper for
  query-param construction.
- Bulk PUT (create-or-update) and POST (create) endpoints take `list[SomeTypedDict]` and return
  the raw response `dict[str, Any]`, mirroring `update_variation_bases`.
- Bulk DELETE endpoints take `ids: list[int]` (flat list of the sub-record IDs to delete) and
  return the raw response dict. The spec documents no request-body schema for any DELETE
  operation in this scope; `ids: list[int]` matches the most common PlentyMarkets bulk-delete
  convention and keeps the call site simple.
- Tests added to the existing `tests/test_pim.py` using the existing `httpx_mock` fixture
  pattern — no new test infrastructure.

## Naming Conventions

- `update_<x>` — PUT, create-or-update semantics (matches existing `update_variation_bases`
  precedent). Used for all 16 variation bulk sub-resources (PUT-only, no separate POST) and for
  the PUT half of endpoints that also have a separate POST.
- `create_<x>` — POST, used only where the API exposes a distinct POST operation (attributes,
  attribute names/values/value-names, sales prices, barcodes, item serial numbers).
- `delete_<x>` — DELETE, bulk-by-id-list.
- `list_<x>` / `get_<x>` — existing GET conventions, unchanged.

## Field-Name Confidence

The OpenAPI spec provides real request/response schemas for some endpoint groups and none for
others. Where schemas are missing, field names are inferred from PlentyMarkets domain
conventions and the `with_` include vocabulary already documented on `list_variations`
(`"barcodes"`, `"categories"`, `"clients"`, `"salesPrices"`, `"warehouses"`, `"tags"`,
`"properties"`, `"images"`, `"skus"`, `"markets"`, `"defaultCategories"`, `"supplier"`,
`"marketIdentNumbers"`, `"bundleComponents"`, `"comments"`, `"additionalSkus"`). Every inferred
TypedDict carries a docstring caveat: *"field names inferred from PlentyMarkets domain
conventions; verify against a live system before relying on optional keys"* — matching the
caveat already shipped on `update_variation_bases`.

| Group | Schema confidence |
|---|---|
| 1. Variations core + 16 bulk sub-resources | **Inferred** — spec has zero request-body schemas |
| 2. Attributes (core, names, values, value-names) | **Confirmed** — full field schemas in spec |
| 3. Category detail lookups (branches/clients/details/properties) | **Confirmed** — real query params in spec |
| 4. Sales price writes | **Confirmed** for PUT/POST; DELETE reuses PUT's schema in the spec (likely a spec authoring quirk) — treated as `ids: list[int]` per the general DELETE convention |
| 5. Barcodes config | **Confirmed** — full field schemas in spec |
| 6. Item serial numbers | **Confirmed** — full field schemas in spec |
| 7. Item lookups | Read-only, path param only — no ambiguity |
| 8. Amazon product types | Read-only, no params — no ambiguity |

## Endpoint Groups (implementation order)

### Group 1 — Variations core + bulk sub-resources (17 endpoints)

- `create_variations(data: list[VariationCreatePayload]) -> dict` / `delete_variations(ids: list[int]) -> dict`
  — PUT/DELETE `/rest/pim/variations`. `VariationCreatePayload` covers the top-level nested keys
  from the spec: `id`, `additionalSkus`, `attributeValues`, `barcodes`, `bundleComponents`,
  `categories`, `clients`, `defaultCategories`, `images`, `markets`, `marketIdentNumbers`,
  `salesPrices`, `skus`, `supplier`, `warehouses`, `properties`, `tags`, `comments`,
  `inheritance`, `unit`, `base` (each `NotRequired[list[dict[str, Any]]]` except `base`, which is
  `NotRequired[dict[str, Any]]`). The spec's DELETE operation reuses PUT's full request schema
  (same quirk noted for sales prices below) — treated as `ids: list[int]` per the general bulk-
  delete convention rather than requiring a full variation payload to delete by ID.
- For each of `additional_skus`, `barcodes`, `bundle_components`, `categories`, `clients`,
  `comments`, `default_categories`, `images`, `market_ident_numbers`, `markets`, `properties`,
  `sales_prices`, `skus`, `supplier`, `tags`, `warehouses`:
  `update_variation_<resource>(data: list[Variation<Resource>Payload]) -> dict` (PUT) and
  `delete_variation_<resource>(ids: list[int]) -> dict` (DELETE). Each `Variation<Resource>Payload`
  TypedDict has `variationId: Required[int]` plus resource-specific fields inferred per the
  Field-Name Confidence section above.

32 methods, 17 TypedDicts (`VariationCreatePayload` + 16 sub-resource payloads).

### Group 2 — Attributes (16 methods)

- `/rest/pim/attributes`: `create_attributes` (POST), `update_attributes` (PUT),
  `delete_attributes(ids)` (DELETE) — fields: `backendName`, `position`,
  `isSurchargePercental`, `isLinkableToImage`, `amazonAttribute`, `fruugoAttribute`,
  `pixmaniaAttribute`, `ottoAttribute`, `googleShoppingAttribute`, `neckermannAtEpAttribute`,
  `typeOfSelectionInOnlineStore`, `laRedouteAttribute`, `isGroupable`.
- `/rest/pim/attributes/names`: `list_attribute_names`, `create_attribute_names`,
  `update_attribute_names`, `delete_attribute_names(ids)` — fields: `attributeId`, `lang`, `name`.
- `/rest/pim/attributes/values`: `list_attribute_values`, `create_attribute_values`,
  `update_attribute_values`, `delete_attribute_values(ids)`.
- `/rest/pim/attributes/values/{id}`: `get_attribute_value(value_id)`.
- `/rest/pim/attributes/values/names`: `list_attribute_value_names`,
  `create_attribute_value_names`, `update_attribute_value_names`,
  `delete_attribute_value_names(ids)` — fields: `valueId`, `lang`, `name`.

### Group 3 — Category detail lookups (4 methods, read-only)

- `list_category_branches(with_)` — `/rest/pim/categories/branches`
- `list_category_clients(category_id, plenty_id, with_)` — `/rest/pim/categories/clients`
- `list_category_details(category_id, plenty_id, lang, name, name_url, meta_keywords, with_)` —
  `/rest/pim/categories/details`
- `list_category_properties(category_id, plenty_id, value, with_)` — `/rest/pim/categories/properties`

### Group 4 — Sales price writes (3 methods)

- `create_sales_prices` (POST) / `update_sales_prices` (PUT) — fields: `position`,
  `minimumOrderQuantity`, `type`, `isCustomerPrice`, `isDisplayedByDefault`, `isLiveConversion`,
  `interval`, `names`, `countries`, `currencies`, `customerClasses`, `referrers`, `clients`,
  `accounts`.
- `delete_sales_prices(ids: list[int])` (DELETE).

### Group 5 — Barcodes config (7 methods)

- `list_barcodes`, `create_barcodes`, `update_barcodes` (fields: `name`, `type`, `referrers`),
  `delete_barcodes(ids)`.
- `list_barcode_duplicates()`, `count_barcode_duplicates()`, `get_barcode_duplicate_settings()`.

### Group 6 — Item serial numbers (4 methods)

- `list_item_serial_numbers`, `create_item_serial_numbers`, `update_item_serial_numbers`
  (fields: `itemId`, `serialNumber`, `orderId`, `orderItemId`), `delete_item_serial_numbers(ids)`.

### Group 7 — Item lookups (2 methods, read-only)

- `get_item_attributes(item_id)` — `/rest/pim/items/{id}/attributes`
- `get_item_combinations(item_id)` — `/rest/pim/items/{id}/combinations`

### Group 8 — Amazon product types (1 method, read-only)

- `list_amazon_product_types()` — `/rest/pim/amazon-product-types`

## Testing

Each group adds tests to `tests/test_pim.py` following the existing pattern: `httpx_mock`-mocked
happy-path test per method, plus a filter/`with_`-param variant for list methods that accept
query parameters. Estimated ~45-55 new tests across all 8 groups. `uv run pytest` (full suite)
run at the end of each group's task to catch regressions before committing.

## Documentation & Versioning

- Each group updates `CHANGELOG.md` under `[Unreleased] ### Pim` (one `feat:` line per method)
  and flips the corresponding `ROADMAP.md` rows from `planned`/`partial` to `**implemented**` —
  same pattern as the existing plan's Tasks 2 and 3.
- Final task, once all 8 groups are merged and `ROADMAP.md`'s `Pim` section reads fully
  `**implemented**`: run `cz bump` targeting `0.2.0` (minor bump — first additional module beyond
  the 0.1.0 core four to reach full endpoint coverage). Its own commit.

## Branch Workflow

Single feature branch off `staging` (per CLAUDE.md's branch policy) for the entire effort, one
commit per group (8 commits) plus a final version-bump commit, merged back into `staging` when
complete.
