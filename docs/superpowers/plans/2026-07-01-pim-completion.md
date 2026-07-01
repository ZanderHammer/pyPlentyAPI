# PIM Module Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement every remaining `/rest/pim/*` endpoint on the existing `PimModule` (`client.pim`) so the `Pim` module reaches full API coverage, then bump the package version `0.1.2` → `0.2.0`.

**Architecture:** All new methods are added directly to the existing `PimModule` class in `src/plentymarkets/modules/pim.py` — no new module, no new `client.py` property. Every write method (PUT/POST) gets a matching `TypedDict` in `_types.py`, exported from `__init__.py`. Every read method reuses the existing `PimModule._build_params(filters, with_)` helper. Bulk PUT/POST endpoints take `list[SomeTypedDict]`; bulk DELETE endpoints take `ids: list[int]`. Tests are appended to the existing `tests/test_pim.py` using the existing `httpx_mock` fixture pattern.

**Tech Stack:** Python ≥3.11, httpx (via shared `_Session`), pytest + pytest-httpx (unit tests mock at the transport layer — no live network needed).

**Spec:** `docs/superpowers/specs/2026-07-01-pim-completion-design.md`

## Global Constraints

- All source under `src/plentymarkets/`; tests under `tests/`
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio` decorator on any test
- Google-style docstrings on every public method; document every response key and every payload key
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`
- `CHANGELOG.md`: append only to `[Unreleased]`; group under `## Pim`
- `ROADMAP.md`: update Status column from `planned`/`partial` → `**implemented**` for each endpoint as it is implemented
- Branch: single feature branch off `staging` for this whole plan; `main` is protected
- Where the OpenAPI spec publishes no request/response schema for an endpoint, TypedDict fields and response-key docs are inferred from PlentyMarkets domain conventions and must carry the caveat: *"PlentyMarkets does not publish a fixed schema for this endpoint; verify against a live system before relying on these keys."* — same pattern already shipped on `update_variation_bases`.
- Bulk DELETE endpoints take `ids: list[int]` (flat list of sub-record IDs), sent as the JSON body via `self._session.delete(path, json=ids)`.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Modify | `src/plentymarkets/_types.py` | Add ~24 new TypedDicts for PIM write payloads |
| Modify | `src/plentymarkets/__init__.py` | Export all new TypedDicts |
| Modify | `src/plentymarkets/modules/pim.py` | Add ~35 new methods to `PimModule` |
| Modify | `tests/test_pim.py` | Add ~50 new tests |
| Modify | `CHANGELOG.md` | Add `[Unreleased] ## Pim` entries per task |
| Modify | `ROADMAP.md` | Mark endpoints implemented per task |
| Modify | `pyproject.toml`, `CHANGELOG.md` | Final task: version bump via `cz bump` |

---

## Task 1: Variations core — create and delete

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._session.put`, `PimModule._session.delete` (existing `_Session` methods)
- Produces:
  - `VariationCreatePayload` TypedDict (exported from `plentymarkets`)
  - `PimModule.create_variations(data: list[VariationCreatePayload]) -> dict[str, Any]`
  - `PimModule.delete_variations(ids: list[int]) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_create_variations_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"created": 1},
    )
    result = await pim.create_variations([{"id": 1, "base": {"itemId": 42}}])
    assert result["created"] == 1


async def test_delete_variations_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"deleted": 2},
    )
    result = await pim.delete_variations([1, 2])
    assert result["deleted"] == 2
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "test_create_variations_puts_data or test_delete_variations_sends_ids" -v`
Expected: `AttributeError: 'PimModule' object has no attribute 'create_variations'`

- [ ] **Step 3: Add `VariationCreatePayload` to `_types.py`**

Append after the `VariationBaseUpdatePayload` class in `src/plentymarkets/_types.py`:

```python
class VariationCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_variations` (``PUT /rest/pim/variations``).

    Creates or fully replaces variations along with their nested related data
    in a single call. Prefer :meth:`PimModule.update_variation_bases` for
    simple base-field updates; use this payload when creating new variations
    or writing several related-data collections at once.

    Keys:
        id: Variation ID. Required when updating an existing variation;
            omit to create a new one.
        base: Base variation fields (see
            :class:`~plentymarkets._types.VariationBaseUpdatePayload`).
        additionalSkus: List of additional-SKU dicts (see
            :class:`~plentymarkets._types.VariationAdditionalSkuPayload`).
        attributeValues: List of attribute-value link dicts, each with
            ``attributeId`` and ``valueId``.
        barcodes: List of barcode link dicts (see
            :class:`~plentymarkets._types.VariationBarcodePayload`).
        bundleComponents: List of bundle component dicts (see
            :class:`~plentymarkets._types.VariationBundleComponentPayload`).
        categories: List of category link dicts (see
            :class:`~plentymarkets._types.VariationCategoryPayload`).
        clients: List of client visibility dicts (see
            :class:`~plentymarkets._types.VariationClientPayload`).
        defaultCategories: List of default-category dicts (see
            :class:`~plentymarkets._types.VariationDefaultCategoryPayload`).
        images: List of image link dicts (see
            :class:`~plentymarkets._types.VariationImagePayload`).
        markets: List of market availability dicts (see
            :class:`~plentymarkets._types.VariationMarketPayload`).
        marketIdentNumbers: List of MIN dicts (see
            :class:`~plentymarkets._types.VariationMarketIdentNumberPayload`).
        salesPrices: List of sales price link dicts (see
            :class:`~plentymarkets._types.VariationSalesPricePayload`).
        skus: List of marketplace SKU dicts (see
            :class:`~plentymarkets._types.VariationSkuPayload`).
        supplier: List of supplier link dicts (see
            :class:`~plentymarkets._types.VariationSupplierPayload`).
        warehouses: List of warehouse stock dicts (see
            :class:`~plentymarkets._types.VariationWarehousePayload`).
        properties: List of property dicts (see
            :class:`~plentymarkets._types.VariationPropertyPayload`).
        tags: List of tag link dicts (see
            :class:`~plentymarkets._types.VariationTagPayload`).
        comments: List of comment dicts (see
            :class:`~plentymarkets._types.VariationCommentPayload`).
        inheritance: List of inheritance-configuration dicts controlling
            which fields a child variation inherits from its parent.
        unit: List with a single unit-configuration dict, e.g.
            ``{"unitId": 1, "content": 1}``.
    """

    id: NotRequired[int]
    base: NotRequired[dict[str, Any]]
    additionalSkus: NotRequired[list[dict[str, Any]]]
    attributeValues: NotRequired[list[dict[str, Any]]]
    barcodes: NotRequired[list[dict[str, Any]]]
    bundleComponents: NotRequired[list[dict[str, Any]]]
    categories: NotRequired[list[dict[str, Any]]]
    clients: NotRequired[list[dict[str, Any]]]
    defaultCategories: NotRequired[list[dict[str, Any]]]
    images: NotRequired[list[dict[str, Any]]]
    markets: NotRequired[list[dict[str, Any]]]
    marketIdentNumbers: NotRequired[list[dict[str, Any]]]
    salesPrices: NotRequired[list[dict[str, Any]]]
    skus: NotRequired[list[dict[str, Any]]]
    supplier: NotRequired[list[dict[str, Any]]]
    warehouses: NotRequired[list[dict[str, Any]]]
    properties: NotRequired[list[dict[str, Any]]]
    tags: NotRequired[list[dict[str, Any]]]
    comments: NotRequired[list[dict[str, Any]]]
    inheritance: NotRequired[list[dict[str, Any]]]
    unit: NotRequired[list[dict[str, Any]]]
```

This class uses `Any` and `dict` — confirm the top of `_types.py` already imports them; if not, add `from typing import Any` to the existing `from typing import NotRequired, Required, TypedDict` import line.

- [ ] **Step 4: Export `VariationCreatePayload` from `__init__.py`**

In `src/plentymarkets/__init__.py`, add `VariationCreatePayload` to both the import list and `__all__`:

```python
from ._types import (
    ContactCreatePayload,
    ContactUpdatePayload,
    ItemCreatePayload,
    ItemUpdatePayload,
    OrderCreatePayload,
    StockCorrectionPayload,
    VariationBaseUpdatePayload,
    VariationCreatePayload,
)

__all__ = [
    "PlentyClient",
    "OrderCreatePayload",
    "ItemCreatePayload",
    "ItemUpdatePayload",
    "StockCorrectionPayload",
    "ContactCreatePayload",
    "ContactUpdatePayload",
    "VariationBaseUpdatePayload",
    "VariationCreatePayload",
]
```

- [ ] **Step 5: Implement `create_variations` and `delete_variations` in `pim.py`**

Add these methods to `PimModule` immediately after `update_variation_bases`:

```python
async def create_variations(
    self,
    data: list[VariationCreatePayload],
) -> dict[str, Any]:
    """Bulk create or fully update variations and their related data.

    Args:
        data: List of variation payloads. Use
            :class:`~plentymarkets._types.VariationCreatePayload` for IDE
            autocomplete. Omit ``id`` to create a new variation; include it
            to update an existing one.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; based on the
        bulk-endpoint pattern used elsewhere in the API, expect:

        - ``created`` (int): Number of variations successfully created or
          updated.
        - ``invalid`` (list[dict]): Entries that failed validation, each
          with ``id`` and ``reason``.

        Verify against a live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations", json=data)

async def delete_variations(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variations by ID.

    Args:
        ids: List of variation IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int): number of variations removed. Verify against a
        live system before relying on this key.
    """
    return await self._session.delete("/rest/pim/variations", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass, including the two new ones.

- [ ] **Step 7: Update `CHANGELOG.md`**

Add to the existing `### Pim` section under `[Unreleased]` in `CHANGELOG.md`:

```markdown
- feat: `PimModule.create_variations` — bulk create/update variations via `PUT /rest/pim/variations`
- feat: `PimModule.delete_variations` — bulk delete variations via `DELETE /rest/pim/variations`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change the `/rest/pim/variations` row's status from `partial` to `**implemented**` and update the Methods cell so PUT and DELETE no longer read as outstanding:

```
| `/rest/pim/variations` | GET, PUT, DELETE (all **implemented**) | List/filter variations (70+ filter params, `with` for eager-loading includes); bulk update and delete | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add variation bulk create and delete"
```

---

## Task 2: Variation bulk sub-resources — batch A (additional SKUs, barcodes, bundle components, categories)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.put`, `_Session.delete`
- Produces:
  - `VariationAdditionalSkuPayload`, `VariationBarcodePayload`, `VariationBundleComponentPayload`, `VariationCategoryPayload` TypedDicts
  - `PimModule.update_variation_additional_skus(data) -> dict[str, Any]` / `PimModule.delete_variation_additional_skus(ids) -> dict[str, Any]`
  - `PimModule.update_variation_barcodes(data) -> dict[str, Any]` / `PimModule.delete_variation_barcodes(ids) -> dict[str, Any]`
  - `PimModule.update_variation_bundle_components(data) -> dict[str, Any]` / `PimModule.delete_variation_bundle_components(ids) -> dict[str, Any]`
  - `PimModule.update_variation_categories(data) -> dict[str, Any]` / `PimModule.delete_variation_categories(ids) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_update_variation_additional_skus_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/additional_skus",
        json={"updated": 1},
    )
    result = await pim.update_variation_additional_skus(
        [{"variationId": 7, "referrerId": 1, "sku": "ABC-1"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_additional_skus_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/additional_skus",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_additional_skus([10])
    assert result["deleted"] == 1


async def test_update_variation_barcodes_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/barcodes",
        json={"updated": 1},
    )
    result = await pim.update_variation_barcodes([{"variationId": 7, "barcodeId": 3}])
    assert result["updated"] == 1


async def test_delete_variation_barcodes_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/barcodes",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_barcodes([3])
    assert result["deleted"] == 1


async def test_update_variation_bundle_components_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/bundle_components",
        json={"updated": 1},
    )
    result = await pim.update_variation_bundle_components(
        [{"variationId": 7, "componentVariationId": 8, "componentQuantity": 2}]
    )
    assert result["updated"] == 1


async def test_delete_variation_bundle_components_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/bundle_components",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_bundle_components([8])
    assert result["deleted"] == 1


async def test_update_variation_categories_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/categories",
        json={"updated": 1},
    )
    result = await pim.update_variation_categories([{"variationId": 7, "categoryId": 5}])
    assert result["updated"] == 1


async def test_delete_variation_categories_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/categories",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_categories([5])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "additional_skus or variation_barcodes or bundle_components or variation_categories" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add the four TypedDicts to `_types.py`**

Append after `VariationCreatePayload`:

```python
class VariationAdditionalSkuPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_additional_skus`
    (``PUT /rest/pim/variations/additional_skus``).

    Keys:
        variationId: Variation ID to attach the SKU to. **Required.**
        id: Additional-SKU record ID, when updating an existing entry.
        referrerId: Referrer/marketplace ID the SKU applies to.
        sku: The additional SKU string.
    """

    variationId: Required[int]
    id: NotRequired[int]
    referrerId: NotRequired[int]
    sku: NotRequired[str]


class VariationBarcodePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_barcodes`
    (``PUT /rest/pim/variations/barcodes``).

    Keys:
        variationId: Variation ID to link the barcode to. **Required.**
        barcodeId: ID of an existing barcode type from
            ``/rest/pim/barcodes``. **Required.**
        code: Barcode value override for this variation, if the barcode
            type allows per-variation codes.
    """

    variationId: Required[int]
    barcodeId: Required[int]
    code: NotRequired[str]


class VariationBundleComponentPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_bundle_components`
    (``PUT /rest/pim/variations/bundle_components``).

    Keys:
        variationId: Variation ID of the bundle itself. **Required.**
        componentVariationId: Variation ID of the component contained in
            the bundle. **Required.**
        componentQuantity: Quantity of the component variation included
            per bundle unit.
    """

    variationId: Required[int]
    componentVariationId: Required[int]
    componentQuantity: NotRequired[float]


class VariationCategoryPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_categories`
    (``PUT /rest/pim/variations/categories``).

    Keys:
        variationId: Variation ID to link to the category. **Required.**
        categoryId: Category ID to link. **Required.**
        plentyId: Client (store) ID the link applies to.
    """

    variationId: Required[int]
    categoryId: Required[int]
    plentyId: NotRequired[int]
```

- [ ] **Step 4: Export the four TypedDicts from `__init__.py`**

Add `VariationAdditionalSkuPayload`, `VariationBarcodePayload`, `VariationBundleComponentPayload`,
`VariationCategoryPayload` to both the import list and `__all__` in `src/plentymarkets/__init__.py`.

- [ ] **Step 5: Implement the eight methods in `pim.py`**

Add after `delete_variations`. Note the response-key docstring wording is identical across all
bulk variation sub-resource methods in this and every following task — this is intentional
(PlentyMarkets publishes no schema for any of them):

```python
async def update_variation_additional_skus(
    self,
    data: list[VariationAdditionalSkuPayload],
) -> dict[str, Any]:
    """Bulk create or update variation additional SKUs.

    Args:
        data: List of additional-SKU payloads. Use
            :class:`~plentymarkets._types.VariationAdditionalSkuPayload`
            for IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; based on the
        bulk-endpoint pattern used elsewhere in the API, expect
        ``updated`` (int) and ``invalid`` (list[dict], each with ``id``
        and ``reason``). Verify against a live system before relying on
        these keys.
    """
    return await self._session.put(
        "/rest/pim/variations/additional_skus", json=data
    )

async def delete_variation_additional_skus(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation additional SKUs by ID.

    Args:
        ids: List of additional-SKU record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete(
        "/rest/pim/variations/additional_skus", json=ids
    )

async def update_variation_barcodes(
    self,
    data: list[VariationBarcodePayload],
) -> dict[str, Any]:
    """Bulk create or update variation barcode links.

    Args:
        data: List of barcode link payloads. Use
            :class:`~plentymarkets._types.VariationBarcodePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/barcodes", json=data)

async def delete_variation_barcodes(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation barcode links by ID.

    Args:
        ids: List of variation-barcode link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/barcodes", json=ids)

async def update_variation_bundle_components(
    self,
    data: list[VariationBundleComponentPayload],
) -> dict[str, Any]:
    """Bulk create or update bundle components on a variation.

    Args:
        data: List of bundle component payloads. Use
            :class:`~plentymarkets._types.VariationBundleComponentPayload`
            for IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put(
        "/rest/pim/variations/bundle_components", json=data
    )

async def delete_variation_bundle_components(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete bundle components by ID.

    Args:
        ids: List of bundle component record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete(
        "/rest/pim/variations/bundle_components", json=ids
    )

async def update_variation_categories(
    self,
    data: list[VariationCategoryPayload],
) -> dict[str, Any]:
    """Bulk create or update category links on variations.

    Args:
        data: List of category link payloads. Use
            :class:`~plentymarkets._types.VariationCategoryPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/categories", json=data)

async def delete_variation_categories(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation category links by ID.

    Args:
        ids: List of variation-category link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/categories", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.update_variation_additional_skus` / `delete_variation_additional_skus` — `/rest/pim/variations/additional_skus`
- feat: `PimModule.update_variation_barcodes` / `delete_variation_barcodes` — `/rest/pim/variations/barcodes`
- feat: `PimModule.update_variation_bundle_components` / `delete_variation_bundle_components` — `/rest/pim/variations/bundle_components`
- feat: `PimModule.update_variation_categories` / `delete_variation_categories` — `/rest/pim/variations/categories`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change these four rows' Status to `**implemented**`:

```
| `/rest/pim/variations/additional_skus` | PUT, DELETE | Bulk create/update/delete variation additional SKUs | **implemented** |
| `/rest/pim/variations/barcodes` | PUT, DELETE | Bulk create/update/delete variation barcodes | **implemented** |
| `/rest/pim/variations/bundle_components` | PUT, DELETE | Bulk create/update/delete bundle components on variations | **implemented** |
| `/rest/pim/variations/categories` | PUT, DELETE | Bulk create/update/delete category links on variations | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add variation additional-sku, barcode, bundle-component, and category bulk ops"
```

---

## Task 3: Variation bulk sub-resources — batch B (clients, comments, default categories, images)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.put`, `_Session.delete`
- Produces:
  - `VariationClientPayload`, `VariationCommentPayload`, `VariationDefaultCategoryPayload`, `VariationImagePayload` TypedDicts
  - `PimModule.update_variation_clients(data)` / `delete_variation_clients(ids)`
  - `PimModule.update_variation_comments(data)` / `delete_variation_comments(ids)`
  - `PimModule.update_variation_default_categories(data)` / `delete_variation_default_categories(ids)`
  - `PimModule.update_variation_images(data)` / `delete_variation_images(ids)`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_update_variation_clients_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/clients",
        json={"updated": 1},
    )
    result = await pim.update_variation_clients([{"variationId": 7, "plentyId": 1}])
    assert result["updated"] == 1


async def test_delete_variation_clients_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/clients",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_clients([1])
    assert result["deleted"] == 1


async def test_update_variation_comments_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/comments",
        json={"updated": 1},
    )
    result = await pim.update_variation_comments(
        [{"variationId": 7, "text": "Check supplier lead time"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_comments_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/comments",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_comments([12])
    assert result["deleted"] == 1


async def test_update_variation_default_categories_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/default_categories",
        json={"updated": 1},
    )
    result = await pim.update_variation_default_categories(
        [{"variationId": 7, "categoryId": 5, "plentyId": 1}]
    )
    assert result["updated"] == 1


async def test_delete_variation_default_categories_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/default_categories",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_default_categories([5])
    assert result["deleted"] == 1


async def test_update_variation_images_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/images",
        json={"updated": 1},
    )
    result = await pim.update_variation_images([{"variationId": 7, "imageId": 9}])
    assert result["updated"] == 1


async def test_delete_variation_images_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/images",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_images([9])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "variation_clients or variation_comments or default_categories or variation_images" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add the four TypedDicts to `_types.py`**

Append after `VariationCategoryPayload`:

```python
class VariationClientPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_clients`
    (``PUT /rest/pim/variations/clients``).

    Keys:
        variationId: Variation ID to make visible in the client. **Required.**
        plentyId: Client (store) ID the variation should be visible in.
            **Required.**
    """

    variationId: Required[int]
    plentyId: Required[int]


class VariationCommentPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_comments`
    (``PUT /rest/pim/variations/comments``).

    Keys:
        variationId: Variation ID to attach the comment to. **Required.**
        text: Comment text. **Required.**
        userId: ID of the back-end user who authored the comment.
        isPermanent: Whether the comment persists across imports/syncs
            instead of being overwritten.
    """

    variationId: Required[int]
    text: Required[str]
    userId: NotRequired[int]
    isPermanent: NotRequired[bool]


class VariationDefaultCategoryPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_default_categories`
    (``PUT /rest/pim/variations/default_categories``).

    Keys:
        variationId: Variation ID to set the default category for.
            **Required.**
        categoryId: Category ID to use as the default (canonical) category
            for this client. **Required.**
        plentyId: Client (store) ID the default applies to. **Required.**
    """

    variationId: Required[int]
    categoryId: Required[int]
    plentyId: Required[int]


class VariationImagePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_images`
    (``PUT /rest/pim/variations/images``).

    Keys:
        variationId: Variation ID to link the image to. **Required.**
        imageId: ID of an existing item image to link. **Required.**
        position: Display sort position among the variation's images.
    """

    variationId: Required[int]
    imageId: Required[int]
    position: NotRequired[int]
```

- [ ] **Step 4: Export the four TypedDicts from `__init__.py`**

Add `VariationClientPayload`, `VariationCommentPayload`, `VariationDefaultCategoryPayload`,
`VariationImagePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the eight methods in `pim.py`**

Add after `delete_variation_categories`:

```python
async def update_variation_clients(
    self,
    data: list[VariationClientPayload],
) -> dict[str, Any]:
    """Bulk create client (store) visibility links on variations.

    Args:
        data: List of client visibility payloads. Use
            :class:`~plentymarkets._types.VariationClientPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/clients", json=data)

async def delete_variation_clients(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation client visibility links by ID.

    Args:
        ids: List of variation-client link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/clients", json=ids)

async def update_variation_comments(
    self,
    data: list[VariationCommentPayload],
) -> dict[str, Any]:
    """Bulk create or update variation comments.

    Args:
        data: List of comment payloads. Use
            :class:`~plentymarkets._types.VariationCommentPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/comments", json=data)

async def delete_variation_comments(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation comments by ID.

    Args:
        ids: List of comment record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/comments", json=ids)

async def update_variation_default_categories(
    self,
    data: list[VariationDefaultCategoryPayload],
) -> dict[str, Any]:
    """Bulk create or update the default category per client on variations.

    Args:
        data: List of default-category payloads. Use
            :class:`~plentymarkets._types.VariationDefaultCategoryPayload`
            for IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put(
        "/rest/pim/variations/default_categories", json=data
    )

async def delete_variation_default_categories(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation default-category links by ID.

    Args:
        ids: List of default-category record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete(
        "/rest/pim/variations/default_categories", json=ids
    )

async def update_variation_images(
    self,
    data: list[VariationImagePayload],
) -> dict[str, Any]:
    """Bulk create image links on variations.

    Args:
        data: List of image link payloads. Use
            :class:`~plentymarkets._types.VariationImagePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/images", json=data)

async def delete_variation_images(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation image links by ID.

    Args:
        ids: List of variation-image link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/images", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.update_variation_clients` / `delete_variation_clients` — `/rest/pim/variations/clients`
- feat: `PimModule.update_variation_comments` / `delete_variation_comments` — `/rest/pim/variations/comments`
- feat: `PimModule.update_variation_default_categories` / `delete_variation_default_categories` — `/rest/pim/variations/default_categories`
- feat: `PimModule.update_variation_images` / `delete_variation_images` — `/rest/pim/variations/images`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change these four rows' Status to `**implemented**`:

```
| `/rest/pim/variations/clients` | PUT, DELETE | Bulk create/delete client (store) visibility on variations | **implemented** |
| `/rest/pim/variations/comments` | PUT, DELETE | Bulk create/update/delete variation comments | **implemented** |
| `/rest/pim/variations/default_categories` | PUT, DELETE | Bulk create/update/delete default category per client on variations | **implemented** |
| `/rest/pim/variations/images` | PUT, DELETE | Bulk create/delete image links on variations | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add variation client, comment, default-category, and image bulk ops"
```

---

## Task 4: Variation bulk sub-resources — batch C (market ident numbers, markets, properties, sales prices)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.put`, `_Session.delete`
- Produces:
  - `VariationMarketIdentNumberPayload`, `VariationMarketPayload`, `VariationPropertyPayload`, `VariationSalesPricePayload` TypedDicts
  - `PimModule.update_variation_market_ident_numbers(data)` / `delete_variation_market_ident_numbers(ids)`
  - `PimModule.update_variation_markets(data)` / `delete_variation_markets(ids)`
  - `PimModule.update_variation_properties(data)` / `delete_variation_properties(ids)`
  - `PimModule.update_variation_sales_prices(data)` / `delete_variation_sales_prices(ids)`

Note: `VariationSalesPricePayload` (this task) links a variation to a *price value*; it is
distinct from the sales price *configuration* CRUD added in Task 11
(`/rest/pim/sales_prices`, which defines price types like "default"/"rrp").

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_update_variation_market_ident_numbers_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/market_ident_numbers",
        json={"updated": 1},
    )
    result = await pim.update_variation_market_ident_numbers(
        [{"variationId": 7, "marketIdentNumberType": "ean", "marketIdentNumber": "4006381333931"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_market_ident_numbers_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/market_ident_numbers",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_market_ident_numbers([4])
    assert result["deleted"] == 1


async def test_update_variation_markets_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/markets",
        json={"updated": 1},
    )
    result = await pim.update_variation_markets([{"variationId": 7, "marketId": 2}])
    assert result["updated"] == 1


async def test_delete_variation_markets_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/markets",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_markets([2])
    assert result["deleted"] == 1


async def test_update_variation_properties_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/properties",
        json={"updated": 1},
    )
    result = await pim.update_variation_properties(
        [{"variationId": 7, "propertyId": 3, "propertyValue": "Cotton"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_properties_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/properties",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_properties([3])
    assert result["deleted"] == 1


async def test_update_variation_sales_prices_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/sales_prices",
        json={"updated": 1},
    )
    result = await pim.update_variation_sales_prices(
        [{"variationId": 7, "salesPriceId": 1, "price": 19.99}]
    )
    assert result["updated"] == 1


async def test_delete_variation_sales_prices_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/sales_prices",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_sales_prices([1])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "market_ident_numbers or variation_markets or variation_properties or variation_sales_prices" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add the four TypedDicts to `_types.py`**

Append after `VariationImagePayload`:

```python
class VariationMarketIdentNumberPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_market_ident_numbers`
    (``PUT /rest/pim/variations/market_ident_numbers``).

    Keys:
        variationId: Variation ID to attach the identifier to. **Required.**
        marketIdentNumberType: Identifier type, e.g. ``"ean"``, ``"isbn"``,
            ``"upc"``, ``"gtin"``. **Required.**
        marketIdentNumber: The identifier value itself. **Required.**
    """

    variationId: Required[int]
    marketIdentNumberType: Required[str]
    marketIdentNumber: Required[str]


class VariationMarketPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_markets`
    (``PUT /rest/pim/variations/markets``).

    Keys:
        variationId: Variation ID to enable for the market. **Required.**
        marketId: Marketplace ID (e.g. an Amazon or eBay account ID
            configured under Market settings). **Required.**
    """

    variationId: Required[int]
    marketId: Required[int]


class VariationPropertyPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_properties`
    (``PUT /rest/pim/variations/properties``).

    Keys:
        variationId: Variation ID to set the property on. **Required.**
        propertyId: Item property ID (from ``/rest/items/properties``).
            **Required.**
        propertyValue: Value to assign for this variation. Required for
            text/number/date property types; omitted for selection types
            configured via property-value IDs instead.
    """

    variationId: Required[int]
    propertyId: Required[int]
    propertyValue: NotRequired[str]


class VariationSalesPricePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_sales_prices`
    (``PUT /rest/pim/variations/sales_prices``).

    Links a variation to a sales price *configuration* and sets its price
    *value*. See :class:`~plentymarkets._types.SalesPriceCreatePayload` for
    the configuration itself.

    Keys:
        variationId: Variation ID to set the price on. **Required.**
        salesPriceId: Sales price configuration ID (from
            ``/rest/pim/sales_prices``). **Required.**
        price: Net or gross price value, depending on the sales price
            configuration's settings. **Required.**
    """

    variationId: Required[int]
    salesPriceId: Required[int]
    price: Required[float]
```

- [ ] **Step 4: Export the four TypedDicts from `__init__.py`**

Add `VariationMarketIdentNumberPayload`, `VariationMarketPayload`, `VariationPropertyPayload`,
`VariationSalesPricePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the eight methods in `pim.py`**

Add after `delete_variation_images`:

```python
async def update_variation_market_ident_numbers(
    self,
    data: list[VariationMarketIdentNumberPayload],
) -> dict[str, Any]:
    """Bulk create or update market identifier numbers (MINs) on variations.

    Args:
        data: List of MIN payloads. Use
            :class:`~plentymarkets._types.VariationMarketIdentNumberPayload`
            for IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put(
        "/rest/pim/variations/market_ident_numbers", json=data
    )

async def delete_variation_market_ident_numbers(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation market identifier numbers by ID.

    Args:
        ids: List of MIN record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete(
        "/rest/pim/variations/market_ident_numbers", json=ids
    )

async def update_variation_markets(
    self,
    data: list[VariationMarketPayload],
) -> dict[str, Any]:
    """Bulk create market availability links on variations.

    Args:
        data: List of market availability payloads. Use
            :class:`~plentymarkets._types.VariationMarketPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/markets", json=data)

async def delete_variation_markets(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation market availability links by ID.

    Args:
        ids: List of variation-market link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/markets", json=ids)

async def update_variation_properties(
    self,
    data: list[VariationPropertyPayload],
) -> dict[str, Any]:
    """Bulk create or update item properties on variations.

    Args:
        data: List of property payloads. Use
            :class:`~plentymarkets._types.VariationPropertyPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/properties", json=data)

async def delete_variation_properties(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation properties by ID.

    Args:
        ids: List of variation-property record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/properties", json=ids)

async def update_variation_sales_prices(
    self,
    data: list[VariationSalesPricePayload],
) -> dict[str, Any]:
    """Bulk create or update sales price values on variations.

    Args:
        data: List of variation sales price payloads. Use
            :class:`~plentymarkets._types.VariationSalesPricePayload` for
            IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/sales_prices", json=data)

async def delete_variation_sales_prices(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation sales price links by ID.

    Args:
        ids: List of variation-sales-price link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/sales_prices", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.update_variation_market_ident_numbers` / `delete_variation_market_ident_numbers` — `/rest/pim/variations/market_ident_numbers`
- feat: `PimModule.update_variation_markets` / `delete_variation_markets` — `/rest/pim/variations/markets`
- feat: `PimModule.update_variation_properties` / `delete_variation_properties` — `/rest/pim/variations/properties`
- feat: `PimModule.update_variation_sales_prices` / `delete_variation_sales_prices` — `/rest/pim/variations/sales_prices`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change these four rows' Status to `**implemented**`:

```
| `/rest/pim/variations/market_ident_numbers` | PUT, DELETE | Bulk create/update/delete market identifier numbers (MINs) | **implemented** |
| `/rest/pim/variations/markets` | PUT, DELETE | Bulk create/delete market availability on variations | **implemented** |
| `/rest/pim/variations/properties` | PUT, DELETE | Bulk create/update/delete variation properties | **implemented** |
| `/rest/pim/variations/sales_prices` | PUT, DELETE | Bulk create/update/delete sales price links on variations | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add variation MIN, market, property, and sales-price bulk ops"
```

---

## Task 5: Variation bulk sub-resources — batch D (SKUs, supplier, tags, warehouses)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.put`, `_Session.delete`
- Produces:
  - `VariationSkuPayload`, `VariationSupplierPayload`, `VariationTagPayload`, `VariationWarehousePayload` TypedDicts
  - `PimModule.update_variation_skus(data)` / `delete_variation_skus(ids)`
  - `PimModule.update_variation_supplier(data)` / `delete_variation_supplier(ids)`
  - `PimModule.update_variation_tags(data)` / `delete_variation_tags(ids)`
  - `PimModule.update_variation_warehouses(data)` / `delete_variation_warehouses(ids)`

This is the last task for Group 1 (Variations). After this task, `ROADMAP.md`'s entire
Variations sub-table should read `**implemented**`.

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_update_variation_skus_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/skus",
        json={"updated": 1},
    )
    result = await pim.update_variation_skus(
        [{"variationId": 7, "marketId": 2, "sku": "MKT-SKU-1"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_skus_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/skus",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_skus([6])
    assert result["deleted"] == 1


async def test_update_variation_supplier_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/supplier",
        json={"updated": 1},
    )
    result = await pim.update_variation_supplier(
        [{"variationId": 7, "supplierId": 4, "supplierPartNumber": "SUP-9"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_supplier_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/supplier",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_supplier([4])
    assert result["deleted"] == 1


async def test_update_variation_tags_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/tags",
        json={"updated": 1},
    )
    result = await pim.update_variation_tags([{"variationId": 7, "tagId": 11}])
    assert result["updated"] == 1


async def test_delete_variation_tags_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/tags",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_tags([11])
    assert result["deleted"] == 1


async def test_update_variation_warehouses_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/warehouses",
        json={"updated": 1},
    )
    result = await pim.update_variation_warehouses(
        [{"variationId": 7, "warehouseId": 1, "stockManagementActive": True}]
    )
    assert result["updated"] == 1


async def test_delete_variation_warehouses_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/warehouses",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_warehouses([1])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "variation_skus or variation_supplier or variation_tags or variation_warehouses" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add the four TypedDicts to `_types.py`**

Append after `VariationSalesPricePayload`:

```python
class VariationSkuPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_skus`
    (``PUT /rest/pim/variations/skus``).

    Keys:
        variationId: Variation ID to set the marketplace SKU for.
            **Required.**
        marketId: Marketplace ID the SKU applies to. **Required.**
        sku: The marketplace-specific SKU string. **Required.**
    """

    variationId: Required[int]
    marketId: Required[int]
    sku: Required[str]


class VariationSupplierPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_supplier`
    (``PUT /rest/pim/variations/supplier``).

    Keys:
        variationId: Variation ID to link the supplier to. **Required.**
        supplierId: Supplier contact ID (from ``/rest/accounts/contacts``
            where the contact is flagged as a supplier). **Required.**
        supplierPartNumber: Supplier's own part number for this variation.
        priority: Preference order when a variation has multiple suppliers
            (lower = preferred).
    """

    variationId: Required[int]
    supplierId: Required[int]
    supplierPartNumber: NotRequired[str]
    priority: NotRequired[int]


class VariationTagPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_tags`
    (``PUT /rest/pim/variations/tags``).

    Keys:
        variationId: Variation ID to tag. **Required.**
        tagId: Tag ID to attach. **Required.**
    """

    variationId: Required[int]
    tagId: Required[int]


class VariationWarehousePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_warehouses`
    (``PUT /rest/pim/variations/warehouses``).

    Keys:
        variationId: Variation ID to link the warehouse to. **Required.**
        warehouseId: Warehouse ID to stock the variation in. **Required.**
        stockManagementActive: Whether stock levels for this variation are
            actively managed in this warehouse.
    """

    variationId: Required[int]
    warehouseId: Required[int]
    stockManagementActive: NotRequired[bool]
```

- [ ] **Step 4: Export the four TypedDicts from `__init__.py`**

Add `VariationSkuPayload`, `VariationSupplierPayload`, `VariationTagPayload`,
`VariationWarehousePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the eight methods in `pim.py`**

Add after `delete_variation_sales_prices`:

```python
async def update_variation_skus(
    self,
    data: list[VariationSkuPayload],
) -> dict[str, Any]:
    """Bulk create or update marketplace SKUs on variations.

    Args:
        data: List of SKU payloads. Use
            :class:`~plentymarkets._types.VariationSkuPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/skus", json=data)

async def delete_variation_skus(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation marketplace SKUs by ID.

    Args:
        ids: List of variation-SKU record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/skus", json=ids)

async def update_variation_supplier(
    self,
    data: list[VariationSupplierPayload],
) -> dict[str, Any]:
    """Bulk create or update supplier links on variations.

    Args:
        data: List of supplier link payloads. Use
            :class:`~plentymarkets._types.VariationSupplierPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/supplier", json=data)

async def delete_variation_supplier(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation supplier links by ID.

    Args:
        ids: List of variation-supplier link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/supplier", json=ids)

async def update_variation_tags(
    self,
    data: list[VariationTagPayload],
) -> dict[str, Any]:
    """Bulk create tags on variations.

    Args:
        data: List of tag payloads. Use
            :class:`~plentymarkets._types.VariationTagPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/tags", json=data)

async def delete_variation_tags(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation tags by ID.

    Args:
        ids: List of variation-tag link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/tags", json=ids)

async def update_variation_warehouses(
    self,
    data: list[VariationWarehousePayload],
) -> dict[str, Any]:
    """Bulk create or update warehouse stock links on variations.

    Args:
        data: List of warehouse link payloads. Use
            :class:`~plentymarkets._types.VariationWarehousePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/variations/warehouses", json=data)

async def delete_variation_warehouses(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete variation warehouse stock links by ID.

    Args:
        ids: List of variation-warehouse link IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/variations/warehouses", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.update_variation_skus` / `delete_variation_skus` — `/rest/pim/variations/skus`
- feat: `PimModule.update_variation_supplier` / `delete_variation_supplier` — `/rest/pim/variations/supplier`
- feat: `PimModule.update_variation_tags` / `delete_variation_tags` — `/rest/pim/variations/tags`
- feat: `PimModule.update_variation_warehouses` / `delete_variation_warehouses` — `/rest/pim/variations/warehouses`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change these four rows' Status to `**implemented**`:

```
| `/rest/pim/variations/skus` | PUT, DELETE | Bulk create/update/delete SKUs on variations | **implemented** |
| `/rest/pim/variations/supplier` | PUT, DELETE | Bulk create/update/delete supplier links on variations | **implemented** |
| `/rest/pim/variations/tags` | PUT, DELETE | Bulk create/delete tags on variations | **implemented** |
| `/rest/pim/variations/warehouses` | PUT, DELETE | Bulk create/update/delete warehouse stock links on variations | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add variation SKU, supplier, tag, and warehouse bulk ops"
```

---

## Task 6: Attributes core CRUD (create, update, delete)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `AttributeCreatePayload`, `AttributeUpdatePayload` TypedDicts
  - `PimModule.create_attributes(data) -> dict[str, Any]`
  - `PimModule.update_attributes(data) -> dict[str, Any]`
  - `PimModule.delete_attributes(ids) -> dict[str, Any]`

Request fields are confirmed directly against the OpenAPI spec (no inference caveat needed for
the payload); response shape is still unpublished, so the response caveat applies as usual.

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_create_attributes_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"created": 1},
    )
    result = await pim.create_attributes([{"backendName": "Material"}])
    assert result["created"] == 1


async def test_update_attributes_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"updated": 1},
    )
    result = await pim.update_attributes([{"id": 3, "position": 2}])
    assert result["updated"] == 1


async def test_delete_attributes_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"deleted": 1},
    )
    result = await pim.delete_attributes([3])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "create_attributes or update_attributes or delete_attributes" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add the two TypedDicts to `_types.py`**

Append after `VariationWarehousePayload`, under a new section comment:

```python
# ---------------------------------------------------------------------------
# PIM Attributes  (/rest/pim/attributes)
# ---------------------------------------------------------------------------


class AttributeCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attributes` (``POST /rest/pim/attributes``).

    Keys:
        backendName: Internal back-end name (unique, no commas, colons,
            semicolons, or quotes). **Required.**
        position: Display sort position in the attribute list.
        isSurchargePercental: Whether value surcharges are treated as a
            percentage rather than a fixed amount.
        isLinkableToImage: Whether images can be linked to attribute values.
        isGroupable: Whether attribute values can be grouped in the
            online store's filter navigation.
        amazonAttribute: Linked Amazon attribute name.
        fruugoAttribute: Linked Fruugo attribute name.
        pixmaniaAttribute: Linked Pixmania attribute ID.
        ottoAttribute: Linked Otto attribute name.
        googleShoppingAttribute: Linked Google Shopping attribute name.
        neckermannAtEpAttribute: Linked neckermann.at attribute ID.
        typeOfSelectionInOnlineStore: Selection widget type in the online
            store, e.g. ``"box"``, ``"list"``, ``"color"``, ``"image"``.
        laRedouteAttribute: Linked La Redoute attribute ID.
    """

    backendName: Required[str]
    position: NotRequired[int]
    isSurchargePercental: NotRequired[bool]
    isLinkableToImage: NotRequired[bool]
    isGroupable: NotRequired[bool]
    amazonAttribute: NotRequired[str]
    fruugoAttribute: NotRequired[str]
    pixmaniaAttribute: NotRequired[int]
    ottoAttribute: NotRequired[str]
    googleShoppingAttribute: NotRequired[str]
    neckermannAtEpAttribute: NotRequired[int]
    typeOfSelectionInOnlineStore: NotRequired[str]
    laRedouteAttribute: NotRequired[int]


class AttributeUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.update_attributes` (``PUT /rest/pim/attributes``).

    Keys:
        id: Attribute ID to update. **Required.**
        backendName: Internal back-end name (unique, no commas, colons,
            semicolons, or quotes).
        position: Display sort position in the attribute list.
        isSurchargePercental: Whether value surcharges are treated as a
            percentage rather than a fixed amount.
        isLinkableToImage: Whether images can be linked to attribute values.
        isGroupable: Whether attribute values can be grouped in the
            online store's filter navigation.
        amazonAttribute: Linked Amazon attribute name.
        fruugoAttribute: Linked Fruugo attribute name.
        pixmaniaAttribute: Linked Pixmania attribute ID.
        ottoAttribute: Linked Otto attribute name.
        googleShoppingAttribute: Linked Google Shopping attribute name.
        neckermannAtEpAttribute: Linked neckermann.at attribute ID.
        typeOfSelectionInOnlineStore: Selection widget type in the online
            store, e.g. ``"box"``, ``"list"``, ``"color"``, ``"image"``.
        laRedouteAttribute: Linked La Redoute attribute ID.
    """

    id: Required[int]
    backendName: NotRequired[str]
    position: NotRequired[int]
    isSurchargePercental: NotRequired[bool]
    isLinkableToImage: NotRequired[bool]
    isGroupable: NotRequired[bool]
    amazonAttribute: NotRequired[str]
    fruugoAttribute: NotRequired[str]
    pixmaniaAttribute: NotRequired[int]
    ottoAttribute: NotRequired[str]
    googleShoppingAttribute: NotRequired[str]
    neckermannAtEpAttribute: NotRequired[int]
    typeOfSelectionInOnlineStore: NotRequired[str]
    laRedouteAttribute: NotRequired[int]
```

- [ ] **Step 4: Export the two TypedDicts from `__init__.py`**

Add `AttributeCreatePayload`, `AttributeUpdatePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the three methods in `pim.py`**

Add after `delete_variation_warehouses`, under a new section comment (a plain Python comment,
not a docstring, matching the existing single-file style of `pim.py`):

```python
# -- Attributes -------------------------------------------------------------

async def create_attributes(
    self,
    data: list[AttributeCreatePayload],
) -> dict[str, Any]:
    """Bulk create attributes (variation axes such as colour or size).

    Args:
        data: List of attribute payloads. Use
            :class:`~plentymarkets._types.AttributeCreatePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/attributes", json=data)

async def update_attributes(
    self,
    data: list[AttributeUpdatePayload],
) -> dict[str, Any]:
    """Bulk update attributes.

    Args:
        data: List of attribute update payloads. Use
            :class:`~plentymarkets._types.AttributeUpdatePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/attributes", json=data)

async def delete_attributes(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete attributes by ID.

    Args:
        ids: List of attribute IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/attributes", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.create_attributes` — bulk create attributes via `POST /rest/pim/attributes`
- feat: `PimModule.update_attributes` — bulk update attributes via `PUT /rest/pim/attributes`
- feat: `PimModule.delete_attributes` — bulk delete attributes via `DELETE /rest/pim/attributes`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change the `/rest/pim/attributes` row's Status to `**implemented**`:

```
| `/rest/pim/attributes` | GET, PUT, POST, DELETE (all **implemented**) | Search, create, update, and delete attributes (defines variation axes like colour, size) | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add attribute create, update, and delete"
```

---

## Task 7: Attribute names CRUD

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`, `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `AttributeNamePayload` TypedDict
  - `PimModule.list_attribute_names(attribute_id, lang, name, with_) -> dict[str, Any]`
  - `PimModule.create_attribute_names(data) -> dict[str, Any]`
  - `PimModule.update_attribute_names(data) -> dict[str, Any]`
  - `PimModule.delete_attribute_names(ids) -> dict[str, Any]`

The OpenAPI spec documents the same request schema (`attributeId`, `lang`, `name`, all required)
for both `PUT` and `POST` on this endpoint — `AttributeNamePayload` is shared by
`create_attribute_names` and `update_attribute_names`.

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_attribute_names_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"entries": [{"attributeId": 3, "lang": "en", "name": "Colour"}], "totalsCount": 1},
    )
    result = await pim.list_attribute_names()
    assert result["totalsCount"] == 1


async def test_list_attribute_names_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/names?attributeId=3&lang=en",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_attribute_names(attribute_id=3, lang="en")
    assert result["totalsCount"] == 0


async def test_create_attribute_names_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"created": 1},
    )
    result = await pim.create_attribute_names(
        [{"attributeId": 3, "lang": "en", "name": "Colour"}]
    )
    assert result["created"] == 1


async def test_update_attribute_names_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"updated": 1},
    )
    result = await pim.update_attribute_names(
        [{"attributeId": 3, "lang": "en", "name": "Color"}]
    )
    assert result["updated"] == 1


async def test_delete_attribute_names_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"deleted": 1},
    )
    result = await pim.delete_attribute_names([9])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "attribute_names" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add `AttributeNamePayload` to `_types.py`**

Append after `AttributeUpdatePayload`:

```python
class AttributeNamePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attribute_names` and
    :meth:`PimModule.update_attribute_names`
    (``POST``/``PUT /rest/pim/attributes/names``).

    Keys:
        attributeId: Attribute ID the name belongs to. **Required.**
        lang: Two-letter language code, e.g. ``"en"``, ``"de"``.
            **Required.**
        name: Display name shown in the back end and online store for this
            language. **Required.**
    """

    attributeId: Required[int]
    lang: Required[str]
    name: Required[str]
```

- [ ] **Step 4: Export `AttributeNamePayload` from `__init__.py`**

Add `AttributeNamePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the four methods in `pim.py`**

Add after `delete_attributes`:

```python
async def list_attribute_names(
    self,
    attribute_id: int | None = None,
    lang: str | None = None,
    name: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search multilingual attribute display names.

    Args:
        attribute_id: Restrict results to names belonging to this
            attribute ID.
        lang: Restrict results to this two-letter language code.
        name: Restrict results to names containing this string.
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched name records, each with
          ``attributeId``, ``lang``, and ``name``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if attribute_id is not None:
        filters["attributeId"] = attribute_id
    if lang is not None:
        filters["lang"] = lang
    if name is not None:
        filters["name"] = name
    params = self._build_params(filters or None, with_)
    return await self._session.get("/rest/pim/attributes/names", params=params or None)

async def create_attribute_names(
    self,
    data: list[AttributeNamePayload],
) -> dict[str, Any]:
    """Bulk create multilingual attribute display names.

    Args:
        data: List of name payloads. Use
            :class:`~plentymarkets._types.AttributeNamePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/attributes/names", json=data)

async def update_attribute_names(
    self,
    data: list[AttributeNamePayload],
) -> dict[str, Any]:
    """Bulk update multilingual attribute display names.

    Args:
        data: List of name payloads. Use
            :class:`~plentymarkets._types.AttributeNamePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/attributes/names", json=data)

async def delete_attribute_names(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete attribute names by ID.

    Args:
        ids: List of attribute-name record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/attributes/names", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_attribute_names` — search attribute names via `GET /rest/pim/attributes/names`
- feat: `PimModule.create_attribute_names` — bulk create attribute names via `POST /rest/pim/attributes/names`
- feat: `PimModule.update_attribute_names` — bulk update attribute names via `PUT /rest/pim/attributes/names`
- feat: `PimModule.delete_attribute_names` — bulk delete attribute names via `DELETE /rest/pim/attributes/names`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change the `/rest/pim/attributes/names` row's Status to `**implemented**`:

```
| `/rest/pim/attributes/names` | GET, PUT, POST, DELETE (all **implemented**) | Manage multilingual attribute display names | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add attribute name list, create, update, and delete"
```

---

## Task 8: Attribute values CRUD + get one

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`, `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `AttributeValuePayload` TypedDict (inferred — spec publishes no request schema for this endpoint)
  - `PimModule.list_attribute_values(ids, attribute_id, backend_name, name, with_) -> dict[str, Any]`
  - `PimModule.create_attribute_values(data) -> dict[str, Any]`
  - `PimModule.update_attribute_values(data) -> dict[str, Any]`
  - `PimModule.delete_attribute_values(ids) -> dict[str, Any]`
  - `PimModule.get_attribute_value(value_id) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_attribute_values_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"entries": [{"id": 10, "attributeId": 3, "backendName": "Red"}], "totalsCount": 1},
    )
    result = await pim.list_attribute_values()
    assert result["totalsCount"] == 1


async def test_list_attribute_values_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values?attributeId=3",
        json={"entries": [{"id": 10}], "totalsCount": 1},
    )
    result = await pim.list_attribute_values(attribute_id=3)
    assert result["entries"][0]["id"] == 10


async def test_create_attribute_values_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"created": 1},
    )
    result = await pim.create_attribute_values(
        [{"attributeId": 3, "backendName": "Red", "position": 1}]
    )
    assert result["created"] == 1


async def test_update_attribute_values_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"updated": 1},
    )
    result = await pim.update_attribute_values([{"id": 10, "position": 2}])
    assert result["updated"] == 1


async def test_delete_attribute_values_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"deleted": 1},
    )
    result = await pim.delete_attribute_values([10])
    assert result["deleted"] == 1


async def test_get_attribute_value(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values/10",
        json={"id": 10, "attributeId": 3, "backendName": "Red"},
    )
    result = await pim.get_attribute_value(10)
    assert result["backendName"] == "Red"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "attribute_value" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add `AttributeValuePayload` to `_types.py`**

Append after `AttributeNamePayload`:

```python
class AttributeValuePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attribute_values` and
    :meth:`PimModule.update_attribute_values`
    (``POST``/``PUT /rest/pim/attributes/values``).

    PlentyMarkets does not publish a request schema for this endpoint; keys
    are inferred from the ``GET`` search parameters and general attribute
    conventions. Verify against a live system before relying on optional
    keys.

    Keys:
        id: Attribute value ID, required when updating an existing value.
        attributeId: Attribute ID this value belongs to. **Required.**
        backendName: Internal back-end name for this value (e.g. ``"Red"``
            for a colour attribute). **Required.**
        position: Display sort position among the attribute's values.
        image: Path or URL of an image representing this value, used when
            the attribute's ``typeOfSelectionInOnlineStore`` is
            ``"image"`` or ``"color"``.
    """

    id: NotRequired[int]
    attributeId: Required[int]
    backendName: Required[str]
    position: NotRequired[int]
    image: NotRequired[str]
```

- [ ] **Step 4: Export `AttributeValuePayload` from `__init__.py`**

Add `AttributeValuePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the five methods in `pim.py`**

Add after `delete_attribute_names`:

```python
async def list_attribute_values(
    self,
    ids: list[int] | None = None,
    attribute_id: int | None = None,
    backend_name: str | None = None,
    name: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search attribute values (e.g. "Red", "Blue" for a colour attribute).

    Args:
        ids: Restrict results to attribute values with these IDs.
        attribute_id: Restrict results to values belonging to this
            attribute ID.
        backend_name: Restrict results to this exact back-end name.
        name: Restrict results to values whose display name contains this
            string.
        with_: Optional list of related data to embed. Accepted values:
            ``"names"`` (multilingual display names).

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched value records, each with at
          minimum ``id``, ``attributeId``, and ``backendName``.
        - ``totalsCount`` (int): Total number of matching values.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if ids is not None:
        filters["ids"] = ",".join(str(i) for i in ids)
    if attribute_id is not None:
        filters["attributeId"] = attribute_id
    if backend_name is not None:
        filters["backendName"] = backend_name
    if name is not None:
        filters["name"] = name
    params = self._build_params(filters or None, with_)
    return await self._session.get("/rest/pim/attributes/values", params=params or None)

async def create_attribute_values(
    self,
    data: list[AttributeValuePayload],
) -> dict[str, Any]:
    """Bulk create attribute values.

    Args:
        data: List of attribute value payloads. Use
            :class:`~plentymarkets._types.AttributeValuePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/attributes/values", json=data)

async def update_attribute_values(
    self,
    data: list[AttributeValuePayload],
) -> dict[str, Any]:
    """Bulk update attribute values.

    Args:
        data: List of attribute value payloads. Use
            :class:`~plentymarkets._types.AttributeValuePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/attributes/values", json=data)

async def delete_attribute_values(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete attribute values by ID.

    Args:
        ids: List of attribute value IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/attributes/values", json=ids)

async def get_attribute_value(self, value_id: int) -> dict[str, Any]:
    """Get a single attribute value by ID.

    Args:
        value_id: The PlentyMarkets attribute value ID.

    Returns:
        A dict with the following keys (based on the fields exposed by
        :meth:`list_attribute_values`; PlentyMarkets does not publish a
        fixed schema for this endpoint — verify against a live system):

        - ``id`` (int): The attribute value ID.
        - ``attributeId`` (int): The parent attribute ID.
        - ``backendName`` (str): Internal back-end name for this value.
        - ``position`` (int): Display sort position among the attribute's
          values.
        - ``image`` (str | None): Linked image path or URL, if any.
    """
    return await self._session.get(f"/rest/pim/attributes/values/{value_id}")
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_attribute_values` — search attribute values via `GET /rest/pim/attributes/values`
- feat: `PimModule.create_attribute_values` — bulk create attribute values via `POST /rest/pim/attributes/values`
- feat: `PimModule.update_attribute_values` — bulk update attribute values via `PUT /rest/pim/attributes/values`
- feat: `PimModule.delete_attribute_values` — bulk delete attribute values via `DELETE /rest/pim/attributes/values`
- feat: `PimModule.get_attribute_value` — get one attribute value via `GET /rest/pim/attributes/values/{id}`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change these two rows' Status to `**implemented**`:

```
| `/rest/pim/attributes/values` | GET, PUT, POST, DELETE (all **implemented**) | Manage attribute values (e.g. "Red", "Blue" for a colour attribute) | **implemented** |
| `/rest/pim/attributes/values/{id}` | GET | Get one attribute value by ID | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add attribute value list, create, update, delete, and get"
```

---

## Task 9: Attribute value names CRUD

This is the last task for Group 2 (Attributes). After this task, `ROADMAP.md`'s entire
Attributes sub-table should read `**implemented**`.

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`, `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `AttributeValueNamePayload` TypedDict
  - `PimModule.list_attribute_value_names(value_id, lang, name, with_) -> dict[str, Any]`
  - `PimModule.create_attribute_value_names(data) -> dict[str, Any]`
  - `PimModule.update_attribute_value_names(data) -> dict[str, Any]`
  - `PimModule.delete_attribute_value_names(ids) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_attribute_value_names_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"entries": [{"valueId": 10, "lang": "en", "name": "Red"}], "totalsCount": 1},
    )
    result = await pim.list_attribute_value_names()
    assert result["totalsCount"] == 1


async def test_list_attribute_value_names_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values/names?valueId=10&lang=en",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_attribute_value_names(value_id=10, lang="en")
    assert result["totalsCount"] == 0


async def test_create_attribute_value_names_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"created": 1},
    )
    result = await pim.create_attribute_value_names(
        [{"valueId": 10, "lang": "en", "name": "Red"}]
    )
    assert result["created"] == 1


async def test_update_attribute_value_names_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"updated": 1},
    )
    result = await pim.update_attribute_value_names(
        [{"valueId": 10, "lang": "en", "name": "Crimson"}]
    )
    assert result["updated"] == 1


async def test_delete_attribute_value_names_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"deleted": 1},
    )
    result = await pim.delete_attribute_value_names([21])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "attribute_value_names" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add `AttributeValueNamePayload` to `_types.py`**

Append after `AttributeValuePayload`:

```python
class AttributeValueNamePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attribute_value_names` and
    :meth:`PimModule.update_attribute_value_names`
    (``POST``/``PUT /rest/pim/attributes/values/names``).

    Keys:
        valueId: Attribute value ID the name belongs to. **Required.**
        lang: Two-letter language code, e.g. ``"en"``, ``"de"``.
            **Required.**
        name: Display name shown in the back end and online store for this
            language. **Required.**
    """

    valueId: Required[int]
    lang: Required[str]
    name: Required[str]
```

- [ ] **Step 4: Export `AttributeValueNamePayload` from `__init__.py`**

Add `AttributeValueNamePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the four methods in `pim.py`**

Add after `get_attribute_value`:

```python
async def list_attribute_value_names(
    self,
    value_id: int | None = None,
    lang: str | None = None,
    name: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search multilingual display names for attribute values.

    Args:
        value_id: Restrict results to names belonging to this attribute
            value ID.
        lang: Restrict results to this two-letter language code.
        name: Restrict results to names containing this string.
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched name records, each with
          ``valueId``, ``lang``, and ``name``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if value_id is not None:
        filters["valueId"] = value_id
    if lang is not None:
        filters["lang"] = lang
    if name is not None:
        filters["name"] = name
    params = self._build_params(filters or None, with_)
    return await self._session.get(
        "/rest/pim/attributes/values/names", params=params or None
    )

async def create_attribute_value_names(
    self,
    data: list[AttributeValueNamePayload],
) -> dict[str, Any]:
    """Bulk create multilingual display names for attribute values.

    Args:
        data: List of name payloads. Use
            :class:`~plentymarkets._types.AttributeValueNamePayload` for
            IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/attributes/values/names", json=data)

async def update_attribute_value_names(
    self,
    data: list[AttributeValueNamePayload],
) -> dict[str, Any]:
    """Bulk update multilingual display names for attribute values.

    Args:
        data: List of name payloads. Use
            :class:`~plentymarkets._types.AttributeValueNamePayload` for
            IDE autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/attributes/values/names", json=data)

async def delete_attribute_value_names(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete attribute value names by ID.

    Args:
        ids: List of attribute-value-name record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete(
        "/rest/pim/attributes/values/names", json=ids
    )
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_attribute_value_names` — search attribute value names via `GET /rest/pim/attributes/values/names`
- feat: `PimModule.create_attribute_value_names` — bulk create attribute value names via `POST /rest/pim/attributes/values/names`
- feat: `PimModule.update_attribute_value_names` — bulk update attribute value names via `PUT /rest/pim/attributes/values/names`
- feat: `PimModule.delete_attribute_value_names` — bulk delete attribute value names via `DELETE /rest/pim/attributes/values/names`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change the `/rest/pim/attributes/values/names` row's Status to `**implemented**`:

```
| `/rest/pim/attributes/values/names` | GET, PUT, POST, DELETE (all **implemented**) | Manage multilingual display names for attribute values | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add attribute value name list, create, update, and delete"
```

---

## Task 10: Category detail lookups (Group 3 — read-only, no TypedDicts)

**Files:**
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`
- Produces:
  - `PimModule.list_category_branches(with_) -> dict[str, Any]`
  - `PimModule.list_category_clients(category_id, plenty_id, with_) -> dict[str, Any]`
  - `PimModule.list_category_details(category_id, plenty_id, lang, name, name_url, meta_keywords, with_) -> dict[str, Any]`
  - `PimModule.list_category_properties(category_id, plenty_id, value, with_) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_category_branches(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/branches",
        json={"entries": [{"categoryId": 5, "branch": [1, 2, 5]}], "totalsCount": 1},
    )
    result = await pim.list_category_branches()
    assert result["totalsCount"] == 1


async def test_list_category_clients(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/clients?categoryId=5&plentyId=1",
        json={"entries": [{"categoryId": 5, "plentyId": 1}], "totalsCount": 1},
    )
    result = await pim.list_category_clients(category_id=5, plenty_id=1)
    assert result["totalsCount"] == 1


async def test_list_category_details(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/details?categoryId=5&lang=en",
        json={"entries": [{"categoryId": 5, "lang": "en", "name": "Shoes"}], "totalsCount": 1},
    )
    result = await pim.list_category_details(category_id=5, lang="en")
    assert result["entries"][0]["name"] == "Shoes"


async def test_list_category_properties(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/properties?categoryId=5",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_category_properties(category_id=5)
    assert result["totalsCount"] == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "category_branches or category_clients or category_details or category_properties" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Implement the four methods in `pim.py`**

Add after `get_category` (in the existing Categories section):

```python
async def list_category_branches(
    self,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search category branches (full path from root to leaf).

    Args:
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched branch records, each with at
          minimum ``categoryId`` and ``branch`` (list[int] of ancestor
          category IDs from root to the category itself).
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    params = self._build_params(None, with_)
    return await self._session.get(
        "/rest/pim/categories/branches", params=params or None
    )

async def list_category_clients(
    self,
    category_id: int | None = None,
    plenty_id: int | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search which clients (stores) have each category active.

    Args:
        category_id: Restrict results to this category ID.
        plenty_id: Restrict results to this client (store) ID.
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched records, each with
          ``categoryId`` and ``plentyId``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if category_id is not None:
        filters["categoryId"] = category_id
    if plenty_id is not None:
        filters["plentyId"] = plenty_id
    params = self._build_params(filters or None, with_)
    return await self._session.get(
        "/rest/pim/categories/clients", params=params or None
    )

async def list_category_details(
    self,
    category_id: int | None = None,
    plenty_id: int | None = None,
    lang: str | None = None,
    name: str | None = None,
    name_url: str | None = None,
    meta_keywords: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search category detail records (multilingual names, descriptions, meta data).

    Args:
        category_id: Restrict results to this category ID.
        plenty_id: Restrict results to this client (store) ID.
        lang: Restrict results to this two-letter language code.
        name: Restrict results to details whose name contains this string.
        name_url: Restrict results to details whose URL slug contains this
            string.
        meta_keywords: Restrict results to details whose meta keywords
            contain this string.
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched detail records, each with at
          minimum ``categoryId``, ``lang``, and ``name``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if category_id is not None:
        filters["categoryId"] = category_id
    if plenty_id is not None:
        filters["plentyId"] = plenty_id
    if lang is not None:
        filters["lang"] = lang
    if name is not None:
        filters["name"] = name
    if name_url is not None:
        filters["nameUrl"] = name_url
    if meta_keywords is not None:
        filters["metaKeywords"] = meta_keywords
    params = self._build_params(filters or None, with_)
    return await self._session.get(
        "/rest/pim/categories/details", params=params or None
    )

async def list_category_properties(
    self,
    category_id: int | None = None,
    plenty_id: int | None = None,
    value: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search category property links.

    Args:
        category_id: Restrict results to this category ID.
        plenty_id: Restrict results to this client (store) ID.
        value: Restrict results to properties with this value.
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched property link records, each
          with at minimum ``categoryId`` and ``value``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if category_id is not None:
        filters["categoryId"] = category_id
    if plenty_id is not None:
        filters["plentyId"] = plenty_id
    if value is not None:
        filters["value"] = value
    params = self._build_params(filters or None, with_)
    return await self._session.get(
        "/rest/pim/categories/properties", params=params or None
    )
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 5: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_category_branches` — search category branches via `GET /rest/pim/categories/branches`
- feat: `PimModule.list_category_clients` — search category client visibility via `GET /rest/pim/categories/clients`
- feat: `PimModule.list_category_details` — search category detail records via `GET /rest/pim/categories/details`
- feat: `PimModule.list_category_properties` — search category property links via `GET /rest/pim/categories/properties`
```

- [ ] **Step 6: Update `ROADMAP.md`**

Change these four rows' Status to `**implemented**`. After this task, `ROADMAP.md`'s entire
Categories sub-table should read `**implemented**`:

```
| `/rest/pim/categories/branches` | GET | Search category branches (full path from root to leaf) | **implemented** |
| `/rest/pim/categories/clients` | GET | Search which clients (stores) have each category active | **implemented** |
| `/rest/pim/categories/details` | GET | Search category detail records (multilingual names, descriptions, meta data) | **implemented** |
| `/rest/pim/categories/properties` | GET | Search category property links | **implemented** |
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add category branch, client, detail, and property lookups"
```

---

## Task 11: Sales price writes (Group 4)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `SalesPriceCreatePayload`, `SalesPriceUpdatePayload` TypedDicts
  - `PimModule.create_sales_prices(data) -> dict[str, Any]`
  - `PimModule.update_sales_prices(data) -> dict[str, Any]`
  - `PimModule.delete_sales_prices(ids) -> dict[str, Any]`

The spec confirms top-level fields (`position`, `minimumOrderQuantity`, `type`,
`isCustomerPrice`, `isDisplayedByDefault`, `isLiveConversion`, `interval`, `names`, `countries`,
`currencies`, `customerClasses`, `referrers`, `clients`, `accounts`) but its nested-array item
shapes are not cleanly separated in the OpenAPI document (likely a spec-authoring artifact from
merged sub-schemas), so nested list items are typed as `list[dict[str, Any]]` with the expected
inner keys documented in prose rather than as separate TypedDicts. The spec's `DELETE` operation
reuses the full `PUT` request schema — per the design spec, `delete_sales_prices` is treated as
`ids: list[int]` per the general bulk-delete convention instead.

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_create_sales_prices_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"created": 1},
    )
    result = await pim.create_sales_prices(
        [{"type": "specialOffer", "position": 3, "isCustomerPrice": False}]
    )
    assert result["created"] == 1


async def test_update_sales_prices_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"updated": 1},
    )
    result = await pim.update_sales_prices([{"id": 1, "position": 2}])
    assert result["updated"] == 1


async def test_delete_sales_prices_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"deleted": 1},
    )
    result = await pim.delete_sales_prices([1])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "create_sales_prices or update_sales_prices or delete_sales_prices" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add the two TypedDicts to `_types.py`**

Append after `AttributeValueNamePayload`, under a new section comment:

```python
# ---------------------------------------------------------------------------
# PIM Sales Prices  (/rest/pim/sales_prices)
# ---------------------------------------------------------------------------


class SalesPriceCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_sales_prices` (``POST /rest/pim/sales_prices``).

    Keys:
        type: Price type. Common values: ``"default"``, ``"rrp"``,
            ``"specialOffer"``, ``"setPrice"``. **Required.**
        position: Display sort position.
        minimumOrderQuantity: Minimum quantity for this price to apply.
        isCustomerPrice: Whether the price is customer-class specific.
        isDisplayedByDefault: Whether this price is shown by default in
            the online store.
        isLiveConversion: Whether to apply live FX conversion.
        interval: Interval this price applies over, e.g. ``"weekly"``.
        names: List of multilingual name dicts, each with ``lang``,
            ``nameInternal``, and ``nameExternal``.
        countries: List of dicts restricting the price to specific
            countries, each with ``countryId``.
        currencies: List of dicts declaring supported currencies, each
            with ``currency`` (ISO 4217 code, e.g. ``"EUR"``).
        customerClasses: List of dicts restricting the price to specific
            customer classes, each with ``customerClassId``.
        referrers: List of dicts restricting the price to specific
            referrers, each with ``referrerId``.
        clients: List of dicts restricting the price to specific clients
            (stores), each with ``plentyId``.
        accounts: List of dicts linking the price to specific accounts,
            each with ``accountId``.
    """

    type: Required[str]
    position: NotRequired[int]
    minimumOrderQuantity: NotRequired[float]
    isCustomerPrice: NotRequired[bool]
    isDisplayedByDefault: NotRequired[bool]
    isLiveConversion: NotRequired[bool]
    interval: NotRequired[str]
    names: NotRequired[list[dict[str, Any]]]
    countries: NotRequired[list[dict[str, Any]]]
    currencies: NotRequired[list[dict[str, Any]]]
    customerClasses: NotRequired[list[dict[str, Any]]]
    referrers: NotRequired[list[dict[str, Any]]]
    clients: NotRequired[list[dict[str, Any]]]
    accounts: NotRequired[list[dict[str, Any]]]


class SalesPriceUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.update_sales_prices` (``PUT /rest/pim/sales_prices``).

    Keys:
        id: Sales price configuration ID to update. **Required.**
        type: Price type. Common values: ``"default"``, ``"rrp"``,
            ``"specialOffer"``, ``"setPrice"``.
        position: Display sort position.
        minimumOrderQuantity: Minimum quantity for this price to apply.
        isCustomerPrice: Whether the price is customer-class specific.
        isDisplayedByDefault: Whether this price is shown by default in
            the online store.
        isLiveConversion: Whether to apply live FX conversion.
        interval: Interval this price applies over, e.g. ``"weekly"``.
        names: List of multilingual name dicts, each with ``lang``,
            ``nameInternal``, and ``nameExternal``.
        countries: List of dicts restricting the price to specific
            countries, each with ``countryId``.
        currencies: List of dicts declaring supported currencies, each
            with ``currency`` (ISO 4217 code, e.g. ``"EUR"``).
        customerClasses: List of dicts restricting the price to specific
            customer classes, each with ``customerClassId``.
        referrers: List of dicts restricting the price to specific
            referrers, each with ``referrerId``.
        clients: List of dicts restricting the price to specific clients
            (stores), each with ``plentyId``.
        accounts: List of dicts linking the price to specific accounts,
            each with ``accountId``.
    """

    id: Required[int]
    type: NotRequired[str]
    position: NotRequired[int]
    minimumOrderQuantity: NotRequired[float]
    isCustomerPrice: NotRequired[bool]
    isDisplayedByDefault: NotRequired[bool]
    isLiveConversion: NotRequired[bool]
    interval: NotRequired[str]
    names: NotRequired[list[dict[str, Any]]]
    countries: NotRequired[list[dict[str, Any]]]
    currencies: NotRequired[list[dict[str, Any]]]
    customerClasses: NotRequired[list[dict[str, Any]]]
    referrers: NotRequired[list[dict[str, Any]]]
    clients: NotRequired[list[dict[str, Any]]]
    accounts: NotRequired[list[dict[str, Any]]]
```

- [ ] **Step 4: Export the two TypedDicts from `__init__.py`**

Add `SalesPriceCreatePayload`, `SalesPriceUpdatePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the three methods in `pim.py`**

Add after `get_sales_price`:

```python
async def create_sales_prices(
    self,
    data: list[SalesPriceCreatePayload],
) -> dict[str, Any]:
    """Bulk create sales price configurations.

    Args:
        data: List of sales price payloads. Use
            :class:`~plentymarkets._types.SalesPriceCreatePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/sales_prices", json=data)

async def update_sales_prices(
    self,
    data: list[SalesPriceUpdatePayload],
) -> dict[str, Any]:
    """Bulk update sales price configurations.

    Args:
        data: List of sales price update payloads. Use
            :class:`~plentymarkets._types.SalesPriceUpdatePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/sales_prices", json=data)

async def delete_sales_prices(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete sales price configurations by ID.

    Args:
        ids: List of sales price configuration IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/sales_prices", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.create_sales_prices` — bulk create sales price configurations via `POST /rest/pim/sales_prices`
- feat: `PimModule.update_sales_prices` — bulk update sales price configurations via `PUT /rest/pim/sales_prices`
- feat: `PimModule.delete_sales_prices` — bulk delete sales price configurations via `DELETE /rest/pim/sales_prices`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change the `/rest/pim/sales_prices` row's Status to `**implemented**`. After this task,
`ROADMAP.md`'s entire Sales Prices sub-table should read `**implemented**`:

```
| `/rest/pim/sales_prices` | GET, PUT, POST, DELETE (all **implemented**) | Search, create, update, and delete sales price configurations | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add sales price create, update, and delete"
```

---

## Task 12: Barcodes config (Group 5)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`, `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `BarcodeCreatePayload`, `BarcodeUpdatePayload` TypedDicts
  - `PimModule.list_barcodes(ids, code, type_, referrer_ids, with_) -> dict[str, Any]`
  - `PimModule.create_barcodes(data) -> dict[str, Any]`
  - `PimModule.update_barcodes(data) -> dict[str, Any]`
  - `PimModule.delete_barcodes(ids) -> dict[str, Any]`
  - `PimModule.list_barcode_duplicates() -> dict[str, Any]`
  - `PimModule.count_barcode_duplicates() -> dict[str, Any]`
  - `PimModule.get_barcode_duplicate_settings() -> dict[str, Any]`

Note: these are barcode *type configurations* (`/rest/pim/barcodes`), distinct from the
variation-to-barcode links added in Task 2 (`/rest/pim/variations/barcodes`, which references a
barcode configuration's `id` via `barcodeId`).

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_barcodes_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"entries": [{"id": 1, "type": "EAN13"}], "totalsCount": 1},
    )
    result = await pim.list_barcodes()
    assert result["totalsCount"] == 1


async def test_list_barcodes_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes?type=EAN13",
        json={"entries": [{"id": 1, "type": "EAN13"}], "totalsCount": 1},
    )
    result = await pim.list_barcodes(type_="EAN13")
    assert result["entries"][0]["id"] == 1


async def test_create_barcodes_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"created": 1},
    )
    result = await pim.create_barcodes([{"name": "EAN-13", "type": "EAN13"}])
    assert result["created"] == 1


async def test_update_barcodes_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"updated": 1},
    )
    result = await pim.update_barcodes([{"id": 1, "name": "EAN-13 (updated)"}])
    assert result["updated"] == 1


async def test_delete_barcodes_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"deleted": 1},
    )
    result = await pim.delete_barcodes([1])
    assert result["deleted"] == 1


async def test_list_barcode_duplicates(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes/duplicates",
        json={"entries": {"4006381333931": [10, 11]}},
    )
    result = await pim.list_barcode_duplicates()
    assert "4006381333931" in result["entries"]


async def test_count_barcode_duplicates(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes/duplicates/count",
        json={"count": 2},
    )
    result = await pim.count_barcode_duplicates()
    assert result["count"] == 2


async def test_get_barcode_duplicate_settings(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes/duplicates/settings",
        json=[{"barcodeType": "EAN13", "checkForDuplicates": True}],
    )
    result = await pim.get_barcode_duplicate_settings()
    assert result[0]["barcodeType"] == "EAN13"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "barcodes" -v`
Expected: `AttributeError` for each missing method (existing `test_update_variation_barcodes_puts_data`
etc. from Task 2 continue to pass — this filter also matches those, which is fine).

- [ ] **Step 3: Add the two TypedDicts to `_types.py`**

Append after `SalesPriceUpdatePayload`, under a new section comment:

```python
# ---------------------------------------------------------------------------
# PIM Barcodes  (/rest/pim/barcodes)
# ---------------------------------------------------------------------------


class BarcodeCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_barcodes` (``POST /rest/pim/barcodes``).

    Keys:
        name: Display name for the barcode type. **Required.**
        type: Barcode symbology/type, e.g. ``"EAN13"``, ``"EAN8"``,
            ``"CODE128"``, ``"GTIN"``. **Required.**
        referrers: List of referrer restriction dicts, each with
            ``referrerId`` (float — the spec declares this field as a
            number rather than an integer).
    """

    name: Required[str]
    type: Required[str]
    referrers: NotRequired[list[dict[str, Any]]]


class BarcodeUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.update_barcodes` (``PUT /rest/pim/barcodes``).

    Keys:
        id: Barcode configuration ID to update. **Required.**
        name: Display name for the barcode type.
        type: Barcode symbology/type, e.g. ``"EAN13"``, ``"EAN8"``,
            ``"CODE128"``, ``"GTIN"``.
        referrers: List of referrer restriction dicts, each with
            ``referrerId`` (float — the spec declares this field as a
            number rather than an integer).
    """

    id: Required[int]
    name: NotRequired[str]
    type: NotRequired[str]
    referrers: NotRequired[list[dict[str, Any]]]
```

- [ ] **Step 4: Export the two TypedDicts from `__init__.py`**

Add `BarcodeCreatePayload`, `BarcodeUpdatePayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the seven methods in `pim.py`**

Add after `delete_sales_prices`, under a new section comment:

```python
# -- Barcodes -----------------------------------------------------------

async def list_barcodes(
    self,
    ids: list[int] | None = None,
    code: str | None = None,
    type_: str | None = None,
    referrer_ids: list[int] | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search barcode type configurations.

    Args:
        ids: Restrict results to barcode configurations with these IDs.
        code: Restrict results to this exact barcode code value.
        type_: Restrict results to this barcode symbology/type, e.g.
            ``"EAN13"``.
        referrer_ids: Restrict results to configurations linked to any of
            these referrer IDs.
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched barcode configuration records,
          each with at minimum ``id``, ``name``, and ``type``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if ids is not None:
        filters["ids"] = ",".join(str(i) for i in ids)
    if code is not None:
        filters["code"] = code
    if type_ is not None:
        filters["type"] = type_
    if referrer_ids is not None:
        filters["referrerIds"] = ",".join(str(i) for i in referrer_ids)
    params = self._build_params(filters or None, with_)
    return await self._session.get("/rest/pim/barcodes", params=params or None)

async def create_barcodes(
    self,
    data: list[BarcodeCreatePayload],
) -> dict[str, Any]:
    """Bulk create barcode type configurations.

    Args:
        data: List of barcode payloads. Use
            :class:`~plentymarkets._types.BarcodeCreatePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/barcodes", json=data)

async def update_barcodes(
    self,
    data: list[BarcodeUpdatePayload],
) -> dict[str, Any]:
    """Bulk update barcode type configurations.

    Args:
        data: List of barcode update payloads. Use
            :class:`~plentymarkets._types.BarcodeUpdatePayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/barcodes", json=data)

async def delete_barcodes(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete barcode type configurations by ID.

    Args:
        ids: List of barcode configuration IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/barcodes", json=ids)

async def list_barcode_duplicates(self) -> dict[str, Any]:
    """List all variations that share a duplicate barcode value.

    Returns:
        A dict with the following keys (PlentyMarkets does not publish a
        fixed schema for this endpoint; verify against a live system):

        - ``entries``: Duplicate groups, keyed by barcode value, each
          mapping to a list of variation IDs sharing that value.
    """
    return await self._session.get("/rest/pim/barcodes/duplicates")

async def count_barcode_duplicates(self) -> dict[str, Any]:
    """Count of duplicate barcodes across the catalogue.

    Returns:
        A dict with the following keys (PlentyMarkets does not publish a
        fixed schema for this endpoint; verify against a live system):

        - ``count`` (int): Number of barcode values that appear on more
          than one variation.
    """
    return await self._session.get("/rest/pim/barcodes/duplicates/count")

async def get_barcode_duplicate_settings(self) -> dict[str, Any]:
    """Get settings controlling barcode duplicate detection behaviour.

    Returns:
        The raw response as returned by the API. The OpenAPI spec
        documents this endpoint's response as a JSON array (not the usual
        ``entries``-wrapped envelope), so despite the ``dict`` type hint
        shared by every method on this class, callers should expect a
        ``list[dict]`` at runtime — each dict describing one barcode
        type's duplicate-detection configuration (e.g. ``barcodeType`` and
        ``checkForDuplicates``). Verify against a live system.
    """
    return await self._session.get("/rest/pim/barcodes/duplicates/settings")
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_barcodes` — search barcode configurations via `GET /rest/pim/barcodes`
- feat: `PimModule.create_barcodes` — bulk create barcode configurations via `POST /rest/pim/barcodes`
- feat: `PimModule.update_barcodes` — bulk update barcode configurations via `PUT /rest/pim/barcodes`
- feat: `PimModule.delete_barcodes` — bulk delete barcode configurations via `DELETE /rest/pim/barcodes`
- feat: `PimModule.list_barcode_duplicates` — list duplicate barcodes via `GET /rest/pim/barcodes/duplicates`
- feat: `PimModule.count_barcode_duplicates` — count duplicate barcodes via `GET /rest/pim/barcodes/duplicates/count`
- feat: `PimModule.get_barcode_duplicate_settings` — get duplicate-detection settings via `GET /rest/pim/barcodes/duplicates/settings`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change these four rows' Status to `**implemented**`. After this task, `ROADMAP.md`'s entire
Barcodes sub-table should read `**implemented**`:

```
| `/rest/pim/barcodes` | GET, PUT, POST, DELETE (all **implemented**) | Search, create, update, and delete barcode type configurations | **implemented** |
| `/rest/pim/barcodes/duplicates` | GET | List all variations that share a duplicate barcode value | **implemented** |
| `/rest/pim/barcodes/duplicates/count` | GET | Count of duplicate barcodes across the catalogue | **implemented** |
| `/rest/pim/barcodes/duplicates/settings` | GET | Settings controlling barcode duplicate detection behaviour | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add barcode config CRUD and duplicate lookups"
```

---

## Task 13: Item serial numbers (Group 6)

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`, `_Session.put`, `_Session.post`, `_Session.delete`
- Produces:
  - `ItemSerialNumberPayload` TypedDict
  - `PimModule.list_item_serial_numbers(with_) -> dict[str, Any]`
  - `PimModule.create_item_serial_numbers(data) -> dict[str, Any]`
  - `PimModule.update_item_serial_numbers(data) -> dict[str, Any]`
  - `PimModule.delete_item_serial_numbers(ids) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_item_serial_numbers(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"entries": [{"id": 1, "itemId": 42, "serialNumber": "SN-001"}], "totalsCount": 1},
    )
    result = await pim.list_item_serial_numbers()
    assert result["totalsCount"] == 1


async def test_create_item_serial_numbers_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"created": 1},
    )
    result = await pim.create_item_serial_numbers(
        [{"itemId": 42, "serialNumber": "SN-002"}]
    )
    assert result["created"] == 1


async def test_update_item_serial_numbers_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"updated": 1},
    )
    result = await pim.update_item_serial_numbers(
        [{"itemId": 42, "serialNumber": "SN-002", "orderId": 100}]
    )
    assert result["updated"] == 1


async def test_delete_item_serial_numbers_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"deleted": 1},
    )
    result = await pim.delete_item_serial_numbers([1])
    assert result["deleted"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "item_serial_numbers" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Add `ItemSerialNumberPayload` to `_types.py`**

Append after `BarcodeUpdatePayload`, under a new section comment:

```python
# ---------------------------------------------------------------------------
# PIM Item Serial Numbers  (/rest/pim/item-serial-numbers)
# ---------------------------------------------------------------------------


class ItemSerialNumberPayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_item_serial_numbers` and
    :meth:`PimModule.update_item_serial_numbers`
    (``POST``/``PUT /rest/pim/item-serial-numbers``).

    Keys:
        itemId: Item ID the serial number is assigned to. **Required.**
        serialNumber: The serial number string. **Required.**
        orderId: Order ID the serial number was consumed by, if assigned
            during order fulfilment.
        orderItemId: Order item ID the serial number was consumed by, if
            assigned during order fulfilment.
    """

    itemId: Required[int]
    serialNumber: Required[str]
    orderId: NotRequired[int]
    orderItemId: NotRequired[int]
```

- [ ] **Step 4: Export `ItemSerialNumberPayload` from `__init__.py`**

Add `ItemSerialNumberPayload` to both the import list and `__all__`.

- [ ] **Step 5: Implement the four methods in `pim.py`**

Add after `get_barcode_duplicate_settings`, under a new section comment:

```python
# -- Item serial numbers --------------------------------------------------

async def list_item_serial_numbers(
    self,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search serial numbers assigned to item variations.

    Args:
        with_: Optional list of related data to embed.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched serial number records, each
          with at minimum ``id``, ``itemId``, and ``serialNumber``.
        - ``totalsCount`` (int): Total number of matching records.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    params = self._build_params(None, with_)
    return await self._session.get(
        "/rest/pim/item-serial-numbers", params=params or None
    )

async def create_item_serial_numbers(
    self,
    data: list[ItemSerialNumberPayload],
) -> dict[str, Any]:
    """Bulk create item serial numbers.

    Args:
        data: List of serial number payloads. Use
            :class:`~plentymarkets._types.ItemSerialNumberPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``created`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.post("/rest/pim/item-serial-numbers", json=data)

async def update_item_serial_numbers(
    self,
    data: list[ItemSerialNumberPayload],
) -> dict[str, Any]:
    """Bulk update item serial numbers.

    Args:
        data: List of serial number payloads. Use
            :class:`~plentymarkets._types.ItemSerialNumberPayload` for IDE
            autocomplete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
        live system before relying on these keys.
    """
    return await self._session.put("/rest/pim/item-serial-numbers", json=data)

async def delete_item_serial_numbers(self, ids: list[int]) -> dict[str, Any]:
    """Bulk delete item serial numbers by ID.

    Args:
        ids: List of serial number record IDs to delete.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; expect
        ``deleted`` (int). Verify against a live system before relying on
        this key.
    """
    return await self._session.delete("/rest/pim/item-serial-numbers", json=ids)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 7: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_item_serial_numbers` — search item serial numbers via `GET /rest/pim/item-serial-numbers`
- feat: `PimModule.create_item_serial_numbers` — bulk create item serial numbers via `POST /rest/pim/item-serial-numbers`
- feat: `PimModule.update_item_serial_numbers` — bulk update item serial numbers via `PUT /rest/pim/item-serial-numbers`
- feat: `PimModule.delete_item_serial_numbers` — bulk delete item serial numbers via `DELETE /rest/pim/item-serial-numbers`
```

- [ ] **Step 8: Update `ROADMAP.md`**

Change the `/rest/pim/item-serial-numbers` row's Status to `**implemented**`:

```
| `/rest/pim/item-serial-numbers` | GET, PUT, POST, DELETE (all **implemented**) | Search, create, update, and delete serial numbers assigned to item variations | **implemented** |
```

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add item serial number list, create, update, and delete"
```

---

## Task 14: Item lookups (Group 7 — read-only, no TypedDicts)

**Files:**
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.get`
- Produces:
  - `PimModule.get_item_attributes(item_id) -> dict[str, Any]`
  - `PimModule.get_item_combinations(item_id) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_get_item_attributes(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/items/42/attributes",
        json=[{"attributeId": 3, "backendName": "Colour"}],
    )
    result = await pim.get_item_attributes(42)
    assert result[0]["attributeId"] == 3


async def test_get_item_combinations(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/items/42/combinations",
        json=[{"attributeValueSetIds": [10, 20]}],
    )
    result = await pim.get_item_combinations(42)
    assert result[0]["attributeValueSetIds"] == [10, 20]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_pim.py -k "item_attributes or item_combinations" -v`
Expected: `AttributeError` for each missing method.

- [ ] **Step 3: Implement the two methods in `pim.py`**

Add after `delete_item_serial_numbers`, under a new section comment:

```python
# -- Item lookups -----------------------------------------------------------

async def get_item_attributes(self, item_id: int) -> dict[str, Any]:
    """Get all attributes linked to a given item.

    Args:
        item_id: The PlentyMarkets item ID.

    Returns:
        The raw response as returned by the API. The OpenAPI spec
        documents this endpoint's response as a JSON array (not the usual
        ``entries``-wrapped envelope), so despite the ``dict`` type hint
        shared by every method on this class, callers should expect a
        ``list[dict]`` at runtime — each dict describing one linked
        attribute, with at minimum ``attributeId`` and ``backendName``.
        Verify against a live system.
    """
    return await self._session.get(f"/rest/pim/items/{item_id}/attributes")

async def get_item_combinations(self, item_id: int) -> dict[str, Any]:
    """Get all valid variation combinations (attribute value sets) for an item.

    Args:
        item_id: The PlentyMarkets item ID.

    Returns:
        The raw response as returned by the API. The OpenAPI spec
        documents this endpoint's response as a JSON array (not the usual
        ``entries``-wrapped envelope), so despite the ``dict`` type hint
        shared by every method on this class, callers should expect a
        ``list[dict]`` at runtime — each dict describing one valid
        combination, with at minimum ``attributeValueSetIds``
        (list[int]). Verify against a live system.
    """
    return await self._session.get(f"/rest/pim/items/{item_id}/combinations")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 5: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.get_item_attributes` — get attributes linked to an item via `GET /rest/pim/items/{id}/attributes`
- feat: `PimModule.get_item_combinations` — get valid variation combinations for an item via `GET /rest/pim/items/{id}/combinations`
```

- [ ] **Step 6: Update `ROADMAP.md`**

Change these two rows' Status to `**implemented**`:

```
| `/rest/pim/items/{id}/attributes` | GET | Get all attributes linked to a given item | **implemented** |
| `/rest/pim/items/{id}/combinations` | GET | Get all valid variation combinations (attribute value sets) for a given item | **implemented** |
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add item attribute and combination lookups"
```

---

## Task 15: Amazon product types (Group 8 — read-only, no TypedDicts)

**Files:**
- Modify: `src/plentymarkets/modules/pim.py`
- Modify: `tests/test_pim.py`
- Modify: `CHANGELOG.md`, `ROADMAP.md`

**Interfaces:**
- Consumes: `_Session.get`
- Produces:
  - `PimModule.list_amazon_product_types() -> dict[str, Any]`

This is the last endpoint-adding task. After this task, every row in `ROADMAP.md`'s `Pim`
section should read `**implemented**`.

---

- [ ] **Step 1: Write the failing test**

Append to `tests/test_pim.py`:

```python
async def test_list_amazon_product_types(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/amazon-product-types",
        json={"entries": [{"productType": "SHOES"}]},
    )
    result = await pim.list_amazon_product_types()
    assert result["entries"][0]["productType"] == "SHOES"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_pim.py -k "amazon_product_types" -v`
Expected: `AttributeError: 'PimModule' object has no attribute 'list_amazon_product_types'`

- [ ] **Step 3: Implement the method in `pim.py`**

Add after `get_item_combinations`, under a new section comment:

```python
# -- Amazon product types ----------------------------------------------------

async def list_amazon_product_types(self) -> dict[str, Any]:
    """List Amazon product type definitions available for attribute mapping.

    Returns:
        A dict with the response body returned by the API. PlentyMarkets
        does not publish a fixed schema for this endpoint; verify against
        a live system before relying on its keys.
    """
    return await self._session.get("/rest/pim/amazon-product-types")
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `uv run pytest tests/test_pim.py -v`
Expected: all tests pass.

- [ ] **Step 5: Run the full project test suite to check for regressions**

Run: `uv run pytest -v`
Expected: all existing tests plus every new PIM test pass; zero failures.

- [ ] **Step 6: Update `CHANGELOG.md`**

Append to the `### Pim` section:

```markdown
- feat: `PimModule.list_amazon_product_types` — list Amazon product types via `GET /rest/pim/amazon-product-types`
```

- [ ] **Step 7: Update `ROADMAP.md`**

Change the `/rest/pim/amazon-product-types` row's Status to `**implemented**`:

```
| `/rest/pim/amazon-product-types` | GET | List Amazon product type definitions available for attribute mapping | **implemented** |
```

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add amazon product type lookup"
```

---

## Task 16: Final verification and version bump to 0.2.0

**Files:**
- Modify: `pyproject.toml` (version bump, handled by `cz bump`)
- Modify: `CHANGELOG.md` (versioning of `[Unreleased]`, handled by `cz bump`'s pre-bump hook)
- Read-only check: `ROADMAP.md`

**Interfaces:**
- Consumes: `commitizen` (`cz`), already configured in `pyproject.toml`
  (`[tool.commitizen]`: `version = "0.1.2"`, `tag_format = "v$version"`,
  `version_files = ["pyproject.toml:version"]`,
  `pre_bump_hooks = ["python3 scripts/bump_changelog.py"]`)
- Produces: `pyproject.toml` version `0.2.0`, a versioned `## [0.2.0] - <date>` section in
  `CHANGELOG.md`, a `bump:` commit, and a `v0.2.0` git tag.

---

- [ ] **Step 1: Confirm every `Pim` endpoint in `ROADMAP.md` is marked implemented**

Run:

```bash
grep -c '\*\*implemented\*\*' ROADMAP.md
grep -A200 '### `Pim`' ROADMAP.md | grep -E '\| planned \||\| partial \|'
```

Expected: the second command prints nothing — every row in the `Pim` section (both the module
summary table at the top of the file and every endpoint table under `### \`Pim\``) reads
`**implemented**`. If any row still reads `planned` or `partial`, stop and go back to the task
that was supposed to cover it — do not proceed to the version bump with incomplete coverage.

Also update the top-of-file module summary table's `Pim` row (originally
`planned — [endpoints documented](#pim--restpim)`) to:

```
| `Pim` | Product Information Management — PIM-specific item operations | **[core]** |
```

- [ ] **Step 2: Run the full test suite**

Run: `uv run pytest -v`
Expected: every test passes, zero failures. This includes the original 10 PIM tests plus every
test added across Tasks 1-15 (roughly 50-60 PIM tests total) plus the pre-existing
orders/items/stock/contacts/session test suites.

- [ ] **Step 3: Commit the ROADMAP module-summary update**

```bash
git add ROADMAP.md
git commit -m "docs(roadmap): mark Pim module fully implemented"
```

- [ ] **Step 4: Run the version bump**

```bash
uv run cz bump --increment MINOR
```

This reads `[tool.commitizen]` from `pyproject.toml`, runs `scripts/bump_changelog.py` (versioning
the `[Unreleased]` section into `## [0.2.0] - <today's date>`), updates
`pyproject.toml`'s `version = "0.2.0"`, and creates a `bump: version 0.1.2 → 0.2.0` commit plus a
`v0.2.0` tag automatically — no manual `git commit` step needed here, unlike every prior task.

- [ ] **Step 5: Verify the bump**

```bash
git log --oneline -3
grep '^version' pyproject.toml
grep -m1 '^## \[' CHANGELOG.md
```

Expected: the log shows the new `bump:` commit at HEAD, `pyproject.toml` reads
`version = "0.2.0"`, and `CHANGELOG.md`'s first `## [...]` heading reads `## [0.2.0] - <today's
date>` with an empty `## [Unreleased]` section above it.

---

## Plan Complete

Once Task 16 lands, `PimModule` covers all 41 `/rest/pim/*` endpoints from the OpenAPI spec, the
package is at `0.2.0`, and the single feature branch (per CLAUDE.md's branch workflow) is ready
to merge back into `staging`.
