# PIM Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `PimModule` (`client.pim`) covering variation search/scroll/bulk-update and read-only lookups for categories, attributes, and sales prices — all under `/rest/pim/`.

**Architecture:** New `PimModule` class in `src/plentymarkets/modules/pim.py`, wired as a lazy property on `PlentyClient` identical to the existing four modules. A `_build_params` helper inside the module handles the `with_` list → comma-joined `with` query param and merges caller-supplied `filters`. The scroll/paginate method is a cursor-based `AsyncIterator` analogous to `ItemsModule.paginate_items`.

**Tech Stack:** Python ≥3.11, httpx (via shared `_Session`), pytest + pytest-httpx (unit tests mock at the transport layer — no live network needed).

## Global Constraints

- All source under `src/plentymarkets/`; tests under `tests/`
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio` decorator on any test
- Google-style docstrings on every public method; document every response key and every payload key
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`
- `CHANGELOG.md`: append only to `[Unreleased]`; group under `## Pim`
- `ROADMAP.md`: update Status column from `planned` → `**implemented**` for each endpoint as it is implemented
- Branch: `staging`; `main` is protected

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Modify | `src/plentymarkets/_types.py` | Add `VariationBaseUpdatePayload` TypedDict |
| Modify | `src/plentymarkets/__init__.py` | Export `VariationBaseUpdatePayload` |
| **Create** | `src/plentymarkets/modules/pim.py` | `PimModule` with all 9 methods |
| Modify | `src/plentymarkets/client.py` | Add `_pim` backing field + `pim` property |
| **Create** | `tests/test_pim.py` | Full unit test suite for `PimModule` |
| Modify | `CHANGELOG.md` | Add `[Unreleased] ## Pim` entries |
| Modify | `ROADMAP.md` | Mark 9 endpoints as implemented |

---

## Task 1: TypedDict + PimModule scaffold + client wiring

**Files:**
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Create: `src/plentymarkets/modules/pim.py`
- Modify: `src/plentymarkets/client.py`
- Create: `tests/test_pim.py` (fixture + one smoke test)

**Interfaces:**
- Produces: `PimModule` class importable from `plentymarkets.modules.pim`; `client.pim` property returning a `PimModule`; `VariationBaseUpdatePayload` exported from `plentymarkets`

---

- [ ] **Step 1: Write the failing smoke test**

Add `tests/test_pim.py`:

```python
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.pim import PimModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def pim(session):
    return PimModule(session)


async def test_pim_module_repr(pim):
    assert repr(pim) == "<PimModule /rest/pim>"
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
uv run pytest tests/test_pim.py -v
```

Expected: `ImportError` — `PimModule` does not exist yet.

- [ ] **Step 3: Add VariationBaseUpdatePayload to `_types.py`**

Append after the last class in `src/plentymarkets/_types.py`:

```python
# ---------------------------------------------------------------------------
# PIM  (/rest/pim/)
# ---------------------------------------------------------------------------


class VariationBaseUpdatePayload(TypedDict, total=False):
    """One entry in the list passed to :meth:`PimModule.update_variation_bases`
    (``PUT /rest/pim/variations/bases``).

    Keys:
        id: Variation ID to update. **Required.**
        number: Variation number / internal SKU string.
        isMain: Whether this is the item's main variation.
        isActive: Whether the variation is active and visible.
        model: Model identifier string shown in the back end.
        purchasePrice: Net purchase price used for margin calculations.
        vatId: VAT configuration ID.
        availabilityId: Availability level (1–10, maps to availability icons).
        weightG: Gross weight in grams.
        weightNetG: Net weight in grams.
        widthMM: Width in millimetres.
        lengthMM: Length in millimetres.
        heightMM: Height in millimetres.
        position: Display sort position within the item.
        stockLimitation: 0=no limit, 1=limited to net stock, 2=disabled.
        unitId: Unit ID (e.g. piece, litre).
        unitsContained: Quantity of base units within this variation unit.
        mainVariationId: ID of the item's main variation (set on child
            variations to declare the parent).
    """

    id: Required[int]
    number: NotRequired[str]
    isMain: NotRequired[bool]
    isActive: NotRequired[bool]
    model: NotRequired[str]
    purchasePrice: NotRequired[float]
    vatId: NotRequired[int]
    availabilityId: NotRequired[int]
    weightG: NotRequired[float]
    weightNetG: NotRequired[float]
    widthMM: NotRequired[float]
    lengthMM: NotRequired[float]
    heightMM: NotRequired[float]
    position: NotRequired[int]
    stockLimitation: NotRequired[int]
    unitId: NotRequired[int]
    unitsContained: NotRequired[int]
    mainVariationId: NotRequired[int]
```

- [ ] **Step 4: Export VariationBaseUpdatePayload from `__init__.py`**

In `src/plentymarkets/__init__.py`, add to the import and `__all__`:

```python
from ._types import (
    ContactCreatePayload,
    ContactUpdatePayload,
    ItemCreatePayload,
    ItemUpdatePayload,
    OrderCreatePayload,
    StockCorrectionPayload,
    VariationBaseUpdatePayload,
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
]
```

- [ ] **Step 5: Create `src/plentymarkets/modules/pim.py` with scaffold**

```python
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._types import VariationBaseUpdatePayload

from .._session import _Session


class PimModule:
    """Wraps the PlentyMarkets ``/rest/pim`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<PimModule /rest/pim>"

    @staticmethod
    def _build_params(
        filters: dict[str, Any] | None,
        with_: list[str] | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if filters:
            params.update(filters)
        if with_:
            params["with"] = ",".join(with_)
        return params
```

- [ ] **Step 6: Wire `client.pim` property in `client.py`**

Add the import at the top of `src/plentymarkets/client.py`:

```python
from .modules.pim import PimModule
```

Add the backing field in `__init__`:

```python
self._pim: PimModule | None = None
```

Add the property:

```python
@property
def pim(self) -> PimModule:
    """Access the PIM module (``/rest/pim``)."""
    if self._pim is None:
        self._pim = PimModule(self._session)
    return self._pim
```

- [ ] **Step 7: Run the test to verify it passes**

```bash
uv run pytest tests/test_pim.py -v
```

Expected: `PASSED` — `test_pim_module_repr`.

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        src/plentymarkets/modules/pim.py src/plentymarkets/client.py \
        tests/test_pim.py
git commit -m "feat(pim): scaffold PimModule, VariationBaseUpdatePayload, and client.pim property"
```

---

## Task 2: Variation methods — list, scroll/paginate, bulk update

**Files:**
- Modify: `src/plentymarkets/modules/pim.py` (add 3 methods)
- Modify: `tests/test_pim.py` (add tests)

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`, `_Session.put`
- Produces:
  - `PimModule.list_variations(filters, with_) -> dict[str, Any]`
  - `PimModule.paginate_variations(filters, with_) -> AsyncIterator[dict[str, Any]]`
  - `PimModule.update_variation_bases(data) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_variations_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"entries": [{"id": 1}, {"id": 2}], "totalsCount": 2},
    )
    result = await pim.list_variations()
    assert result["totalsCount"] == 2


async def test_list_variations_with_filters_and_with(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations?isActive=true&with=base%2Cbarcodes",
        json={"entries": [{"id": 5}], "totalsCount": 1},
    )
    result = await pim.list_variations(
        filters={"isActive": "true"},
        with_=["base", "barcodes"],
    )
    assert result["entries"][0]["id"] == 5


async def test_paginate_variations_yields_all_across_cursors(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll",
        json={"entries": [{"id": 10}, {"id": 11}], "cursor": "abc123"},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?cursor=abc123",
        json={"entries": [{"id": 12}], "cursor": None},
    )
    results = [v async for v in pim.paginate_variations()]
    assert [r["id"] for r in results] == [10, 11, 12]


async def test_paginate_variations_stops_on_empty_entries(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll",
        json={"entries": [], "cursor": None},
    )
    results = [v async for v in pim.paginate_variations()]
    assert results == []


async def test_update_variation_bases_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/bases",
        json={"updated": 1},
    )
    result = await pim.update_variation_bases([{"id": 7, "isActive": True}])
    assert result["updated"] == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
uv run pytest tests/test_pim.py -v
```

Expected: 5 new failures — `AttributeError: 'PimModule' object has no attribute 'list_variations'` etc.

- [ ] **Step 3: Implement the three variation methods in `pim.py`**

Add these methods to `PimModule` (after `_build_params`):

```python
async def list_variations(
    self,
    filters: dict[str, Any] | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search and filter variations.

    Args:
        filters: Optional dict of filter/sort query parameters. Any of the
            70+ parameters supported by ``GET /rest/pim/variations`` may be
            passed here (e.g. ``{"isActive": "true", "itemId": 42}``).
        with_: Optional list of related data to include inline. Accepted
            values include ``"base"``, ``"base.item"``, ``"base.texts"``,
            ``"base.images"``, ``"base.stock"``, ``"barcodes"``,
            ``"categories"``, ``"clients"``, ``"salesPrices"``,
            ``"warehouses"``, ``"tags"``, ``"properties"``, ``"images"``,
            ``"attributeValues"``, ``"skus"``, ``"markets"``,
            ``"defaultCategories"``, ``"supplier"``, ``"unit"``,
            ``"timestamps"``, ``"bundleComponents"``, ``"comments"``.
            Dotted sub-includes (e.g. ``"base.item"``) pull nested records.

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched variation records. Each dict
          contains the fields requested via ``with_`` plus variation ID.
        - ``totalsCount`` (int): Total number of matching variations.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    params = self._build_params(filters, with_)
    return await self._session.get("/rest/pim/variations", params=params or None)

async def paginate_variations(
    self,
    filters: dict[str, Any] | None = None,
    with_: list[str] | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Async generator that yields every variation via cursor-based scroll.

    Uses ``GET /rest/pim/variations/scroll``. Prefer this over
    :meth:`list_variations` when iterating the full catalogue; the scroll
    API is optimised for large result sets and does not require page-count
    arithmetic.

    Args:
        filters: Optional dict of filter query parameters (same set as
            :meth:`list_variations`, excluding pagination params).
        with_: Optional list of related data to include inline (same values
            as :meth:`list_variations`).

    Yields:
        Individual variation dicts. Each dict contains at minimum ``id``;
        additional keys depend on the ``with_`` includes requested.
    """
    params = self._build_params(filters, with_)
    cursor: str | None = None

    while True:
        call_params = dict(params)
        if cursor:
            call_params["cursor"] = cursor
        result = await self._session.get(
            "/rest/pim/variations/scroll",
            params=call_params or None,
        )
        entries = result.get("entries", [])
        if not entries:
            break
        for entry in entries:
            yield entry
        cursor = result.get("cursor") or None
        if not cursor:
            break

async def update_variation_bases(
    self,
    data: list[VariationBaseUpdatePayload],
) -> dict[str, Any]:
    """Bulk create or update variation base data.

    Args:
        data: List of variation update payloads. Each entry must contain
            ``id`` (the variation ID to update). Use
            :class:`~plentymarkets._types.VariationBaseUpdatePayload` for
            IDE autocomplete. Only provided keys are changed.

    Returns:
        A dict with the following keys:

        - ``updated`` (int): Number of variations successfully updated.
        - ``invalid`` (list[dict]): Entries that failed validation, each
          with ``id`` and ``reason``.
    """
    return await self._session.put("/rest/pim/variations/bases", json=data)
```

Also add `AsyncIterator` to the import line at the top of `pim.py`:

```python
from typing import TYPE_CHECKING, Any, AsyncIterator
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
uv run pytest tests/test_pim.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Update CHANGELOG.md**

Add under `[Unreleased]` in `CHANGELOG.md`:

```markdown
### Pim

- feat: `PimModule.list_variations` — search and filter variations via `GET /rest/pim/variations`
- feat: `PimModule.paginate_variations` — cursor-based async iterator via `GET /rest/pim/variations/scroll`
- feat: `PimModule.update_variation_bases` — bulk variation update via `PUT /rest/pim/variations/bases`
```

- [ ] **Step 6: Update ROADMAP.md**

In `ROADMAP.md`, change `planned` → `**implemented**` for these three rows:

```
| `/rest/pim/variations` | GET, PUT, DELETE | ... | **implemented** |
| `/rest/pim/variations/scroll` | GET | ... | **implemented** |
| `/rest/pim/variations/bases` | PUT | ... | **implemented** |
```

Note: Only the GET on `/rest/pim/variations` and GET on `/rest/pim/variations/scroll` and PUT on `/rest/pim/variations/bases` are implemented; the PUT/DELETE on `/rest/pim/variations` itself remain `planned`.

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add variation list, cursor-scroll pagination, and bulk base update"
```

---

## Task 3: Reference data — categories, attributes, sales prices

**Files:**
- Modify: `src/plentymarkets/modules/pim.py` (add 6 methods)
- Modify: `tests/test_pim.py` (add 8 tests)

**Interfaces:**
- Consumes: `PimModule._build_params`, `_Session.get`
- Produces:
  - `PimModule.list_categories(ids, type_, level, name, with_) -> dict[str, Any]`
  - `PimModule.get_category(category_id, with_) -> dict[str, Any]`
  - `PimModule.list_attributes(ids, backend_name, with_) -> dict[str, Any]`
  - `PimModule.get_attribute(attribute_id) -> dict[str, Any]`
  - `PimModule.list_sales_prices(ids, type_, currency, with_) -> dict[str, Any]`
  - `PimModule.get_sales_price(price_id) -> dict[str, Any]`

---

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_pim.py`:

```python
async def test_list_categories_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories",
        json={"entries": [{"id": 1, "type": "item"}], "totalsCount": 1},
    )
    result = await pim.list_categories()
    assert result["totalsCount"] == 1


async def test_list_categories_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories?type=item&level=1",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_categories(type_="item", level=1)
    assert result["totalsCount"] == 0


async def test_get_category(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/99",
        json={"id": 99, "type": "item"},
    )
    result = await pim.get_category(99)
    assert result["id"] == 99


async def test_list_attributes_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"entries": [{"id": 3, "backendName": "Colour"}], "totalsCount": 1},
    )
    result = await pim.list_attributes()
    assert result["entries"][0]["backendName"] == "Colour"


async def test_list_attributes_with_backend_name(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes?backendName=Size",
        json={"entries": [{"id": 4}], "totalsCount": 1},
    )
    result = await pim.list_attributes(backend_name="Size")
    assert result["entries"][0]["id"] == 4


async def test_get_attribute(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/3",
        json={"id": 3, "backendName": "Colour"},
    )
    result = await pim.get_attribute(3)
    assert result["backendName"] == "Colour"


async def test_list_sales_prices_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"entries": [{"id": 1, "type": "default"}], "totalsCount": 1},
    )
    result = await pim.list_sales_prices()
    assert result["totalsCount"] == 1


async def test_get_sales_price(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/sales_prices/1",
        json={"id": 1, "type": "default", "currency": "EUR"},
    )
    result = await pim.get_sales_price(1)
    assert result["currency"] == "EUR"
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
uv run pytest tests/test_pim.py -v
```

Expected: 8 new failures — `AttributeError: 'PimModule' object has no attribute 'list_categories'` etc.

- [ ] **Step 3: Implement the six reference-data methods in `pim.py`**

Append these methods to `PimModule`:

```python
async def list_categories(
    self,
    ids: list[int] | None = None,
    type_: str | None = None,
    level: int | None = None,
    name: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search categories.

    Args:
        ids: Restrict results to categories with these IDs.
        type_: Restrict results to categories of this type. Common values:
            ``"item"`` (product categories), ``"content"`` (CMS pages),
            ``"container"``, ``"blog"``.
        level: Restrict results to categories at this tree depth (1=root).
        name: Restrict results to categories whose name contains this string.
        with_: Optional list of related data to embed. Accepted values:
            ``"details"`` (multilingual name, description, meta data),
            ``"clients"`` (which stores have the category active),
            ``"branch"`` (full ancestor path).

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched category records. Each dict
          contains at minimum ``id`` and ``type``; additional keys depend
          on the ``with_`` includes requested.
        - ``totalsCount`` (int): Total number of matching categories.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if ids is not None:
        filters["ids"] = ",".join(str(i) for i in ids)
    if type_ is not None:
        filters["type"] = type_
    if level is not None:
        filters["level"] = level
    if name is not None:
        filters["name"] = name
    params = self._build_params(filters or None, with_)
    return await self._session.get("/rest/pim/categories", params=params or None)

async def get_category(
    self,
    category_id: int,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Get a single category by ID.

    Args:
        category_id: The PlentyMarkets category ID.
        with_: Optional list of related data to embed (same values as
            :meth:`list_categories`).

    Returns:
        A dict with the following keys:

        - ``id`` (int): The category ID.
        - ``type`` (str): Category type (e.g. ``"item"``, ``"content"``).
        - ``parentCategoryId`` (int | None): Parent category ID, or
          ``None`` for root categories.
        - ``level`` (int): Tree depth (1=root).
        - ``right`` (str): Visibility. ``"all"`` or ``"customer"``.
        - ``sitemap`` (str): Whether included in sitemap (``"Y"``/``"N"``).
        - ``linklist`` (str): Whether shown in link list (``"Y"``/``"N"``).
        - ``updatedAt`` (str): ISO 8601 last-update timestamp.
    """
    params = self._build_params(None, with_)
    return await self._session.get(
        f"/rest/pim/categories/{category_id}",
        params=params or None,
    )

async def list_attributes(
    self,
    ids: list[int] | None = None,
    backend_name: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search attributes (variation axes such as colour or size).

    Args:
        ids: Restrict results to attributes with these IDs.
        backend_name: Restrict results to the attribute with this exact
            back-end name (case-sensitive).
        with_: Optional list of related data to embed. Accepted values:
            ``"names"`` (multilingual display names),
            ``"values"`` (all attribute values),
            ``"values.names"`` (multilingual names for each value),
            ``"maps"`` (marketplace attribute mappings).

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched attribute records. Each dict
          contains at minimum ``id`` and ``backendName``; additional keys
          depend on the ``with_`` includes requested.
        - ``totalsCount`` (int): Total number of matching attributes.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if ids is not None:
        filters["ids"] = ",".join(str(i) for i in ids)
    if backend_name is not None:
        filters["backendName"] = backend_name
    params = self._build_params(filters or None, with_)
    return await self._session.get("/rest/pim/attributes", params=params or None)

async def get_attribute(self, attribute_id: int) -> dict[str, Any]:
    """Get a single attribute by ID.

    Args:
        attribute_id: The PlentyMarkets attribute ID.

    Returns:
        A dict with the following keys:

        - ``id`` (int): The attribute ID.
        - ``backendName`` (str): Internal back-end name (unique, no commas
          colons, semicolons, or quotes).
        - ``position`` (int): Display sort position in the attribute list.
        - ``isSurchargePercental`` (bool): Whether value surcharges are
          treated as a percentage.
        - ``isLinkableToImage`` (bool): Whether images can be linked to
          attribute values.
        - ``amazonAttribute`` (str | None): Linked Amazon attribute name.
        - ``updatedAt`` (str): ISO 8601 last-update timestamp.
    """
    return await self._session.get(f"/rest/pim/attributes/{attribute_id}")

async def list_sales_prices(
    self,
    ids: list[int] | None = None,
    type_: str | None = None,
    currency: str | None = None,
    with_: list[str] | None = None,
) -> dict[str, Any]:
    """Search sales price configurations.

    Sales price configurations define the *type* of price (default, RRP,
    special offer, etc.) and which clients, customer classes, countries, and
    referrers the price applies to. Actual price *values* are stored on the
    variation via ``/rest/pim/variations/sales_prices``.

    Args:
        ids: Restrict results to sales prices with these IDs.
        type_: Restrict results to prices of this type. Common values:
            ``"default"``, ``"rrp"``, ``"specialOffer"``, ``"setPrice"``.
        currency: Restrict results to prices in this ISO 4217 currency code
            (e.g. ``"EUR"``, ``"GBP"``).
        with_: Optional list of related data to embed. Accepted values:
            ``"names"`` (multilingual display names),
            ``"accounts"`` (linked client/referrer/country rules).

    Returns:
        A dict with the following keys:

        - ``entries`` (list[dict]): Matched sales price configuration records.
          Each dict contains at minimum ``id``, ``type``, and ``currency``;
          additional keys depend on the ``with_`` includes requested.
        - ``totalsCount`` (int): Total number of matching price configurations.
        - ``isLastPage`` (bool): ``True`` when no further pages exist.
        - ``lastPageNumber`` (int): Number of the last page.
        - ``page`` (int): Current page number.
    """
    filters: dict[str, Any] = {}
    if ids is not None:
        filters["ids"] = ",".join(str(i) for i in ids)
    if type_ is not None:
        filters["type"] = type_
    if currency is not None:
        filters["currency"] = currency
    params = self._build_params(filters or None, with_)
    return await self._session.get("/rest/pim/sales_prices", params=params or None)

async def get_sales_price(self, price_id: int) -> dict[str, Any]:
    """Get a single sales price configuration by ID.

    Args:
        price_id: The PlentyMarkets sales price ID.

    Returns:
        A dict with the following keys:

        - ``id`` (int): The sales price ID.
        - ``type`` (str): Price type (e.g. ``"default"``, ``"rrp"``).
        - ``currency`` (str): ISO 4217 currency code (e.g. ``"EUR"``).
        - ``position`` (int): Display sort position.
        - ``isLiveConversion`` (bool): Whether to apply live FX conversion.
        - ``minimumOrderQuantity`` (float): Minimum quantity for this price
          to apply.
        - ``updatedAt`` (str): ISO 8601 last-update timestamp.
    """
    return await self._session.get(f"/rest/pim/sales_prices/{price_id}")
```

- [ ] **Step 4: Run the full test suite**

```bash
uv run pytest tests/test_pim.py -v
```

Expected: all tests pass (including Tasks 1 and 2 tests).

- [ ] **Step 5: Run the full project test suite to check for regressions**

```bash
uv run pytest -v
```

Expected: all existing tests plus new PIM tests pass; zero failures.

- [ ] **Step 6: Update CHANGELOG.md**

Extend the `### Pim` section added in Task 2:

```markdown
- feat: `PimModule.list_categories` — search categories via `GET /rest/pim/categories`
- feat: `PimModule.get_category` — get one category via `GET /rest/pim/categories/{id}`
- feat: `PimModule.list_attributes` — search attributes via `GET /rest/pim/attributes`
- feat: `PimModule.get_attribute` — get one attribute via `GET /rest/pim/attributes/{id}`
- feat: `PimModule.list_sales_prices` — search sales prices via `GET /rest/pim/sales_prices`
- feat: `PimModule.get_sales_price` — get one sales price via `GET /rest/pim/sales_prices/{id}`
```

- [ ] **Step 7: Update ROADMAP.md**

Change `planned` → `**implemented**` for these six rows:

```
| `/rest/pim/categories` | GET | ... | **implemented** |
| `/rest/pim/categories/{id}` | GET | ... | **implemented** |
| `/rest/pim/attributes` | GET, PUT, POST, DELETE | ... | **implemented** |
| `/rest/pim/attributes/{id}` | GET | ... | **implemented** |
| `/rest/pim/sales_prices` | GET, PUT, POST, DELETE | ... | **implemented** |
| `/rest/pim/sales_prices/{id}` | GET | ... | **implemented** |
```

Note: Only the GET methods are implemented; PUT/POST/DELETE on attributes and sales_prices remain `planned`.

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/modules/pim.py tests/test_pim.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(pim): add category, attribute, and sales price lookup methods"
```