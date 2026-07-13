# Order API Phase 4 — Core Order Metadata — Design Spec

**Date:** 2026-07-13
**Status:** Approved

## Overview

`OrdersModule` (`client.orders`) currently covers 45 of 307 endpoints under the PlentyMarkets
`Order` API tag (see `ROADMAP.md`'s `### Order` section and `docs/superpowers/plans/` history —
the 0.3.0 release brought coverage from a handful of core methods to 45 by adding order item
transactions, items, serial numbers, warehouse locations, and reorders, and split flat
`orders.py` into the `modules/orders/` package of mixins).

This spec covers the next phase: 69 endpoints covering order metadata that isn't yet exposed —
batch/contact/accounting lookups, order-item dates, order and order-item properties, referrers,
currencies, coupons, and TARIC VAT assignments (tagged `Order` in the spec despite being tax/
system config). Full roadmap context (all 307 endpoints, all phases) lives in
`/home/hammer/.claude/plans/pls-plan-the-next-goofy-origami.md` and `ROADMAP.md`; this spec only
details Phase 4.

Endpoint inventory confirmed directly against `docs/openApiV3.json` (byte-identical to the live
spec at the URL in `CLAUDE.md`) and cross-checked against `ROADMAP.md`'s existing per-endpoint
table — both agree on the count: 45 implemented, 69 in scope here.

## Scope

- **In scope:** The 69 `Order`-tagged endpoints listed in the "Endpoint Groups" section below —
  all currently `planned` or `deprecated (...)` in `ROADMAP.md`'s `### Order` table, in the
  batch/contacts/accounting-summary, item-dates, properties, referrers, currencies, coupons, and
  TARIC-VAT families.
- **Out of scope:** Shipping (58 endpoints — Phase 5) and the 13 document-type resources
  (`sales_orders`, `returns`, `repairs`, `warranties`, `subscriptions`, `offers`,
  `advance_orders`, `credit_notes`, `delivery_orders`, `redistributions`, `reorders`-as-a-
  standalone-resource, `multi_orders`, `multi_credit_notes` — 135 endpoints, Phase 6+). No
  changes to other modules. No changes to `_session.py` auth/retry behavior.

## Architecture (extends existing `modules/orders/` package)

- Two existing mixins gain methods: `CoreMixin` (`core.py`, +10 methods) and `DatesMixin`
  (`dates.py`, +9 methods).
- Five new mixins, one per new file, wired into `OrdersModule` in `modules/orders/__init__.py`
  as soon as each is created: `PropertiesMixin` (`properties.py`), `ReferrersMixin`
  (`referrers.py`), `CurrenciesMixin` (`currencies.py`), `CouponsMixin` (`coupons.py`),
  `TaricMixin` (`taric.py`). Each `class FooMixin(OrdersBase):` — same pattern as
  `TransactionsMixin`/`ItemsMixin`/etc.
- Every read method that supports `page`/`itemsPerPage` gets a `paginate_*` async-generator
  wrapper (same shape as `paginate_orders`/`paginate_search`/`paginate_item_transactions`) —
  except where the spec documents no pagination params at all (`list_campaigns`) or the
  endpoint isn't page-shaped (flat lookups).
  Endpoints getting a `paginate_*` wrapper: `list_contact_orders`, `list_accounting_summaries`,
  `search_referrers`, `list_redeemed_coupon_codes`, `list_taric_vat_assignments`.
- Every write method (PUT/POST) with ≥4 payload fields gets a matching `TypedDict` in
  `_types.py` (`total=False`, `Required[...]`/`NotRequired[...]` per CLAUDE.md convention),
  exported from `__init__.py`. Bodies with ≤3 scalar fields use direct keyword arguments instead
  (matches `update_item_transaction`'s existing precedent) — see the Field-Name Confidence table
  below for which methods get which treatment.
- Every list/search method reuses the existing `OrdersBase._build_params(filters, with_,
  **extra)` helper.
- Two endpoints (`update_order_currency`, `update_referrer`) have **zero** documented request
  body in the spec — treated as `data: dict[str, Any]` passthrough with the same Known-Schema-Gap
  docstring caveat already used by `ROADMAP.md`'s "Known Schema Gaps" table and shipped on
  `PimModule.update_variation_bases`.
- Tests: one new `tests/test_orders_<name>.py` per new file (`properties`, `referrers`,
  `currencies`, `coupons`, `taric`), extending `test_orders_core.py`/`test_orders_dates.py` for
  the two extended files — each test file keeps its own local `session`/`orders` fixtures (no
  shared conftest, matching every existing `test_orders_*.py`).

## Naming Conventions

- `list_<x>` / `search_<x>` — GET collection, existing convention.
- `paginate_<x>` — async generator wrapping the matching `list_`/`search_` method.
- `get_<x>` — GET single resource.
- `create_<x>` — POST.
- `update_<x>` — PUT.
- `delete_<x>` — DELETE.
- `_by_type`/`_by_id` suffixes distinguish sibling endpoints addressing the same resource two
  ways (e.g. order-item dates addressed by their own `dateId` vs. by `(orderItemId, typeId)`) —
  mirrors how `TransactionsMixin` already has both `update_item_transaction` (by transaction ID)
  and the `{orderItemId}/transactions` family (scoped to one item).

## Deprecation Handling

~27 of the 69 endpoints carry `<b>DEPRECATED: Use the following route: ...</b>` in their spec
`description` field (verified directly, not inferred): all 9 order-item-date endpoints, all 15
order-level and order-item-level property-*value* endpoints (property *types* are NOT
deprecated), and 3 outgoing-stock/booking endpoints in `core.py`. Each deprecated method still
gets implemented (matches this repo's philosophy of full endpoint coverage tracked in
`ROADMAP.md` regardless of deprecation status) but carries a prominent docstring `Note:` naming
the replacement route.

**Correction to `ROADMAP.md`**: its table currently shows the 6 order-level property-value rows
(`/rest/orders/properties/{id}` PUT/DELETE, `/rest/orders/{orderId}/properties*` POST/GET/PUT/
DELETE) as plain `planned`, missing the `deprecated (use PUT /rest/orders/{orderId})` annotation
their sibling item-level rows already carry. Verified directly against the live spec description
field — all 6 do carry the deprecation notice. Fix these 6 rows' Status column alongside marking
them implemented.

## Spec Quirks (apply the documented resolution; don't silently "fix" the wire format)

| Quirk | Where | Resolution |
|---|---|---|
| Path param literally named `{parentReferrerId?}` / `{typeId?}`, yet `required: true` | `create_referrer`, `list_order_properties` (`/rest/orders/{orderId}/properties/{typeId?}`) | Implement as a required Python param; docstring `Note:` flags the spec contradiction (description text implies optional/auto-assigned) and recommends live-system verification. |
| `Collection` response schema is a bare `{"type": "object"}`, not confidently an array | `get_orders_batch` (`GET /rest/orders/batch`) | Return `Any` (not `list[...]`) with a strong verify-before-relying-on-this Note — stronger than the usual placeholder caveat since even the array-vs-object shape is unverified. |
| `OrderBooking` response schema is a bare placeholder | `book_order_in` | `dict[str, Any]` + Note, same treatment as `book_item_in`/`book_item_transactions`. |
| Response items are `$ref: mixed` | `list_exchange_rates_from`, `list_exchange_rates_to`, `validate_order_coupon` | `list[Any]` + Note + `# type: ignore[return-value]`, matching `get_my_account_url`'s existing precedent. |
| Same identifier typed `string` on some operations, `integer` on siblings | `currencyIso` (string on lookups, integer on the 2 exchange-rate ops); `code`/`coupon` (string on GET, integer on DELETE/PUT/validate); `taricCode` (string as path param, integer inside every requestBody that redeclares it) | Use `str` uniformly (all are alphanumeric per their regex constraints); flag the inconsistency in each affected docstring. |
| Path params redundantly redeclared as required body fields | `create_taric_vat_assignment`/`update_taric_vat_assignment` (`taricCode`/`countryId`), `create_item_date_by_type`/`update_item_date_by_type`, `create_order_property`/`update_order_property_by_type`, `create_item_property_by_type`/`update_item_property_by_type` | Merge path args into the JSON body automatically inside the method; never expose them as separate body keys — matches `create_item_transaction`'s existing precedent (`json={**data, "orderItemId": order_item_id}`). |
| DELETE with a spurious requestBody that redeclares path params, nothing new | `delete_taric_vat_assignment` | Omit the body entirely — matches `delete_status_definition`/`delete_order_item`, which never resend path-supplied fields. |
| Non-standard pagination defaults | `documents/accounting_summary` (`itemsPerPage` default 10, not this repo's usual 50); `referrers/search` (default 20) | Use the spec's stated default, not the repo-wide 50; note the deviation in the docstring. |
| Page-shaped response, zero query params documented | `GET /rest/orders/coupons/campaigns` | `list_campaigns()` takes no args, no `paginate_*` wrapper possible; flag the oddity. |
| `with` param is a plain `string`, not the usual `array[string]` | `GET /rest/orders/coupons/campaigns/codes/{code}` | `with_: str \| None = None` → `{"with": with_}`, bypassing `_build_params`'s list-join convention for this one call. |
| Redundant-looking dual required fields (`name`+`lang` *and* `names` array) | `POST /rest/orders/properties/types` | Implement literally per spec (both required) — don't collapse/guess; flag with a Note. |
| `required` array vs. field *description* text disagree on which fields are optional | `DELETE /rest/orders/items/outgoing_stocks` (`id`/`quantity`/`warehouseId` all in `required`, but descriptions call `quantity`/`warehouseId` "optional") | The `required` array is authoritative for typing; flag both readings in the docstring Note. |

## Endpoint Groups (implementation order — 17 tasks, see the plan doc for full detail)

### Group 1 — `core.py` extensions (10 endpoints, 4 tasks)
`get_orders_batch`, `list_contact_orders`/`paginate_contact_orders`, `create_multi_order`,
`list_accounting_summaries`/`paginate_accounting_summaries`, `book_order_in`,
`get_contact_wish`, `update_order_currency`, `revert_item_outgoing_stock`,
`book_out_order_items`, `revert_order_outgoing_stock`.

### Group 2 — `dates.py` extensions (9 endpoints, 2 tasks)
Order-item dates: `create_item_date`/`delete_item_date`/`get_item_date`/`update_item_date` (by
`dateId`) and `list_item_dates`/`delete_item_date_by_type`/`get_item_date_by_type`/
`create_item_date_by_type`/`update_item_date_by_type` (by `orderItemId`+`typeId`). Also fixes
`TransactionsMixin`'s class docstring, which currently (and after this phase, incorrectly)
states these are "intentionally not implemented here."

### Group 3 — `properties.py` (new file, 20 endpoints, 4 tasks)
Property types (5, not deprecated): `list_property_types`, `create_property_type`,
`delete_property_type`, `get_property_type`, `update_property_type` — 3 new TypedDicts
(`OrderPropertyTypeNamePayload`, `OrderPropertyTypeCreatePayload`,
`OrderPropertyTypeUpdatePayload`).
Order-level property values (6, deprecated): `delete_order_property`, `update_order_property`,
`create_order_property`, `list_order_properties`, `delete_order_property_by_type`,
`update_order_property_by_type`.
Order-item property values (9, deprecated): `create_item_property`, `delete_item_property`,
`get_item_property`, `update_item_property`, `list_item_properties`,
`delete_item_property_by_type`, `get_item_property_by_type`, `create_item_property_by_type`,
`update_item_property_by_type`.

### Group 4 — `referrers.py` (new file, 7 endpoints, 1 task)
`list_referrers`, `get_next_free_referrer_id`, `search_referrers`/`paginate_referrers`,
`create_referrer`, `delete_referrer`, `get_referrer`, `update_referrer`.

### Group 5 — `currencies.py` (new file, 7 endpoints, 1 task)
`list_currencies`, `get_currency_for_country`, `list_exchange_rates_from`,
`list_exchange_rates_to`, `get_currency`, `list_currency_countries`,
`get_currency_exchange_rate`. All GET, no writes, no TypedDicts.

### Group 6 — `coupons.py` (new file, 11 endpoints, 2 tasks)
Campaigns/codes management: `list_campaigns`, `delete_coupon_code`, `get_coupon_code`,
`set_coupon_code_disabled`, `get_campaign`, `create_coupon_code` — 1 new TypedDict
(`OrderCouponCodeCreatePayload`).
Validation/redemption: `validate_coupons`, `list_redeemed_coupon_codes`/
`paginate_redeemed_coupon_codes`, `validate_coupon`, `redeem_coupon`, `validate_order_coupon` —
1 new TypedDict (`OrderCouponValidatePayload`).

### Group 7 — `taric.py` (new file, 5 endpoints, 1 task)
`list_taric_vat_assignments`/`paginate_taric_vat_assignments`, `delete_taric_vat_assignment`,
`get_taric_vat_assignment`, `create_taric_vat_assignment`, `update_taric_vat_assignment`.

**Endpoint-count check:** 10 + 9 + 20 + 7 + 7 + 11 + 5 = **69** ✓ (17 implementation tasks + 1
final verification/version-bump task = 18 total).

## Testing

Each task adds tests to the relevant `tests/test_orders_*.py` file following the existing
pattern: `httpx_mock`-mocked happy-path test per method, plus a filters/`with_`-param variant
for list/search methods that accept query parameters, plus yields-across-pages/stops-on-empty
tests for each `paginate_*` wrapper (mirrors `test_paginate_orders_yields_all_items_across_pages`
/ `test_paginate_orders_stops_on_empty_entries` in `test_orders_core.py`). Estimated ~74-85 new
tests across all 7 groups. `uv run pytest` (full suite) run at the end of each task to catch
regressions before committing.

## Documentation & Versioning

- Each task updates `CHANGELOG.md` under `[Unreleased] ### Order` (one `feat:` line per method)
  and flips the corresponding `ROADMAP.md` rows from `planned`/`deprecated (...)` to
  `**implemented**` + method name — same pattern as the 0.3.0 and Pim-completion work. The 6
  order-level-property rows additionally get their missing `deprecated (...)` annotation added
  (see Deprecation Handling above).
- Final task, once all 69 rows read `**implemented**`: run `uv run cz bump` (conventional-commit
  `feat:` entries trigger a minor bump automatically — expected `0.3.2` → `0.4.0`, matching the
  0.3.0 precedent where the prior orders coverage milestone was also a minor bump). Its own
  commit.

## Branch Workflow

Single feature branch off `staging` (per `CLAUDE.md`'s branch policy) for the entire effort, one
commit per task (17 commits) plus a final version-bump commit, merged back into `staging` when
complete.
