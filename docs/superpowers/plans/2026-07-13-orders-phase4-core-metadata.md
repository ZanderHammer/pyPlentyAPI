# Order API Phase 4 (Core Order Metadata) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the 69 remaining `Order`-tagged core-metadata endpoints (batch/contact/
accounting lookups, order-item dates, order & order-item properties, referrers, currencies,
coupons, TARIC VAT assignments) on `OrdersModule` (`client.orders`), bringing `Order` tag
coverage from 45/307 to 114/307, then bump the package version.

**Architecture:** Two existing mixins (`CoreMixin` in `core.py`, `DatesMixin` in `dates.py`)
gain new methods. Five new mixins are added, one per new file (`properties.py`, `referrers.py`,
`currencies.py`, `coupons.py`, `taric.py`), each wired into `OrdersModule` in
`src/plentymarkets/modules/orders/__init__.py` the moment its file is created. No new top-level
module, no new `client.py` property — everything lives on `client.orders`.

**Tech Stack:** Python ≥3.11, httpx (via shared `Session`), pytest + pytest-httpx (unit tests
mock at the transport layer — no live network needed). `asyncio_mode = "auto"`.

**Spec:** `docs/superpowers/specs/2026-07-13-orders-phase4-core-metadata-design.md`

## Global Constraints

- All source under `src/plentymarkets/`; tests under `tests/`.
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio` decorator on any test.
- Google-style docstrings on every public method; document every response dict key and every
  payload key, matching the density already in `core.py`/`dates.py`/`statuses.py`.
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
- `CHANGELOG.md`: append only to `[Unreleased]`; group under `## Order`.
- `ROADMAP.md`: update the `### Order` section's Status column from `planned`/
  `deprecated (...)` → `**implemented**` + method name (`orders.<method>`) for each endpoint as
  it lands. The 6 order-level-property rows (`/rest/orders/properties/{id}` PUT/DELETE,
  `/rest/orders/{orderId}/properties*` POST/GET/PUT/DELETE) additionally need their missing
  `deprecated (use PUT /rest/orders/{orderId})` annotation added — verified directly against the
  live OpenAPI spec description field, ROADMAP.md currently only shows `planned` for these 6.
  Also update the top-of-file summary line `**150 / 1837**` → `**219 / 1837**` and the `Order`
  row `**45/307**` → `**114/307**`.
- Branch: single feature branch off `staging` for this whole plan; `main` is protected.
- Where PlentyMarkets' spec declares no request-body schema at all (not even an empty
  placeholder), the method takes `data: dict[str, Any]` and its docstring carries: *"PlentyMarkets'
  published OpenAPI spec declares no request body schema for this endpoint. Verify against a live
  system before relying on this shape."* — same wording pattern as `ROADMAP.md`'s existing "Known
  Schema Gaps" table. Applies only to `update_order_currency` and `update_referrer` in this plan.
- Where a response schema is a bare placeholder (`Collection`, `OrderBooking`,
  `SimpleRestResponse`) or an array of `$ref: mixed`, follow the existing `get_my_account_url`/
  `delete_item_transaction` precedent: type as `dict[str, Any]`/`list[Any]` (add
  `# type: ignore[return-value]` when the underlying `Session` method's declared return type is
  `dict[str, Any]` but the real payload is a list) with a docstring `Note:` explaining the gap.
- Every identifier the spec types inconsistently across sibling operations (`currencyIso`,
  `code`/`coupon`, `taricCode` — string on some operations, integer on others) is typed `str` in
  Python uniformly, with a one-line docstring `Note:` flagging the inconsistency. Do not "fix" the
  wire format — just pick the sane Python type and interpolate it into the URL as-is.
- Deprecated endpoints (marked in the spec's `description` as `<b>DEPRECATED: Use the following
  route: ...</b>`) are still implemented in full (matches this repo's complete-coverage
  philosophy) but get a docstring `Note:` naming the replacement route verbatim.
- Path params spec'd with a literal `?` in the name/segment (`{parentReferrerId?}`,
  `{typeId?}`) but marked `required: true` are implemented as required Python params; docstring
  `Note:` flags the contradiction.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Modify | `src/plentymarkets/modules/orders/core.py` | +10 methods across Tasks 1-4 |
| Modify | `src/plentymarkets/modules/orders/dates.py` | +9 methods across Tasks 5-6 |
| Modify | `src/plentymarkets/modules/orders/transactions.py` | Docstring fix, Task 6 |
| Create | `src/plentymarkets/modules/orders/properties.py` | 20 methods across Tasks 7-10 |
| Create | `src/plentymarkets/modules/orders/referrers.py` | 8 methods, Task 11 |
| Create | `src/plentymarkets/modules/orders/currencies.py` | 7 methods, Task 12 |
| Create | `src/plentymarkets/modules/orders/coupons.py` | 12 methods across Tasks 13-14 |
| Create | `src/plentymarkets/modules/orders/taric.py` | 6 methods, Task 15 |
| Modify | `src/plentymarkets/modules/orders/__init__.py` | Wire in 5 new mixins, incrementally per Tasks 7/11/12/13/15 |
| Modify | `src/plentymarkets/_types.py` | +8 new TypedDicts across Tasks 7, 13, 14 |
| Modify | `src/plentymarkets/__init__.py` | Export the 8 new TypedDicts |
| Modify | `tests/test_orders_core.py` | +12 tests, Tasks 1-4 |
| Modify | `tests/test_orders_dates.py` | +9 tests, Tasks 5-6 |
| Create | `tests/test_orders_properties.py` | +20 tests, Tasks 7-10 |
| Create | `tests/test_orders_referrers.py` | +8 tests, Task 11 |
| Create | `tests/test_orders_currencies.py` | +7 tests, Task 12 |
| Create | `tests/test_orders_coupons.py` | +12 tests, Tasks 13-14 |
| Create | `tests/test_orders_taric.py` | +6 tests, Task 15 |
| Modify | `CHANGELOG.md`, `ROADMAP.md` | Per task |
| Modify | `pyproject.toml`, `CHANGELOG.md` | Final task: version bump via `cz bump` |

All new/modified source files start with `from __future__ import annotations`. `Any`/
`AsyncIterator` come from `typing`. TypedDict imports for type-checking only go under
`if TYPE_CHECKING:` (see `core.py`'s existing pattern).

---

## Task 1: `core.py` batch A — batch fetch and contact orders

**Files:**
- Modify: `src/plentymarkets/modules/orders/core.py`
- Test: `tests/test_orders_core.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session` (existing)
- Produces:
  - `CoreMixin.get_orders_batch(order_ids: list[int], with_: list[str] | None = None, add_order_items: bool | None = None) -> Any`
  - `CoreMixin.list_contact_orders(contact_id: int, page: int = 1, items_per_page: int = 50, with_: list[str] | None = None) -> dict[str, Any]`
  - `CoreMixin.paginate_contact_orders(contact_id: int, with_: list[str] | None = None, items_per_page: int = 50) -> AsyncIterator[dict[str, Any]]`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_core.py`:

```python
async def test_get_orders_batch_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/batch?orderIds=1%2C2&addOrderItems=true",
        json=[{"id": 1}, {"id": 2}],
    )
    result = await orders.get_orders_batch([1, 2], add_order_items=True)
    assert result == [{"id": 1}, {"id": 2}]


async def test_list_contact_orders_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_contact_orders(7)
    assert result["page"] == 1


async def test_paginate_contact_orders_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [
        o async for o in orders.paginate_contact_orders(7, items_per_page=2)
    ]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_contact_orders_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_contact_orders(7)]
    assert results == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_core.py -v -k "batch or contact_orders"`
Expected: FAIL with `AttributeError: 'OrdersModule' object has no attribute 'get_orders_batch'`.

- [ ] **Step 3: Implement in `core.py`**

Add to `CoreMixin`, after `paginate_search` (the last existing method):

```python
    async def get_orders_batch(
        self,
        order_ids: list[int],
        with_: list[str] | None = None,
        add_order_items: bool | None = None,
    ) -> Any:
        """Get several orders at once by ID.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as ``Collection`` — a bare placeholder schema
            (``{"type": "object"}``) with no further structure, despite the
            plural "Get orders" name and the array-shaped ``orderIds``
            filter. Unlike similar gaps elsewhere in this module, the
            response isn't even confidently a list here. Verify against a
            live system before depending on this endpoint's shape.

        Args:
            order_ids: Order IDs to fetch.
            with_: Related data to embed on each order.
            add_order_items: Whether to include each order's items in the
                response.

        Returns:
            Unverified shape — see the Note above. Likely a list of order
            dicts (see :meth:`get` for the per-order field reference).
        """
        params = self._build_params(
            None,
            with_=with_,
            orderIds=",".join(str(i) for i in order_ids),
            addOrderItems=add_order_items,
        )
        return await self._session.get("/rest/orders/batch", params=params)

    async def list_contact_orders(
        self,
        contact_id: int,
        page: int = 1,
        items_per_page: int = 50,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """List all orders belonging to a contact, with pagination.

        Args:
            contact_id: The contact ID.
            page: Page number (1-indexed).
            items_per_page: Results per page.
            with_: Related data to embed on each order.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching orders.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Order dicts (see :meth:`get` for the
              field reference).
        """
        params = self._build_params(
            None, with_=with_, page=page, itemsPerPage=items_per_page
        )
        return await self._session.get(
            f"/rest/orders/contacts/{contact_id}", params=params
        )

    async def paginate_contact_orders(
        self,
        contact_id: int,
        with_: list[str] | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every order belonging to a contact
        across all pages.

        Args:
            contact_id: The contact ID.
            with_: Related data to embed on each order.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual order dicts (see :meth:`get` for the field
            reference).
        """
        page = 1
        while True:
            result = await self.list_contact_orders(
                contact_id, page=page, items_per_page=items_per_page, with_=with_
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_core.py -v`
Expected: all tests pass, including the 4 new ones.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add to the existing `### Order` section under `[Unreleased]` in `CHANGELOG.md` (create the
section — `## [Unreleased]` currently has no subsections — with this as its first entries):

```markdown
### Order

- feat: `OrdersModule.get_orders_batch` — get several orders at once by ID via `GET /rest/orders/batch`
- feat: `OrdersModule.list_contact_orders` / `paginate_contact_orders` — list/iterate a contact's orders via `GET /rest/orders/contacts/{contactId}`
```

- [ ] **Step 6: Update `ROADMAP.md`**

In the `### Order` table, change these two rows:

```
| GET | `/rest/orders/batch` | Get orders | **implemented** | `orders.get_orders_batch` |
| GET | `/rest/orders/contacts/{contactId}` | List orders of a contact | **implemented** | `orders.list_contact_orders` |
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/core.py tests/test_orders_core.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add batch order fetch and per-contact order listing"
```

---

## Task 2: `core.py` batch B — multi-order creation and accounting summaries

**Files:**
- Modify: `src/plentymarkets/modules/orders/core.py`
- Test: `tests/test_orders_core.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `CoreMixin.create_multi_order(contact_id: int) -> dict[str, Any]`
  - `CoreMixin.list_accounting_summaries(order_id: int | None = None, document_type: str | None = None, created_at_from: str | None = None, created_at_to: str | None = None, page: int = 1, items_per_page: int = 10) -> dict[str, Any]`
  - `CoreMixin.paginate_accounting_summaries(order_id: int | None = None, document_type: str | None = None, created_at_from: str | None = None, created_at_to: str | None = None, items_per_page: int = 10) -> AsyncIterator[dict[str, Any]]`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_core.py`:

```python
async def test_create_multi_order_posts_to_contact_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/contacts/7/multi_order",
        json={"id": 99, "typeId": 9},
    )
    result = await orders.create_multi_order(7)
    assert result["typeId"] == 9


async def test_list_accounting_summaries_defaults_to_page_1_and_10(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/documents/accounting_summary?page=1&itemsPerPage=10",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_accounting_summaries()
    assert result["page"] == 1


async def test_list_accounting_summaries_sends_filters(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/documents/accounting_summary?orderId=42"
            "&documentType=reversal_document&createdAtFrom=2026-01-01"
            "&createdAtTo=2026-02-01&page=1&itemsPerPage=10"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_accounting_summaries(
        order_id=42,
        document_type="reversal_document",
        created_at_from="2026-01-01",
        created_at_to="2026-02-01",
    )
    assert result["page"] == 1


async def test_paginate_accounting_summaries_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/documents/accounting_summary?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"key": "a"}, {"key": "b"}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/documents/accounting_summary?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"key": "c"}],
        },
    )
    results = [
        s async for s in orders.paginate_accounting_summaries(items_per_page=2)
    ]
    assert [r["key"] for r in results] == ["a", "b", "c"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_core.py -v -k "multi_order or accounting_summaries"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `core.py`**

Add to `CoreMixin`, after `paginate_contact_orders`:

```python
    async def create_multi_order(self, contact_id: int) -> dict[str, Any]:
        """Create a multi-order for a contact.

        Note:
            Behavior depends on the options chosen in the PlentyMarkets
            back end under System » Orders » Order types » Multi-order.

        Args:
            contact_id: The contact ID.

        Returns:
            The created order dict (see :meth:`get` for the field
            reference); ``typeId`` will be ``9`` (multi-order).
        """
        return await self._session.post(
            f"/rest/orders/contacts/{contact_id}/multi_order"
        )

    async def list_accounting_summaries(
        self,
        order_id: int | None = None,
        document_type: str | None = None,
        created_at_from: str | None = None,
        created_at_to: str | None = None,
        page: int = 1,
        items_per_page: int = 10,
    ) -> dict[str, Any]:
        """List document accounting summaries, with pagination.

        A document accounting summary is saved along with each reversal
        document (for invoices and credit notes).

        Note:
            The spec documents this endpoint's default ``itemsPerPage`` as
            ``10``, not this module's usual default of ``50``.

        Args:
            order_id: Filter by order ID.
            document_type: Filter by document type. One of
                ``"reversal_document"`` (invoice reversal) or
                ``"reversal_refund"`` (credit note reversal).
            created_at_from: Only return entries created on or after this
                date.
            created_at_to: Only return entries created on or before this
                date.
            page: Page number (1-indexed).
            items_per_page: Results per page.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching entries.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): ``StorageObject`` dicts, each with:

                - ``key`` (str): The storage key.
                - ``path`` (str): The storage path.
                - ``lastModified`` (str): ISO 8601 last-modified timestamp.
                - ``metaData`` (list[dict]): Arbitrary metadata entries.
                - ``eTag`` (str): The object's ETag.
                - ``size`` (int): Object size in bytes.
                - ``storageClass`` (str): The storage backend class.
                - ``body`` (str): The object body, if inlined.
                - ``contentType`` (str): MIME type.
                - ``contentLength`` (str): Content length.
        """
        params = self._build_params(
            None,
            orderId=order_id,
            documentType=document_type,
            createdAtFrom=created_at_from,
            createdAtTo=created_at_to,
            page=page,
            itemsPerPage=items_per_page,
        )
        return await self._session.get(
            "/rest/orders/documents/accounting_summary", params=params
        )

    async def paginate_accounting_summaries(
        self,
        order_id: int | None = None,
        document_type: str | None = None,
        created_at_from: str | None = None,
        created_at_to: str | None = None,
        items_per_page: int = 10,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every document accounting summary
        across all pages.

        Args:
            order_id: Filter by order ID.
            document_type: Filter by document type (see
                :meth:`list_accounting_summaries`).
            created_at_from: Only return entries created on or after this
                date.
            created_at_to: Only return entries created on or before this
                date.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual ``StorageObject`` dicts (see
            :meth:`list_accounting_summaries` for the field reference).
        """
        page = 1
        while True:
            result = await self.list_accounting_summaries(
                order_id=order_id,
                document_type=document_type,
                created_at_from=created_at_from,
                created_at_to=created_at_to,
                page=page,
                items_per_page=items_per_page,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_core.py -v`
Expected: all tests pass, including the 4 new ones.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.create_multi_order` — create a multi-order for a contact via `POST /rest/orders/contacts/{contactId}/multi_order`
- feat: `OrdersModule.list_accounting_summaries` / `paginate_accounting_summaries` — list/iterate document accounting summaries via `GET /rest/orders/documents/accounting_summary`
```

- [ ] **Step 6: Update `ROADMAP.md`**

```
| POST | `/rest/orders/contacts/{contactId}/multi_order` | Create a multi-order | **implemented** | `orders.create_multi_order` |
| GET | `/rest/orders/documents/accounting_summary` | List document accounting summaries | **implemented** | `orders.list_accounting_summaries` |
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/core.py tests/test_orders_core.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add multi-order creation and accounting summary listing"
```

---

## Task 3: `core.py` batch C — order booking, contact wish, currency update

**Files:**
- Modify: `src/plentymarkets/modules/orders/core.py`
- Test: `tests/test_orders_core.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `CoreMixin.book_order_in(order_id: int, delivery_note_number: str | None = None) -> dict[str, Any]`
  - `CoreMixin.get_contact_wish(order_id: int) -> dict[str, Any]`
  - `CoreMixin.update_order_currency(order_id: int, data: dict[str, Any]) -> dict[str, Any]`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_core.py`:

```python
async def test_book_order_in_posts_to_booking_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/booking",
        json={},
    )
    result = await orders.book_order_in(42)
    assert result == {}


async def test_book_order_in_sends_delivery_note_number(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/booking?deliveryNoteNumber=DN-1",
        json={},
    )
    await orders.book_order_in(42, delivery_note_number="DN-1")


async def test_get_contact_wish_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/contactWish",
        json={"text": "Please gift-wrap"},
    )
    result = await orders.get_contact_wish(42)
    assert result["text"] == "Please gift-wrap"


async def test_update_order_currency_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/currency",
        json={"id": 42, "statusId": 5.0},
    )
    result = await orders.update_order_currency(
        42, {"currency": "EUR", "exchangeRate": 1.0}
    )
    assert result["id"] == 42
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_core.py -v -k "book_order_in or contact_wish or update_order_currency"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `core.py`**

Add to `CoreMixin`, after `paginate_accounting_summaries`:

```python
    async def book_order_in(
        self, order_id: int, delivery_note_number: str | None = None
    ) -> dict[str, Any]:
        """Book an order in, e.g. an order of type reorder.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as ``OrderBooking`` — a bare placeholder schema with no
            fields. Response shape is unverified. Verify against a live
            system before relying on it.

        Args:
            order_id: The PlentyMarkets order ID.
            delivery_note_number: External delivery note number.

        Returns:
            The API's response dict; likely empty on success.
        """
        params = self._build_params(None, deliveryNoteNumber=delivery_note_number)
        return await self._session.post(
            f"/rest/orders/{order_id}/booking", params=params
        )

    async def get_contact_wish(self, order_id: int) -> dict[str, Any]:
        """Get the contact wish recorded on an order.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A dict with a single key:

            - ``text`` (str): The contact's wish text.
        """
        return await self._session.get(f"/rest/orders/{order_id}/contactWish")

    async def update_order_currency(
        self, order_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update the currency of an order.

        Note:
            PlentyMarkets' published OpenAPI spec declares no request body
            schema for this endpoint at all. Based on the endpoint's
            description ("The currency and the exchange rate must be
            specified"), ``data`` likely needs ``currency`` (ISO 4217 code)
            and ``exchangeRate`` (float) keys. Verify against a live system
            before relying on this shape.

        Args:
            order_id: The PlentyMarkets order ID.
            data: Currency update payload — see the Note above.

        Returns:
            The updated order dict (see :meth:`get` for the field
            reference).
        """
        return await self._session.put(
            f"/rest/orders/{order_id}/currency", json=data
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_core.py -v`
Expected: all tests pass, including the 4 new ones.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.book_order_in` — book an order in via `POST /rest/orders/{orderId}/booking`
- feat: `OrdersModule.get_contact_wish` — get an order's contact wish via `GET /rest/orders/{orderId}/contactWish`
- feat: `OrdersModule.update_order_currency` — update an order's currency via `PUT /rest/orders/{orderId}/currency`
```

- [ ] **Step 6: Update `ROADMAP.md`**

```
| POST | `/rest/orders/{orderId}/booking` | Book an order in | **implemented** | `orders.book_order_in` |
| GET | `/rest/orders/{orderId}/contactWish` | Get a contact wish | **implemented** | `orders.get_contact_wish` |
| PUT | `/rest/orders/{orderId}/currency` | Update the order currency | **implemented** | `orders.update_order_currency` |
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/core.py tests/test_orders_core.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order booking, contact wish, and currency update"
```

---

## Task 4: `core.py` batch D — deprecated outgoing-stock endpoints

**Files:**
- Modify: `src/plentymarkets/modules/orders/core.py`
- Test: `tests/test_orders_core.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `CoreMixin.revert_item_outgoing_stock(order_item_id: int, quantity: float, warehouse_id: int, batch: str | None = None, best_before_date: str | None = None, reason_id: int | None = None) -> dict[str, Any]`
  - `CoreMixin.book_out_order_items(order_id: int, date: str | None = None) -> dict[str, Any]`
  - `CoreMixin.revert_order_outgoing_stock(order_id: int) -> dict[str, Any]`

All three endpoints in this task are marked deprecated in the spec.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_core.py`:

```python
async def test_revert_item_outgoing_stock_sends_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/items/outgoing_stocks",
        json={},
    )
    result = await orders.revert_item_outgoing_stock(
        order_item_id=10, quantity=2.0, warehouse_id=1
    )
    assert result == {}
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "id": 10,
        "quantity": 2.0,
        "warehouseId": 1,
    }


async def test_book_out_order_items_posts_to_outgoing_stocks_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/outgoing_stocks",
        json={},
    )
    result = await orders.book_out_order_items(42)
    assert result == {}


async def test_book_out_order_items_sends_date(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/outgoing_stocks?date=2026-07-13",
        json={},
    )
    await orders.book_out_order_items(42, date="2026-07-13")


async def test_revert_order_outgoing_stock_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/42/outgoing_stocks",
        json={},
    )
    result = await orders.revert_order_outgoing_stock(42)
    assert result == {}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_core.py -v -k "outgoing_stock"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `core.py`**

Add to `CoreMixin`, after `update_order_currency`:

```python
    async def revert_item_outgoing_stock(
        self,
        order_item_id: int,
        quantity: float,
        warehouse_id: int,
        batch: str | None = None,
        best_before_date: str | None = None,
        reason_id: int | None = None,
    ) -> dict[str, Any]:
        """Revert the outgoing-stock booking of one order item.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``POST /rest/{orderType}/{orderId}/cancel_booking`` instead.

            The spec's JSON Schema marks ``quantity`` and ``warehouse_id``
            as required, even though their field descriptions call them
            "optional" — a contradiction in the published spec. The
            ``required`` array is treated as authoritative here.

        Args:
            order_item_id: The order item ID to book back in.
            quantity: The quantity to book back in.
            warehouse_id: The warehouse ID to book the quantity back into.
            batch: Batch identifier of the stock being reverted.
            best_before_date: Best-before date of the stock being reverted,
                ISO 8601.
            reason_id: ID of the reason for the reversal.

        Returns:
            Empty dict on success (the spec documents no response content).
        """
        data: dict[str, Any] = {
            "id": order_item_id,
            "quantity": quantity,
            "warehouseId": warehouse_id,
        }
        if batch is not None:
            data["batch"] = batch
        if best_before_date is not None:
            data["bestBeforeDate"] = best_before_date
        if reason_id is not None:
            data["reasonId"] = reason_id
        return await self._session.delete(
            "/rest/orders/items/outgoing_stocks", json=data
        )

    async def book_out_order_items(
        self, order_id: int, date: str | None = None
    ) -> dict[str, Any]:
        """Book out the order items of an order.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``POST /rest/{orderType}/{orderId}/book`` instead.

        Args:
            order_id: The PlentyMarkets order ID.
            date: Booking date, ISO 8601. Defaults to now if omitted.

        Returns:
            Empty dict on success (the spec documents no response content).
        """
        params = self._build_params(None, date=date)
        return await self._session.post(
            f"/rest/orders/{order_id}/outgoing_stocks", params=params
        )

    async def revert_order_outgoing_stock(self, order_id: int) -> dict[str, Any]:
        """Revert the outgoing-stock booking of an order.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``POST /rest/{orderType}/{orderId}/cancel_booking`` instead.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            Empty dict on success (the spec documents no response content).
        """
        return await self._session.delete(f"/rest/orders/{order_id}/outgoing_stocks")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_core.py -v`
Expected: all tests pass, including the 4 new ones. Then run the full file once more to
confirm Task 1-4's combined 16 new tests all pass together: `uv run pytest tests/test_orders_core.py -v`.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.revert_item_outgoing_stock` — revert an order item's outgoing-stock booking via `DELETE /rest/orders/items/outgoing_stocks` (deprecated by PlentyMarkets; use `POST /rest/{orderType}/{orderId}/cancel_booking`)
- feat: `OrdersModule.book_out_order_items` — book out an order's items via `POST /rest/orders/{orderId}/outgoing_stocks` (deprecated by PlentyMarkets; use `POST /rest/{orderType}/{orderId}/book`)
- feat: `OrdersModule.revert_order_outgoing_stock` — revert an order's outgoing-stock booking via `DELETE /rest/orders/{orderId}/outgoing_stocks` (deprecated by PlentyMarkets; use `POST /rest/{orderType}/{orderId}/cancel_booking`)
- `Order` reaches 55/307 endpoint coverage under the `Order` API tag (core metadata batch A-D: batch fetch, contact/multi orders, accounting summaries, booking, contact wish, currency, outgoing stocks)
```

- [ ] **Step 6: Update `ROADMAP.md`**

```
| DELETE | `/rest/orders/items/outgoing_stocks` | Revert outgoing stock for order items | **implemented** | `orders.revert_item_outgoing_stock` |
| POST | `/rest/orders/{orderId}/outgoing_stocks` | Book out order items | **implemented** | `orders.book_out_order_items` |
| DELETE | `/rest/orders/{orderId}/outgoing_stocks` | Revert outgoing stock | **implemented** | `orders.revert_order_outgoing_stock` |
```

Also update the top-of-file summary: `**150 / 1837**` → `**160 / 1837**`, and the `Order` row
`**45/307**` → `**55/307**` (both the summary table row and the `### Order` section's own
`45/307 implemented.` line).

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/core.py tests/test_orders_core.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add deprecated outgoing-stock booking endpoints"
```

---

## Task 5: `dates.py` batch A — order-item dates addressed by date ID

**Files:**
- Modify: `src/plentymarkets/modules/orders/dates.py`
- Test: `tests/test_orders_dates.py`

**Interfaces:**
- Consumes: `OrdersBase._session`
- Produces:
  - `DatesMixin.create_item_date(order_item_id: int, type_id: int, date: str) -> dict[str, Any]`
  - `DatesMixin.delete_item_date(date_id: int) -> dict[str, Any]`
  - `DatesMixin.get_item_date(date_id: int) -> dict[str, Any]`
  - `DatesMixin.update_item_date(date_id: int, date: str) -> dict[str, Any]`

All four endpoints in this task are marked deprecated in the spec (use
`PUT /rest/orders/{orderId}`).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_dates.py`:

```python
async def test_create_item_date_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/items/dates",
        json={"id": 1, "orderItemId": 10, "typeId": 9},
    )
    result = await orders.create_item_date(order_item_id=10, type_id=9, date="2026-07-13")
    assert result["id"] == 1
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderItemId": 10,
        "typeId": 9,
        "date": "2026-07-13",
    }


async def test_delete_item_date_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/items/dates/1",
        json={},
    )
    result = await orders.delete_item_date(1)
    assert result == {}


async def test_get_item_date_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/dates/1",
        json={"id": 1, "orderItemId": 10, "typeId": 9},
    )
    result = await orders.get_item_date(1)
    assert result["orderItemId"] == 10


async def test_update_item_date_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/items/dates/1",
        json={"id": 1, "orderItemId": 10, "typeId": 9},
    )
    result = await orders.update_item_date(1, date="2026-08-01")
    assert result["id"] == 1
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"date": "2026-08-01"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_dates.py -v -k "item_date"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `dates.py`**

Add to `DatesMixin`, after `get_order_date` (the last existing method):

```python
    async def create_item_date(
        self, order_item_id: int, type_id: int, date: str
    ) -> dict[str, Any]:
        """Create a date for an order item, addressed by a new date ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.
            See the caveat on :meth:`list_order_dates` regarding the
            published schema's missing date-value field — the same applies
            here (``OrderItemDate`` has no value field either).

        Args:
            order_item_id: The order item ID.
            type_id: The order date type ID (see :meth:`list_date_types`).
            date: The date value, ISO 8601.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The order-item date record ID.
            - ``orderItemId`` (int): The order item this date belongs to.
            - ``typeId`` (int): The date type ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.post(
            "/rest/orders/items/dates",
            json={"orderItemId": order_item_id, "typeId": type_id, "date": date},
        )

    async def delete_item_date(self, date_id: int) -> dict[str, Any]:
        """Delete a date of an order item by its own date ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            date_id: The order-item date record ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(f"/rest/orders/items/dates/{date_id}")

    async def get_item_date(self, date_id: int) -> dict[str, Any]:
        """Get a date of an order item by its own date ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            date_id: The order-item date record ID.

        Returns:
            An order-item date dict (see :meth:`create_item_date` for the
            field reference).
        """
        return await self._session.get(f"/rest/orders/items/dates/{date_id}")

    async def update_item_date(self, date_id: int, date: str) -> dict[str, Any]:
        """Update a date of an order item by its own date ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            date_id: The order-item date record ID.
            date: The new date value, ISO 8601.

        Returns:
            The updated order-item date dict (see :meth:`create_item_date`
            for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/items/dates/{date_id}", json={"date": date}
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_dates.py -v`
Expected: all tests pass, including the 4 new ones.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.create_item_date` — create a date for an order item via `POST /rest/orders/items/dates` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.delete_item_date` — delete a date of an order item via `DELETE /rest/orders/items/dates/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.get_item_date` — get a date of an order item via `GET /rest/orders/items/dates/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.update_item_date` — update a date of an order item via `PUT /rest/orders/items/dates/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
```

- [ ] **Step 6: Update `ROADMAP.md`**

```
| POST | `/rest/orders/items/dates` | Create a date for an order item | **implemented** | `orders.create_item_date` |
| DELETE | `/rest/orders/items/dates/{id}` | Delete a date of an order item | **implemented** | `orders.delete_item_date` |
| GET | `/rest/orders/items/dates/{id}` | Get date of an order item | **implemented** | `orders.get_item_date` |
| PUT | `/rest/orders/items/dates/{id}` | Update a date of an order item | **implemented** | `orders.update_item_date` |
```

(Keep the existing `deprecated (use PUT /rest/orders/{orderId})` wording folded into these rows'
Status column alongside `**implemented**`, e.g. `**implemented** (deprecated by PlentyMarkets)`.)

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/dates.py tests/test_orders_dates.py \
        CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order-item dates addressed by date ID"
```

---

## Task 6: `dates.py` batch B — order-item dates addressed by type, and docstring fix

**Files:**
- Modify: `src/plentymarkets/modules/orders/dates.py`
- Modify: `src/plentymarkets/modules/orders/transactions.py`
- Test: `tests/test_orders_dates.py`

**Interfaces:**
- Consumes: `OrdersBase._session`
- Produces:
  - `DatesMixin.list_item_dates(order_item_id: int) -> list[dict[str, Any]]`
  - `DatesMixin.delete_item_date_by_type(order_item_id: int, type_id: int) -> dict[str, Any]`
  - `DatesMixin.get_item_date_by_type(order_item_id: int, type_id: int) -> dict[str, Any]`
  - `DatesMixin.create_item_date_by_type(order_item_id: int, type_id: int, date: str) -> dict[str, Any]`
  - `DatesMixin.update_item_date_by_type(order_item_id: int, type_id: int, date: str) -> dict[str, Any]`

All five endpoints in this task are marked deprecated in the spec (use
`PUT /rest/orders/{orderId}`).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_dates.py`:

```python
async def test_list_item_dates_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/10/dates",
        json=[{"id": 1, "orderItemId": 10, "typeId": 9}],
    )
    result = await orders.list_item_dates(10)
    assert result[0]["typeId"] == 9


async def test_delete_item_date_by_type_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/items/10/dates/9",
        json={},
    )
    result = await orders.delete_item_date_by_type(10, 9)
    assert result == {}


async def test_get_item_date_by_type_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/10/dates/9",
        json={"id": 1, "orderItemId": 10, "typeId": 9},
    )
    result = await orders.get_item_date_by_type(10, 9)
    assert result["id"] == 1


async def test_create_item_date_by_type_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/items/10/dates/9",
        json={"id": 1, "orderItemId": 10, "typeId": 9},
    )
    result = await orders.create_item_date_by_type(10, 9, date="2026-07-13")
    assert result["id"] == 1
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderItemId": 10,
        "typeId": 9,
        "date": "2026-07-13",
    }


async def test_update_item_date_by_type_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/items/10/dates/9",
        json={"id": 1, "orderItemId": 10, "typeId": 9},
    )
    result = await orders.update_item_date_by_type(10, 9, date="2026-08-01")
    assert result["id"] == 1
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"date": "2026-08-01"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_dates.py -v -k "by_type"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `dates.py`**

Add to `DatesMixin`, after `update_item_date`:

```python
    async def list_item_dates(self, order_item_id: int) -> list[dict[str, Any]]:
        """List all dates recorded on an order item.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.

        Returns:
            A list of order-item date dicts (see :meth:`create_item_date`
            for the field reference).
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/items/{order_item_id}/dates"
        )

    async def delete_item_date_by_type(
        self, order_item_id: int, type_id: int
    ) -> dict[str, Any]:
        """Delete a date of an order item, addressed by item and date type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order date type ID (see :meth:`list_date_types`).

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/orders/items/{order_item_id}/dates/{type_id}"
        )

    async def get_item_date_by_type(
        self, order_item_id: int, type_id: int
    ) -> dict[str, Any]:
        """Get a date of an order item, addressed by item and date type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order date type ID (see :meth:`list_date_types`).

        Returns:
            An order-item date dict (see :meth:`create_item_date` for the
            field reference).
        """
        return await self._session.get(
            f"/rest/orders/items/{order_item_id}/dates/{type_id}"
        )

    async def create_item_date_by_type(
        self, order_item_id: int, type_id: int, date: str
    ) -> dict[str, Any]:
        """Create a date for an order item, addressed by item and date type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order date type ID (see :meth:`list_date_types`).
            date: The date value, ISO 8601.

        Returns:
            The created order-item date dict (see :meth:`create_item_date`
            for the field reference).
        """
        return await self._session.post(
            f"/rest/orders/items/{order_item_id}/dates/{type_id}",
            json={"orderItemId": order_item_id, "typeId": type_id, "date": date},
        )

    async def update_item_date_by_type(
        self, order_item_id: int, type_id: int, date: str
    ) -> dict[str, Any]:
        """Update a date of an order item, addressed by item and date type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order date type ID (see :meth:`list_date_types`).
            date: The new date value, ISO 8601.

        Returns:
            The updated order-item date dict (see :meth:`create_item_date`
            for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/items/{order_item_id}/dates/{type_id}",
            json={"date": date},
        )
```

- [ ] **Step 4: Fix `transactions.py`'s class docstring**

`TransactionsMixin`'s class docstring currently claims order-item dates/properties are
"intentionally not implemented here" because they're deprecated. That statement is now false.
In `src/plentymarkets/modules/orders/transactions.py`, replace:

```python
    """Order item transaction (stock movement) management.

    These methods manage transactions (stock movements) recorded against
    order items, via the flat `/rest/orders/items/transactions/*` family
    (addressed by transaction ID) and the `/rest/orders/items/{orderItemId}
    /transactions` family (scoped to one order item). Both are current
    (not deprecated), unlike the sibling order-item dates/properties
    families, which PlentyMarkets has deprecated in favor of
    `PUT /rest/orders/{orderId}` and are intentionally not implemented here.
    """
```

with:

```python
    """Order item transaction (stock movement) management.

    These methods manage transactions (stock movements) recorded against
    order items, via the flat `/rest/orders/items/transactions/*` family
    (addressed by transaction ID) and the `/rest/orders/items/{orderItemId}
    /transactions` family (scoped to one order item). Both are current
    (not deprecated), unlike the sibling order-item dates (`DatesMixin`)
    and order/order-item properties (`PropertiesMixin`) families, which
    PlentyMarkets has deprecated in favor of `PUT /rest/orders/{orderId}`
    but which this package still implements for full endpoint coverage.
    """
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_dates.py tests/test_orders_transactions.py -v`
Expected: all tests pass, including the 5 new ones. `transactions.py`'s existing tests are
unaffected by the docstring-only change.

- [ ] **Step 6: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_item_dates` — list all dates of an order item via `GET /rest/orders/items/{orderItemId}/dates` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.delete_item_date_by_type` — delete a date of an order item by type via `DELETE /rest/orders/items/{orderItemId}/dates/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.get_item_date_by_type` — get a date of an order item by type via `GET /rest/orders/items/{orderItemId}/dates/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.create_item_date_by_type` — create a date for an order item by type via `POST /rest/orders/items/{orderItemId}/dates/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.update_item_date_by_type` — update a date of an order item by type via `PUT /rest/orders/items/{orderItemId}/dates/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- `Order` reaches 64/307 endpoint coverage under the `Order` API tag (order-item dates milestone)
```

- [ ] **Step 7: Update `ROADMAP.md`**

```
| GET | `/rest/orders/items/{orderItemId}/dates` | List all dates of an order item | **implemented** | `orders.list_item_dates` |
| DELETE | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Delete a date of an order item by order item and date type | **implemented** | `orders.delete_item_date_by_type` |
| GET | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Get a date of an order item by order item and date type | **implemented** | `orders.get_item_date_by_type` |
| POST | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Create a date for an order item by order item and date type | **implemented** | `orders.create_item_date_by_type` |
| PUT | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Update a date of an order item by order item and date type | **implemented** | `orders.update_item_date_by_type` |
```

Update the top-of-file summary: `**160 / 1837**` → `**169 / 1837**`, and the `Order` row
`**55/307**` → `**64/307**` (both places).

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/modules/orders/dates.py \
        src/plentymarkets/modules/orders/transactions.py \
        tests/test_orders_dates.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order-item dates addressed by item and date type"
```

---

## Task 7: `properties.py` — new file, property types CRUD

**Files:**
- Create: `src/plentymarkets/modules/orders/properties.py`
- Modify: `src/plentymarkets/modules/orders/__init__.py`
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Test: Create `tests/test_orders_properties.py`

**Interfaces:**
- Consumes: `OrdersBase._session` (existing)
- Produces:
  - `PropertiesMixin` class (new), added to `OrdersModule`'s bases
  - `PropertiesMixin.list_property_types(lang: list[str] | None = None) -> list[dict[str, Any]]`
  - `PropertiesMixin.create_property_type(data: OrderPropertyTypeCreatePayload) -> dict[str, Any]`
  - `PropertiesMixin.delete_property_type(type_id: int) -> dict[str, Any]`
  - `PropertiesMixin.get_property_type(type_id: int, lang: list[str] | None = None) -> dict[str, Any]`
  - `PropertiesMixin.update_property_type(type_id: int, data: OrderPropertyTypeUpdatePayload) -> dict[str, Any]`
  - `OrderPropertyTypeNamePayload`, `OrderPropertyTypeCreatePayload`, `OrderPropertyTypeUpdatePayload` TypedDicts, exported from `plentymarkets`

None of these 5 endpoints are deprecated.

- [ ] **Step 1: Add the 3 TypedDicts to `_types.py`**

In `src/plentymarkets/_types.py`, add immediately after `OrderTransactionsCreatePayload` (still
inside the `# --- Orders (/rest/orders) ---` section):

```python
class OrderPropertyTypeNamePayload(TypedDict, total=False):
    """One entry in the ``names`` list for
    :meth:`OrdersModule.create_property_type` and
    :meth:`OrdersModule.update_property_type`
    (``POST``/``PUT /rest/orders/properties/types(/{typeId})``).

    Keys:
        lang: Two-letter ISO 639-1 language code, e.g. ``"en"``, ``"de"``.
            **Required.**
        name: Translated display name for the property type in this
            language. **Required.**
    """

    lang: Required[str]
    name: Required[str]


class OrderPropertyTypeCreatePayload(TypedDict, total=False):
    """Payload for :meth:`OrdersModule.create_property_type`
    (``POST /rest/orders/properties/types``).

    Note:
        PlentyMarkets requires both a singular ``lang``/``name`` pair *and*
        a ``names`` array of the same shape simultaneously — redundant-
        looking, but both are marked required in the spec. Implemented
        literally; verify against a live system before assuming one can be
        omitted.

    Keys:
        lang: Two-letter ISO 639-1 language code for ``name``. **Required.**
        name: Translated display name for the property type. **Required.**
        names: List of translated names in other languages. Use
            :class:`OrderPropertyTypeNamePayload` for IDE autocomplete.
            **Required.**
        cast: Data type of the property's values. One of ``"string"``,
            ``"int"``, ``"numeric"``, ``"bool"``, or
            ``"enum(val1,val2,val3,...)"``.
        position: Sort position.
    """

    lang: Required[str]
    name: Required[str]
    names: Required[list[OrderPropertyTypeNamePayload]]
    cast: NotRequired[str]
    position: NotRequired[int]


class OrderPropertyTypeUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`OrdersModule.update_property_type`
    (``PUT /rest/orders/properties/types/{typeId}``).

    Keys:
        lang: Two-letter ISO 639-1 language code for ``name``. **Required.**
        name: Translated display name for the property type. **Required.**
        names: List of translated names to create/update. Use
            :class:`OrderPropertyTypeNamePayload` for IDE autocomplete.
        position: Sort position.
    """

    lang: Required[str]
    name: Required[str]
    names: NotRequired[list[OrderPropertyTypeNamePayload]]
    position: NotRequired[int]
```

- [ ] **Step 2: Export the 3 TypedDicts from `src/plentymarkets/__init__.py`**

Add `OrderPropertyTypeCreatePayload`, `OrderPropertyTypeNamePayload`,
`OrderPropertyTypeUpdatePayload` to both the `from ._types import (...)` block and `__all__`,
alphabetized alongside the existing `Order*` entries (immediately after
`OrderCreatePayload`/before `OrderStatusNamePayload` in both places, keeping the file's
alphabetical-within-prefix ordering).

- [ ] **Step 3: Write the failing tests**

Create `tests/test_orders_properties.py`:

```python
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


# --- property types ---


async def test_list_property_types_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/properties/types",
        json=[{"id": 1, "isErasable": False, "position": 1, "cast": "string"}],
    )
    result = await orders.list_property_types()
    assert result[0]["id"] == 1


async def test_list_property_types_sends_lang_filter(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/properties/types?lang=en%2Cde",
        json=[],
    )
    await orders.list_property_types(lang=["en", "de"])


async def test_create_property_type_posts_data(httpx_mock, orders):
    payload = {
        "lang": "en",
        "name": "Gift wrap",
        "names": [{"lang": "de", "name": "Geschenkverpackung"}],
    }
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/properties/types",
        json={"id": 1001, "isErasable": True, "position": 1},
    )
    result = await orders.create_property_type(payload)
    assert result["id"] == 1001


async def test_delete_property_type_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/properties/types/1001",
        json={},
    )
    result = await orders.delete_property_type(1001)
    assert result == {}


async def test_get_property_type_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/properties/types/1001",
        json={"id": 1001, "isErasable": True, "position": 1},
    )
    result = await orders.get_property_type(1001)
    assert result["id"] == 1001


async def test_update_property_type_puts_data(httpx_mock, orders):
    payload = {"lang": "en", "name": "Gift wrap (updated)"}
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/properties/types/1001",
        json={"id": 1001, "isErasable": True, "position": 1},
    )
    result = await orders.update_property_type(1001, payload)
    assert result["id"] == 1001
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_properties.py -v`
Expected: FAIL — `properties.py` does not exist yet / `OrdersModule` has no `list_property_types`.

- [ ] **Step 5: Create `properties.py`**

```python
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import OrderPropertyTypeCreatePayload, OrderPropertyTypeUpdatePayload

from ._base import OrdersBase


class PropertiesMixin(OrdersBase):
    """Order property types, and order/order-item property values.

    Property *types* (`/rest/orders/properties/types*`) are current, not
    deprecated. The order-level and order-item-level property *value*
    families below them are all deprecated by PlentyMarkets in favor of
    `PUT /rest/orders/{orderId}`, but are still implemented here for full
    endpoint coverage — see each method's docstring Note for the
    replacement route.
    """

    async def list_property_types(
        self, lang: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List all order property types and their translated names.

        Args:
            lang: Restrict the response to these languages. Defaults to all
                languages if omitted.

        Returns:
            A list of property type dicts, each with:

            - ``id`` (int): The property type ID. IDs below 1000 are
              PlentyMarkets system defaults and cannot be deleted.
            - ``isErasable`` (bool): Whether this type can be deleted.
            - ``position`` (int): Display sort position.
            - ``cast`` (str): Data type of the property's values. One of
              ``"string"``, ``"int"``, ``"numeric"``, ``"bool"``, or
              ``"enum(val1,val2,val3,...)"``.
        """
        params = self._build_params(None, lang=",".join(lang) if lang else None)
        return await self._session.get(  # type: ignore[return-value]
            "/rest/orders/properties/types", params=params
        )

    async def create_property_type(
        self, data: OrderPropertyTypeCreatePayload
    ) -> dict[str, Any]:
        """Create a new order property type.

        After creation, the property type can be linked to an order via its
        ID (see :meth:`create_order_property`).

        Args:
            data: Property type payload. Use
                :class:`~plentymarkets._types.OrderPropertyTypeCreatePayload`
                for IDE autocomplete. Required keys: ``lang``, ``name``,
                ``names``.

        Returns:
            The created property type dict (see :meth:`list_property_types`
            for the field reference).
        """
        return await self._session.post(
            "/rest/orders/properties/types", json=data
        )

    async def delete_property_type(self, type_id: int) -> dict[str, Any]:
        """Delete an order property type and all its translated names.

        Note:
            Property type IDs below 1000 are PlentyMarkets system defaults
            and cannot be deleted.

        Args:
            type_id: The property type ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(f"/rest/orders/properties/types/{type_id}")

    async def get_property_type(
        self, type_id: int, lang: list[str] | None = None
    ) -> dict[str, Any]:
        """Get a single order property type by ID.

        Args:
            type_id: The property type ID.
            lang: Restrict the response to these languages. Defaults to all
                languages if omitted.

        Returns:
            A property type dict (see :meth:`list_property_types` for the
            field reference).
        """
        params = self._build_params(None, lang=",".join(lang) if lang else None)
        return await self._session.get(
            f"/rest/orders/properties/types/{type_id}", params=params
        )

    async def update_property_type(
        self, type_id: int, data: OrderPropertyTypeUpdatePayload
    ) -> dict[str, Any]:
        """Update an order property type and its translated names.

        Note:
            Names for languages that don't yet exist are created; existing
            ones are updated.

        Args:
            type_id: The property type ID.
            data: Property type payload. Use
                :class:`~plentymarkets._types.OrderPropertyTypeUpdatePayload`
                for IDE autocomplete. Required keys: ``lang``, ``name``.

        Returns:
            The updated property type dict (see :meth:`list_property_types`
            for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/properties/types/{type_id}", json=data
        )
```

- [ ] **Step 6: Wire `PropertiesMixin` into `OrdersModule`**

In `src/plentymarkets/modules/orders/__init__.py`, replace:

```python
from .core import CoreMixin
from .dates import DatesMixin
from .order_items import ItemsMixin
from .reorders import ReordersMixin
from .status_history import StatusHistoryMixin
from .statuses import StatusMixin
from .transactions import TransactionsMixin

__all__ = ["OrdersModule"]


class OrdersModule(
    CoreMixin,
    StatusMixin,
    StatusHistoryMixin,
    DatesMixin,
    TransactionsMixin,
    ItemsMixin,
    ReordersMixin,
    OrdersBase,
):
```

with:

```python
from .core import CoreMixin
from .dates import DatesMixin
from .order_items import ItemsMixin
from .properties import PropertiesMixin
from .reorders import ReordersMixin
from .status_history import StatusHistoryMixin
from .statuses import StatusMixin
from .transactions import TransactionsMixin

__all__ = ["OrdersModule"]


class OrdersModule(
    CoreMixin,
    StatusMixin,
    StatusHistoryMixin,
    DatesMixin,
    TransactionsMixin,
    ItemsMixin,
    ReordersMixin,
    PropertiesMixin,
    OrdersBase,
):
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_properties.py -v`
Expected: all 6 tests pass. Then run `uv run pytest` (full suite) to confirm no regressions from
the `__init__.py` change.

- [ ] **Step 8: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_property_types` — list order property types via `GET /rest/orders/properties/types`
- feat: `OrdersModule.create_property_type` — create an order property type via `POST /rest/orders/properties/types`
- feat: `OrdersModule.delete_property_type` — delete an order property type via `DELETE /rest/orders/properties/types/{typeId}`
- feat: `OrdersModule.get_property_type` — get one order property type via `GET /rest/orders/properties/types/{typeId}`
- feat: `OrdersModule.update_property_type` — update an order property type via `PUT /rest/orders/properties/types/{typeId}`
- feat: `OrderPropertyTypeNamePayload`, `OrderPropertyTypeCreatePayload`, `OrderPropertyTypeUpdatePayload` — TypedDicts for `create_property_type`/`update_property_type`
- refactor: `modules/orders/` gains a `properties.py` mixin (`PropertiesMixin`) — no public API change
```

- [ ] **Step 9: Update `ROADMAP.md`**

```
| GET | `/rest/orders/properties/types` | List order property types | **implemented** | `orders.list_property_types` |
| POST | `/rest/orders/properties/types` | Create order property type | **implemented** | `orders.create_property_type` |
| DELETE | `/rest/orders/properties/types/{typeId}` | Delete property type | **implemented** | `orders.delete_property_type` |
| GET | `/rest/orders/properties/types/{typeId}` | Get property type | **implemented** | `orders.get_property_type` |
| PUT | `/rest/orders/properties/types/{typeId}` | Update property type | **implemented** | `orders.update_property_type` |
```

Update the top-of-file summary: `**169 / 1837**` → `**174 / 1837**`, and the `Order` row
`**64/307**` → `**69/307**` (both places).

- [ ] **Step 10: Commit**

```bash
git add src/plentymarkets/modules/orders/properties.py \
        src/plentymarkets/modules/orders/__init__.py \
        src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        tests/test_orders_properties.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order property types CRUD"
```

---

## Task 8: `properties.py` — order-level property values

**Files:**
- Modify: `src/plentymarkets/modules/orders/properties.py`
- Test: `tests/test_orders_properties.py`

**Interfaces:**
- Consumes: `OrdersBase._session`
- Produces:
  - `PropertiesMixin.delete_order_property(property_id: int) -> dict[str, Any]`
  - `PropertiesMixin.update_order_property(property_id: int, type_id: int, value: str) -> dict[str, Any]`
  - `PropertiesMixin.create_order_property(order_id: int, type_id: int, value: str) -> dict[str, Any]`
  - `PropertiesMixin.list_order_properties(order_id: int, type_id: int) -> list[dict[str, Any]]`
  - `PropertiesMixin.delete_order_property_by_type(order_id: int, type_id: int) -> dict[str, Any]`
  - `PropertiesMixin.update_order_property_by_type(order_id: int, type_id: int, value: str) -> dict[str, Any]`

All six endpoints in this task are marked deprecated in the spec (use
`PUT /rest/orders/{orderId}`) — **correction to `ROADMAP.md`**: its table currently shows these
6 rows as plain `planned`, missing the `deprecated (...)` annotation their sibling item-level
rows already carry. Verified directly against the live spec's `description` field. Fix the
Status column wording for these 6 rows alongside marking them implemented (see Step 9).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_properties.py`:

```python
# --- order-level property values ---


async def test_delete_order_property_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/properties/501",
        json={},
    )
    result = await orders.delete_order_property(501)
    assert result == {}


async def test_update_order_property_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/properties/501",
        json={"id": 501, "orderId": 42, "typeId": 1, "value": "A1"},
    )
    result = await orders.update_order_property(501, type_id=1, value="A1")
    assert result["value"] == "A1"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"id": 501, "typeId": 1, "value": "A1"}


async def test_create_order_property_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/properties",
        json={"id": 501, "orderId": 42, "typeId": 1, "value": "A1"},
    )
    result = await orders.create_order_property(42, type_id=1, value="A1")
    assert result["id"] == 501
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderId": 42,
        "typeId": 1,
        "value": "A1",
    }


async def test_list_order_properties_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/properties/1",
        json=[{"id": 501, "orderId": 42, "typeId": 1, "value": "A1"}],
    )
    result = await orders.list_order_properties(42, type_id=1)
    assert result[0]["value"] == "A1"


async def test_delete_order_property_by_type_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/42/properties/1",
        json={},
    )
    result = await orders.delete_order_property_by_type(42, type_id=1)
    assert result == {}


async def test_update_order_property_by_type_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/properties/1",
        json={"id": 501, "orderId": 42, "typeId": 1, "value": "A2"},
    )
    result = await orders.update_order_property_by_type(42, type_id=1, value="A2")
    assert result["value"] == "A2"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderId": 42,
        "typeId": 1,
        "value": "A2",
    }
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_properties.py -v -k "order_property or order_properties"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `properties.py`**

Add to `PropertiesMixin`, after `update_property_type`:

```python
    async def delete_order_property(self, property_id: int) -> dict[str, Any]:
        """Delete a property of an order, addressed by the property's own ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            property_id: The order property record ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(f"/rest/orders/properties/{property_id}")

    async def update_order_property(
        self, property_id: int, type_id: int, value: str
    ) -> dict[str, Any]:
        """Update the value of an order property, addressed by its own ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            property_id: The order property record ID.
            type_id: The property type ID (see :meth:`list_property_types`).
            value: The new property value.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The order property record ID.
            - ``orderId`` (int): The order this property belongs to.
            - ``typeId`` (int): The property type ID.
            - ``value`` (str): The property value.
        """
        return await self._session.put(
            f"/rest/orders/properties/{property_id}",
            json={"id": property_id, "typeId": type_id, "value": value},
        )

    async def create_order_property(
        self, order_id: int, type_id: int, value: str
    ) -> dict[str, Any]:
        """Create a property and link it to an order.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_id: The PlentyMarkets order ID.
            type_id: The property type ID (see :meth:`list_property_types`).
            value: The property value.

        Returns:
            The created order property dict (see
            :meth:`update_order_property` for the field reference).
        """
        return await self._session.post(
            f"/rest/orders/{order_id}/properties",
            json={"orderId": order_id, "typeId": type_id, "value": value},
        )

    async def list_order_properties(
        self, order_id: int, type_id: int
    ) -> list[dict[str, Any]]:
        """List properties of an order, optionally filtered by property type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``GET /rest/orders/{orderId}`` instead. The spec's path
            template literally reads ``{typeId?}`` (implying an optional
            segment) yet marks the parameter ``required: true`` — a
            contradiction in the published spec. ``type_id`` is implemented
            as required here; verify against a live system whether a
            no-segment call (all properties, unfiltered) is also accepted.

        Args:
            order_id: The PlentyMarkets order ID.
            type_id: The property type ID to filter by (see
                :meth:`list_property_types`).

        Returns:
            A list of order property dicts (see :meth:`update_order_property`
            for the field reference).
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/properties/{type_id}"
        )

    async def delete_order_property_by_type(
        self, order_id: int, type_id: int
    ) -> dict[str, Any]:
        """Delete a property of an order, addressed by order and property type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_id: The PlentyMarkets order ID.
            type_id: The property type ID (see :meth:`list_property_types`).

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/orders/{order_id}/properties/{type_id}"
        )

    async def update_order_property_by_type(
        self, order_id: int, type_id: int, value: str
    ) -> dict[str, Any]:
        """Update the value of a property already linked to an order,
        addressed by order and property type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_id: The PlentyMarkets order ID.
            type_id: The property type ID (see :meth:`list_property_types`).
            value: The new property value.

        Returns:
            The updated order property dict (see
            :meth:`update_order_property` for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/{order_id}/properties/{type_id}",
            json={"orderId": order_id, "typeId": type_id, "value": value},
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_properties.py -v`
Expected: all tests pass, including the 6 new ones.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.delete_order_property` — delete a property of an order by property ID via `DELETE /rest/orders/properties/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.update_order_property` — update a property of an order by property ID via `PUT /rest/orders/properties/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.create_order_property` — create and link a property to an order via `POST /rest/orders/{orderId}/properties` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.list_order_properties` — list properties of an order via `GET /rest/orders/{orderId}/properties/{typeId}` (deprecated by PlentyMarkets; use `GET /rest/orders/{orderId}`)
- feat: `OrdersModule.delete_order_property_by_type` — delete a property of an order by order and type via `DELETE /rest/orders/{orderId}/properties/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.update_order_property_by_type` — update a property of an order by order and type via `PUT /rest/orders/{orderId}/properties/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- `Order` reaches 75/307 endpoint coverage under the `Order` API tag (order property types and order-level property values milestone)
```

- [ ] **Step 6: Update `ROADMAP.md`**

Change these 6 rows' Status column to `**implemented**` and, per this task's correction, add
the deprecation note that's currently missing on them:

```
| DELETE | `/rest/orders/properties/{id}` | Delete property of an order by property ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.delete_order_property` |
| PUT | `/rest/orders/properties/{id}` | Update property of an order by property ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.update_order_property` |
| POST | `/rest/orders/{orderId}/properties` | Create property for an order | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.create_order_property` |
| GET | `/rest/orders/{orderId}/properties/{typeId?}` | List properties of an order | **implemented** (deprecated by PlentyMarkets, use `GET /rest/orders/{orderId}`) | `orders.list_order_properties` |
| DELETE | `/rest/orders/{orderId}/properties/{typeId}` | Delete property of an order by order ID and property type ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.delete_order_property_by_type` |
| PUT | `/rest/orders/{orderId}/properties/{typeId}` | Update property of an order by order ID and property ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.update_order_property_by_type` |
```

Update the top-of-file summary: `**174 / 1837**` → `**180 / 1837**`, and the `Order` row
`**69/307**` → `**75/307**` (both places).

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/properties.py \
        tests/test_orders_properties.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order-level property value endpoints"
```

---

## Task 9: `properties.py` — order-item property values, addressed by property ID

**Files:**
- Modify: `src/plentymarkets/modules/orders/properties.py`
- Test: `tests/test_orders_properties.py`

**Interfaces:**
- Consumes: `OrdersBase._session`
- Produces:
  - `PropertiesMixin.create_item_property(order_item_id: int, type_id: int, value: str) -> dict[str, Any]`
  - `PropertiesMixin.delete_item_property(property_id: int) -> dict[str, Any]`
  - `PropertiesMixin.get_item_property(property_id: int) -> dict[str, Any]`
  - `PropertiesMixin.update_item_property(property_id: int, order_item_id: int | None = None, type_id: int | None = None, value: str | None = None) -> dict[str, Any]`

All four endpoints in this task are marked deprecated in the spec (use
`PUT /rest/orders/{orderId}`).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_properties.py`:

```python
# --- order-item property values, by property ID ---


async def test_create_item_property_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/items/properties",
        json={"id": 701, "orderItemId": 10, "typeId": 29, "value": "M"},
    )
    result = await orders.create_item_property(
        order_item_id=10, type_id=29, value="M"
    )
    assert result["id"] == 701
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderItemId": 10,
        "typeId": 29,
        "value": "M",
    }


async def test_delete_item_property_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/items/properties/701",
        json={},
    )
    result = await orders.delete_item_property(701)
    assert result == {}


async def test_get_item_property_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/properties/701",
        json={"id": 701, "orderItemId": 10, "typeId": 29, "value": "M"},
    )
    result = await orders.get_item_property(701)
    assert result["value"] == "M"


async def test_update_item_property_puts_only_given_fields(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/items/properties/701",
        json={"id": 701, "orderItemId": 10, "typeId": 29, "value": "L"},
    )
    result = await orders.update_item_property(701, value="L")
    assert result["value"] == "L"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"value": "L"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_properties.py -v -k "item_property and not item_property_by_type"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `properties.py`**

Add to `PropertiesMixin`, after `update_order_property_by_type`:

```python
    async def create_item_property(
        self, order_item_id: int, type_id: int, value: str
    ) -> dict[str, Any]:
        """Create an order-item property, addressed by a new property ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order-item property type ID.
            value: The property value.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The order-item property record ID.
            - ``orderItemId`` (int): The order item this property belongs
              to.
            - ``typeId`` (int): The property type ID.
            - ``value`` (str): The property value.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.post(
            "/rest/orders/items/properties",
            json={"orderItemId": order_item_id, "typeId": type_id, "value": value},
        )

    async def delete_item_property(self, property_id: int) -> dict[str, Any]:
        """Delete an order-item property by its own property ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            property_id: The order-item property record ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/orders/items/properties/{property_id}"
        )

    async def get_item_property(self, property_id: int) -> dict[str, Any]:
        """Get an order-item property by its own property ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            property_id: The order-item property record ID.

        Returns:
            An order-item property dict (see :meth:`create_item_property`
            for the field reference).
        """
        return await self._session.get(f"/rest/orders/items/properties/{property_id}")

    async def update_item_property(
        self,
        property_id: int,
        order_item_id: int | None = None,
        type_id: int | None = None,
        value: str | None = None,
    ) -> dict[str, Any]:
        """Update an order-item property by its own property ID.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead. Unlike most PUT
            endpoints in this module, the spec marks none of this
            operation's body fields as required — all three are optional
            here.

        Args:
            property_id: The order-item property record ID.
            order_item_id: New order item ID to reassign the property to.
            type_id: New property type ID.
            value: New property value.

        Returns:
            The updated order-item property dict (see
            :meth:`create_item_property` for the field reference).
        """
        data: dict[str, Any] = {}
        if order_item_id is not None:
            data["orderItemId"] = order_item_id
        if type_id is not None:
            data["typeId"] = type_id
        if value is not None:
            data["value"] = value
        return await self._session.put(
            f"/rest/orders/items/properties/{property_id}", json=data
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_properties.py -v`
Expected: all tests pass, including the 4 new ones.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.create_item_property` — create an order-item property via `POST /rest/orders/items/properties` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.delete_item_property` — delete an order-item property via `DELETE /rest/orders/items/properties/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.get_item_property` — get an order-item property via `GET /rest/orders/items/properties/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.update_item_property` — update an order-item property via `PUT /rest/orders/items/properties/{id}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
```

- [ ] **Step 6: Update `ROADMAP.md`**

```
| POST | `/rest/orders/items/properties` | Create order item property | **implemented** | `orders.create_item_property` |
| DELETE | `/rest/orders/items/properties/{id}` | Delete order item property | **implemented** | `orders.delete_item_property` |
| GET | `/rest/orders/items/properties/{id}` | Get order item property | **implemented** | `orders.get_item_property` |
| PUT | `/rest/orders/items/properties/{id}` | Update order item property | **implemented** | `orders.update_item_property` |
```

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/properties.py \
        tests/test_orders_properties.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order-item property values addressed by property ID"
```

---

## Task 10: `properties.py` — order-item property values, addressed by type

**Files:**
- Modify: `src/plentymarkets/modules/orders/properties.py`
- Test: `tests/test_orders_properties.py`

**Interfaces:**
- Consumes: `OrdersBase._session`
- Produces:
  - `PropertiesMixin.list_item_properties(order_item_id: int) -> list[dict[str, Any]]`
  - `PropertiesMixin.delete_item_property_by_type(order_item_id: int, type_id: int) -> dict[str, Any]`
  - `PropertiesMixin.get_item_property_by_type(order_item_id: int, type_id: int) -> dict[str, Any]`
  - `PropertiesMixin.create_item_property_by_type(order_item_id: int, type_id: int, value: str) -> dict[str, Any]`
  - `PropertiesMixin.update_item_property_by_type(order_item_id: int, type_id: int, value: str) -> dict[str, Any]`

All five endpoints in this task are marked deprecated in the spec (use
`PUT /rest/orders/{orderId}`). This is the last `properties.py` task — 20/20 methods complete
after this one.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_orders_properties.py`:

```python
# --- order-item property values, by order item + type ---


async def test_list_item_properties_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/10/properties",
        json=[{"id": 701, "orderItemId": 10, "typeId": 29, "value": "M"}],
    )
    result = await orders.list_item_properties(10)
    assert result[0]["typeId"] == 29


async def test_delete_item_property_by_type_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/items/10/properties/29",
        json={},
    )
    result = await orders.delete_item_property_by_type(10, 29)
    assert result == {}


async def test_get_item_property_by_type_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/10/properties/29",
        json={"id": 701, "orderItemId": 10, "typeId": 29, "value": "M"},
    )
    result = await orders.get_item_property_by_type(10, 29)
    assert result["value"] == "M"


async def test_create_item_property_by_type_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/items/10/properties/29",
        json={"id": 701, "orderItemId": 10, "typeId": 29, "value": "M"},
    )
    result = await orders.create_item_property_by_type(10, 29, value="M")
    assert result["id"] == 701
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderItemId": 10,
        "typeId": 29,
        "value": "M",
    }


async def test_update_item_property_by_type_puts_value(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/items/10/properties/29",
        json={"id": 701, "orderItemId": 10, "typeId": 29, "value": "L"},
    )
    result = await orders.update_item_property_by_type(10, 29, value="L")
    assert result["value"] == "L"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"value": "L"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_properties.py -v -k "item_property_by_type or list_item_properties"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Implement in `properties.py`**

Add to `PropertiesMixin`, after `update_item_property`:

```python
    async def list_item_properties(
        self, order_item_id: int
    ) -> list[dict[str, Any]]:
        """List all properties of an order item.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.

        Returns:
            A list of order-item property dicts (see
            :meth:`create_item_property` for the field reference).
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/items/{order_item_id}/properties"
        )

    async def delete_item_property_by_type(
        self, order_item_id: int, type_id: int
    ) -> dict[str, Any]:
        """Delete an order-item property, addressed by item and type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order-item property type ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/orders/items/{order_item_id}/properties/{type_id}"
        )

    async def get_item_property_by_type(
        self, order_item_id: int, type_id: int
    ) -> dict[str, Any]:
        """Get an order-item property, addressed by item and type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order-item property type ID.

        Returns:
            An order-item property dict (see :meth:`create_item_property`
            for the field reference).
        """
        return await self._session.get(
            f"/rest/orders/items/{order_item_id}/properties/{type_id}"
        )

    async def create_item_property_by_type(
        self, order_item_id: int, type_id: int, value: str
    ) -> dict[str, Any]:
        """Create an order-item property, addressed by item and type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order-item property type ID.
            value: The property value.

        Returns:
            The created order-item property dict (see
            :meth:`create_item_property` for the field reference).
        """
        return await self._session.post(
            f"/rest/orders/items/{order_item_id}/properties/{type_id}",
            json={"orderItemId": order_item_id, "typeId": type_id, "value": value},
        )

    async def update_item_property_by_type(
        self, order_item_id: int, type_id: int, value: str
    ) -> dict[str, Any]:
        """Update an order-item property, addressed by item and type.

        Note:
            **Deprecated** by PlentyMarkets: use
            ``PUT /rest/orders/{orderId}`` instead.

        Args:
            order_item_id: The order item ID.
            type_id: The order-item property type ID.
            value: The new property value.

        Returns:
            The updated order-item property dict (see
            :meth:`create_item_property` for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/items/{order_item_id}/properties/{type_id}",
            json={"value": value},
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_properties.py -v`
Expected: all 20 tests in the file pass. Then run the full suite: `uv run pytest`.

- [ ] **Step 5: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_item_properties` — list all properties of an order item via `GET /rest/orders/items/{orderItemId}/properties` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.delete_item_property_by_type` — delete an order-item property by item and type via `DELETE /rest/orders/items/{orderItemId}/properties/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.get_item_property_by_type` — get an order-item property by item and type via `GET /rest/orders/items/{orderItemId}/properties/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.create_item_property_by_type` — create an order-item property by item and type via `POST /rest/orders/items/{orderItemId}/properties/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- feat: `OrdersModule.update_item_property_by_type` — update an order-item property by item and type via `PUT /rest/orders/items/{orderItemId}/properties/{typeId}` (deprecated by PlentyMarkets; use `PUT /rest/orders/{orderId}`)
- `Order` reaches 84/307 endpoint coverage under the `Order` API tag (properties milestone complete: property types + order-level + order-item-level property values)
```

- [ ] **Step 6: Update `ROADMAP.md`**

```
| GET | `/rest/orders/items/{orderItemId}/properties` | Get all order item properties | **implemented** | `orders.list_item_properties` |
| DELETE | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Delete order item property | **implemented** | `orders.delete_item_property_by_type` |
| GET | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Get order item property | **implemented** | `orders.get_item_property_by_type` |
| POST | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Create order item property | **implemented** | `orders.create_item_property_by_type` |
| PUT | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Update order item property | **implemented** | `orders.update_item_property_by_type` |
```

Update the top-of-file summary: `**180 / 1837**` → `**189 / 1837**`, and the `Order` row
`**75/307**` → `**84/307**` (both places).

- [ ] **Step 7: Commit**

```bash
git add src/plentymarkets/modules/orders/properties.py \
        tests/test_orders_properties.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order-item property values addressed by item and type"
```

---

## Task 11: `referrers.py` — new file, order referrers CRUD

**Files:**
- Create: `src/plentymarkets/modules/orders/referrers.py`
- Modify: `src/plentymarkets/modules/orders/__init__.py`
- Test: Create `tests/test_orders_referrers.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `ReferrersMixin` class (new), added to `OrdersModule`'s bases
  - `ReferrersMixin.list_referrers(columns: list[str] | None = None) -> list[dict[str, Any]]`
  - `ReferrersMixin.get_next_free_referrer_id() -> dict[str, Any]`
  - `ReferrersMixin.search_referrers(page: int = 1, items_per_page: int = 20, sort_by: str | None = None, sort_order: str | None = None, referrer_id: int | None = None, name: str | None = None) -> dict[str, Any]`
  - `ReferrersMixin.paginate_referrers(sort_by: str | None = None, sort_order: str | None = None, referrer_id: int | None = None, name: str | None = None, items_per_page: int = 20) -> AsyncIterator[dict[str, Any]]`
  - `ReferrersMixin.create_referrer(parent_referrer_id: int, values: list[str]) -> dict[str, Any]`
  - `ReferrersMixin.delete_referrer(referrer_id: int) -> dict[str, Any]`
  - `ReferrersMixin.get_referrer(referrer_id: int) -> dict[str, Any]`
  - `ReferrersMixin.update_referrer(referrer_id: int, data: dict[str, Any]) -> dict[str, Any]`

None of these 7 endpoints are deprecated.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_orders_referrers.py`:

```python
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_list_referrers_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers",
        json=[{"id": 1, "name": "Google", "isEditable": True}],
    )
    result = await orders.list_referrers()
    assert result[0]["name"] == "Google"


async def test_list_referrers_sends_columns(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers?columns=id%2Cname",
        json=[],
    )
    await orders.list_referrers(columns=["id", "name"])


async def test_get_next_free_referrer_id_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/next_free_main",
        json={"data": 5},
    )
    result = await orders.get_next_free_referrer_id()
    assert result["data"] == 5


async def test_search_referrers_defaults_to_page_1_and_20(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/search?page=1&itemsPerPage=20",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search_referrers()
    assert result["page"] == 1


async def test_paginate_referrers_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/search?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/search?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [r async for r in orders.paginate_referrers(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_create_referrer_sends_data_values(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/referrers/1?data=name%3AGoogle%2CisFilterable%3Atrue",
        json={"id": 2, "name": "Google"},
    )
    result = await orders.create_referrer(
        1, values=["name:Google", "isFilterable:true"]
    )
    assert result["id"] == 2


async def test_delete_referrer_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/referrers/2",
        json={},
    )
    result = await orders.delete_referrer(2)
    assert result == {}


async def test_get_referrer_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/2",
        json={"id": 2, "name": "Google"},
    )
    result = await orders.get_referrer(2)
    assert result["name"] == "Google"


async def test_update_referrer_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/referrers/2",
        json={"id": 2, "name": "Google Ads"},
    )
    result = await orders.update_referrer(2, {"name": "Google Ads"})
    assert result["name"] == "Google Ads"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_referrers.py -v`
Expected: FAIL — `referrers.py` does not exist yet.

- [ ] **Step 3: Create `referrers.py`**

```python
from __future__ import annotations

from typing import Any, AsyncIterator

from ._base import OrdersBase


class ReferrersMixin(OrdersBase):
    """Order referrer management (`/rest/orders/referrers`)."""

    async def list_referrers(
        self, columns: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List all order referrers.

        Args:
            columns: Restrict the response to these referrer attributes.

        Returns:
            A list of referrer dicts, each with:

            - ``id`` (float): The referrer ID.
            - ``isEditable`` (bool): Whether this referrer can be edited or
              deleted.
            - ``backendName`` (str): The referrer's back-end name.
            - ``name`` (str): The referrer's public display name, e.g. on
              documents.
            - ``orderOwnerId`` (int): User ID that owns new orders from this
              referrer.
            - ``isFilterable`` (bool): Whether this referrer can be used as
              a filter.
            - ``origin`` (str): The referrer's origin.
            - ``showInLeads`` (bool): Whether this referrer is shown when
              creating a new lead.
        """
        params = self._build_params(
            None, columns=",".join(columns) if columns else None
        )
        return await self._session.get(  # type: ignore[return-value]
            "/rest/orders/referrers", params=params
        )

    async def get_next_free_referrer_id(self) -> dict[str, Any]:
        """Get the next free main referrer ID.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as ``SimpleRestResponse`` — a bare placeholder schema
            with no fields. Response shape is unverified. Verify against a
            live system before relying on it.

        Returns:
            The API's response dict.
        """
        return await self._session.get("/rest/orders/referrers/next_free_main")

    async def search_referrers(
        self,
        page: int = 1,
        items_per_page: int = 20,
        sort_by: str | None = None,
        sort_order: str | None = None,
        referrer_id: int | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        """Search order referrers with pagination and filters.

        Note:
            The spec documents this endpoint's default ``itemsPerPage`` as
            ``20``, not this module's usual default of ``50``.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page.
            sort_by: Field to sort by. Defaults to ``"id"``.
            sort_order: Sort direction, ``"asc"`` or ``"desc"``. Defaults to
                ``"asc"``.
            referrer_id: Filter by referrer ID.
            name: Filter by referrer name.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching referrers.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Referrer dicts (see
              :meth:`list_referrers` for the field reference).
        """
        params = self._build_params(
            None,
            page=page,
            itemsPerPage=items_per_page,
            sortBy=sort_by,
            sortOrder=sort_order,
            id=referrer_id,
            name=name,
        )
        return await self._session.get("/rest/orders/referrers/search", params=params)

    async def paginate_referrers(
        self,
        sort_by: str | None = None,
        sort_order: str | None = None,
        referrer_id: int | None = None,
        name: str | None = None,
        items_per_page: int = 20,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every matching referrer across all
        pages.

        Args:
            sort_by: Field to sort by (see :meth:`search_referrers`).
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            referrer_id: Filter by referrer ID.
            name: Filter by referrer name.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual referrer dicts (see :meth:`list_referrers` for the
            field reference).
        """
        page = 1
        while True:
            result = await self.search_referrers(
                page=page,
                items_per_page=items_per_page,
                sort_by=sort_by,
                sort_order=sort_order,
                referrer_id=referrer_id,
                name=name,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def create_referrer(
        self, parent_referrer_id: int, values: list[str]
    ) -> dict[str, Any]:
        """Create a new order referrer, or a sub-referrer of an existing one.

        Note:
            The spec's path parameter is literally named
            ``{parentReferrerId?}`` — the trailing ``?`` suggests an
            optional segment — yet it is marked ``required: true``, and the
            endpoint's own description says a referrer ID is
            auto-assigned "if no ID is specified." This is a contradiction
            in the published spec; ``parent_referrer_id`` is implemented as
            required here. Verify against a live system whether calling
            ``POST /rest/orders/referrers`` (no segment) is also accepted
            for auto-assignment.

        Args:
            parent_referrer_id: ID of the parent referrer to create a
                sub-referrer under.
            values: List of ``"key:value"`` strings describing the new
                referrer's attributes (see :meth:`list_referrers` for the
                available keys), e.g. ``["name:Google",
                "isFilterable:true"]``.

        Returns:
            The created referrer dict (see :meth:`list_referrers` for the
            field reference).
        """
        params = self._build_params(None, data=",".join(values))
        return await self._session.post(
            f"/rest/orders/referrers/{parent_referrer_id}", params=params
        )

    async def delete_referrer(self, referrer_id: int) -> dict[str, Any]:
        """Delete an order referrer.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as ``SimpleRestResponse`` — a bare placeholder schema
            with no fields. Response shape is unverified. Verify against a
            live system before relying on it.

        Args:
            referrer_id: The referrer ID.

        Returns:
            The API's response dict.
        """
        return await self._session.delete(f"/rest/orders/referrers/{referrer_id}")

    async def get_referrer(self, referrer_id: int) -> dict[str, Any]:
        """Get a single order referrer by ID.

        Args:
            referrer_id: The referrer ID.

        Returns:
            A referrer dict (see :meth:`list_referrers` for the field
            reference).
        """
        return await self._session.get(f"/rest/orders/referrers/{referrer_id}")

    async def update_referrer(
        self, referrer_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an order referrer.

        Note:
            PlentyMarkets' published OpenAPI spec declares no request body
            schema for this endpoint at all. Based on :meth:`list_referrers`'
            field reference, ``data`` likely accepts ``name``,
            ``backendName``, ``orderOwnerId``, ``isFilterable``,
            ``showInLeads`` keys. Verify against a live system before
            relying on this shape.

        Args:
            referrer_id: The referrer ID.
            data: Referrer update payload — see the Note above.

        Returns:
            The updated referrer dict (see :meth:`list_referrers` for the
            field reference).
        """
        return await self._session.put(
            f"/rest/orders/referrers/{referrer_id}", json=data
        )
```

- [ ] **Step 4: Wire `ReferrersMixin` into `OrdersModule`**

In `src/plentymarkets/modules/orders/__init__.py`, replace:

```python
from .properties import PropertiesMixin
from .reorders import ReordersMixin
```

with:

```python
from .properties import PropertiesMixin
from .referrers import ReferrersMixin
from .reorders import ReordersMixin
```

and replace:

```python
    ReordersMixin,
    PropertiesMixin,
    OrdersBase,
):
```

with:

```python
    ReordersMixin,
    PropertiesMixin,
    ReferrersMixin,
    OrdersBase,
):
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_referrers.py -v`
Expected: all 9 tests pass. Then run `uv run pytest` (full suite) to confirm no regressions.

- [ ] **Step 6: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_referrers` — list all order referrers via `GET /rest/orders/referrers`
- feat: `OrdersModule.get_next_free_referrer_id` — get the next free main referrer ID via `GET /rest/orders/referrers/next_free_main`
- feat: `OrdersModule.search_referrers` / `paginate_referrers` — search/iterate order referrers via `GET /rest/orders/referrers/search`
- feat: `OrdersModule.create_referrer` — create an order referrer via `POST /rest/orders/referrers/{parentReferrerId}`
- feat: `OrdersModule.delete_referrer` — delete an order referrer via `DELETE /rest/orders/referrers/{referrerId}`
- feat: `OrdersModule.get_referrer` — get one order referrer via `GET /rest/orders/referrers/{referrerId}`
- feat: `OrdersModule.update_referrer` — update an order referrer via `PUT /rest/orders/referrers/{referrerId}`
- `Order` reaches 91/307 endpoint coverage under the `Order` API tag (referrers milestone)
- refactor: `modules/orders/` gains a `referrers.py` mixin (`ReferrersMixin`) — no public API change
```

- [ ] **Step 7: Update `ROADMAP.md`**

```
| GET | `/rest/orders/referrers` | List referrers | **implemented** | `orders.list_referrers` |
| GET | `/rest/orders/referrers/next_free_main` | Get next free main referrer ID | **implemented** | `orders.get_next_free_referrer_id` |
| GET | `/rest/orders/referrers/search` | Search for referrers | **implemented** | `orders.search_referrers` |
| POST | `/rest/orders/referrers/{parentReferrerId?}` | Create an order referrer | **implemented** | `orders.create_referrer` |
| DELETE | `/rest/orders/referrers/{referrerId}` | Delete referrer | **implemented** | `orders.delete_referrer` |
| GET | `/rest/orders/referrers/{referrerId}` | Get a referrer | **implemented** | `orders.get_referrer` |
| PUT | `/rest/orders/referrers/{referrerId}` | Update referrer | **implemented** | `orders.update_referrer` |
```

Update the top-of-file summary: `**189 / 1837**` → `**196 / 1837**`, and the `Order` row
`**84/307**` → `**91/307**` (both places).

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/modules/orders/referrers.py \
        src/plentymarkets/modules/orders/__init__.py \
        tests/test_orders_referrers.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add order referrers CRUD"
```

---

## Task 12: `currencies.py` — new file, currency and exchange-rate lookups

**Files:**
- Create: `src/plentymarkets/modules/orders/currencies.py`
- Modify: `src/plentymarkets/modules/orders/__init__.py`
- Test: Create `tests/test_orders_currencies.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `CurrenciesMixin` class (new), added to `OrdersModule`'s bases
  - `CurrenciesMixin.list_currencies(columns: list[str] | None = None, with_: list[str] | None = None) -> list[dict[str, Any]]`
  - `CurrenciesMixin.get_currency_for_country(country_id: int, columns: list[str] | None = None, with_: list[str] | None = None) -> dict[str, Any]`
  - `CurrenciesMixin.list_exchange_rates_from(currency_iso: str) -> list[Any]`
  - `CurrenciesMixin.list_exchange_rates_to(currency_iso: str) -> list[Any]`
  - `CurrenciesMixin.get_currency(currency_iso: str, columns: list[str] | None = None, with_: list[str] | None = None) -> dict[str, Any]`
  - `CurrenciesMixin.list_currency_countries(currency_iso: str, columns: list[str] | None = None) -> list[dict[str, Any]]`
  - `CurrenciesMixin.get_currency_exchange_rate(currency_iso: str) -> dict[str, Any]`

All 7 endpoints are GET, none deprecated, no TypedDicts (no writes).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_orders_currencies.py`:

```python
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_list_currencies_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies",
        json=[{"currency": "EUR", "isActive": True}],
    )
    result = await orders.list_currencies()
    assert result[0]["currency"] == "EUR"


async def test_get_currency_for_country_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/countries/1",
        json={"currency": "EUR", "isActive": True},
    )
    result = await orders.get_currency_for_country(1)
    assert result["currency"] == "EUR"


async def test_list_exchange_rates_from_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/exchange_rates/from/EUR",
        json=[{"to": "USD", "rate": 1.1}],
    )
    result = await orders.list_exchange_rates_from("EUR")
    assert result == [{"to": "USD", "rate": 1.1}]


async def test_list_exchange_rates_to_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/exchange_rates/to/EUR",
        json=[{"from": "USD", "rate": 0.9}],
    )
    result = await orders.list_exchange_rates_to("EUR")
    assert result == [{"from": "USD", "rate": 0.9}]


async def test_get_currency_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/EUR",
        json={"currency": "EUR", "isActive": True},
    )
    result = await orders.get_currency("EUR")
    assert result["currency"] == "EUR"


async def test_list_currency_countries_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/EUR/countries",
        json=[{"id": 1, "name": "Germany", "isoCode2": "DE"}],
    )
    result = await orders.list_currency_countries("EUR")
    assert result[0]["isoCode2"] == "DE"


async def test_get_currency_exchange_rate_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/EUR/exchangeRate",
        json={"exchangeRate": 1.0},
    )
    result = await orders.get_currency_exchange_rate("EUR")
    assert result["exchangeRate"] == 1.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_currencies.py -v`
Expected: FAIL — `currencies.py` does not exist yet.

- [ ] **Step 3: Create `currencies.py`**

```python
from __future__ import annotations

from typing import Any

from ._base import OrdersBase


class CurrenciesMixin(OrdersBase):
    """Currency and exchange-rate lookups (`/rest/orders/currencies`).

    All-read-only; PlentyMarkets exposes no create/update/delete endpoints
    for currencies.
    """

    async def list_currencies(
        self, columns: list[str] | None = None, with_: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List all currencies known to the system.

        Args:
            columns: Restrict the response to these currency attributes.
            with_: Related data to embed.

        Returns:
            A list of currency dicts, each with:

            - ``currency`` (str): The ISO 4217 currency code.
            - ``htmlCode`` (str): HTML entity code for the currency symbol.
            - ``unicodeSign`` (str): Unicode currency symbol, or the HTML
              code if no Unicode symbol exists.
            - ``isActive`` (bool): Whether the currency is active in the
              system (activated per sales price).
            - ``isErasable`` (bool): Whether this currency can be deleted.
            - ``exchangeRate`` (float): The current exchange rate.
        """
        params = self._build_params(
            None, with_=with_, columns=",".join(columns) if columns else None
        )
        return await self._session.get(  # type: ignore[return-value]
            "/rest/orders/currencies", params=params
        )

    async def get_currency_for_country(
        self,
        country_id: int,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get the currency configured for a country.

        Args:
            country_id: The country ID.
            columns: Restrict the response to these currency attributes.
            with_: Related data to embed.

        Returns:
            A currency dict (see :meth:`list_currencies` for the field
            reference).
        """
        params = self._build_params(
            None, with_=with_, columns=",".join(columns) if columns else None
        )
        return await self._session.get(
            f"/rest/orders/currencies/countries/{country_id}", params=params
        )

    async def list_exchange_rates_from(self, currency_iso: str) -> list[Any]:
        """List exchange rates *from* a currency to every other currency.

        Note:
            The spec types ``currencyIso`` as ``integer`` on this operation
            (and :meth:`list_exchange_rates_to`), inconsistent with the
            ``string`` type used everywhere else in this mixin — treated as
            ``str`` here uniformly. Response items are also declared as an
            untyped (``mixed``) schema. Verify against a live system before
            relying on this endpoint's shape.

        Args:
            currency_iso: ISO 4217 currency code to convert from.

        Returns:
            An unverified list of exchange-rate entries.
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/currencies/exchange_rates/from/{currency_iso}"
        )

    async def list_exchange_rates_to(self, currency_iso: str) -> list[Any]:
        """List exchange rates *to* a currency from every other currency.

        Note:
            See the Note on :meth:`list_exchange_rates_from` — the same
            ``currencyIso`` type inconsistency and untyped response items
            apply here.

        Args:
            currency_iso: ISO 4217 currency code to convert to.

        Returns:
            An unverified list of exchange-rate entries.
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/currencies/exchange_rates/to/{currency_iso}"
        )

    async def get_currency(
        self,
        currency_iso: str,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a single currency by its ISO 4217 code.

        Args:
            currency_iso: ISO 4217 currency code, e.g. ``"EUR"``.
            columns: Restrict the response to these currency attributes.
            with_: Related data to embed.

        Returns:
            A currency dict (see :meth:`list_currencies` for the field
            reference).
        """
        params = self._build_params(
            None, with_=with_, columns=",".join(columns) if columns else None
        )
        return await self._session.get(
            f"/rest/orders/currencies/{currency_iso}", params=params
        )

    async def list_currency_countries(
        self, currency_iso: str, columns: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List countries that use a given currency.

        Args:
            currency_iso: ISO 4217 currency code, e.g. ``"EUR"``.
            columns: Restrict the response to these country attributes.

        Returns:
            A list of country dicts, each with:

            - ``id`` (int): The country ID.
            - ``name`` (str): The country name.
            - ``shippingDestinationId`` (int): Shipping destination group
              ID.
            - ``active`` (bool): Whether the country is active in the
              system.
            - ``storehouseId`` (int): Associated storehouse ID.
            - ``isoCode2`` (str): ISO 3166-1 alpha-2 code.
            - ``isoCode3`` (str): ISO 3166-1 alpha-3 code.
            - ``lang`` (str): The country's default language.
            - ``isCountryStateMandatory`` (bool): Whether a state/province
              is required for addresses in this country.
            - ``vatCodes`` (list): VAT code configurations for this
              country.
        """
        params = self._build_params(
            None, columns=",".join(columns) if columns else None
        )
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/currencies/{currency_iso}/countries", params=params
        )

    async def get_currency_exchange_rate(self, currency_iso: str) -> dict[str, Any]:
        """Get the current exchange rate for a currency.

        Note:
            The spec types ``currencyIso`` as ``integer`` on this
            operation, inconsistent with the ``string`` type used
            elsewhere in this mixin — treated as ``str`` here uniformly.

        Args:
            currency_iso: ISO 4217 currency code, e.g. ``"EUR"``.

        Returns:
            A dict with a single key:

            - ``exchangeRate`` (float): The current exchange rate.
        """
        return await self._session.get(
            f"/rest/orders/currencies/{currency_iso}/exchangeRate"
        )
```

- [ ] **Step 4: Wire `CurrenciesMixin` into `OrdersModule`**

In `src/plentymarkets/modules/orders/__init__.py`, replace:

```python
from .core import CoreMixin
from .dates import DatesMixin
```

with:

```python
from .core import CoreMixin
from .currencies import CurrenciesMixin
from .dates import DatesMixin
```

and replace:

```python
    PropertiesMixin,
    ReferrersMixin,
    OrdersBase,
):
```

with:

```python
    PropertiesMixin,
    ReferrersMixin,
    CurrenciesMixin,
    OrdersBase,
):
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_currencies.py -v`
Expected: all 7 tests pass. Then run `uv run pytest` (full suite) to confirm no regressions.

- [ ] **Step 6: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_currencies` — list all currencies via `GET /rest/orders/currencies`
- feat: `OrdersModule.get_currency_for_country` — get a country's currency via `GET /rest/orders/currencies/countries/{countryId}`
- feat: `OrdersModule.list_exchange_rates_from` — list exchange rates from a currency via `GET /rest/orders/currencies/exchange_rates/from/{currencyIso}`
- feat: `OrdersModule.list_exchange_rates_to` — list exchange rates to a currency via `GET /rest/orders/currencies/exchange_rates/to/{currencyIso}`
- feat: `OrdersModule.get_currency` — get one currency via `GET /rest/orders/currencies/{currencyIso}`
- feat: `OrdersModule.list_currency_countries` — list countries using a currency via `GET /rest/orders/currencies/{currencyIso}/countries`
- feat: `OrdersModule.get_currency_exchange_rate` — get a currency's exchange rate via `GET /rest/orders/currencies/{currencyIso}/exchangeRate`
- `Order` reaches 98/307 endpoint coverage under the `Order` API tag (currencies milestone)
- refactor: `modules/orders/` gains a `currencies.py` mixin (`CurrenciesMixin`) — no public API change
```

- [ ] **Step 7: Update `ROADMAP.md`**

```
| GET | `/rest/orders/currencies` | List currencies | **implemented** | `orders.list_currencies` |
| GET | `/rest/orders/currencies/countries/{countryId}` | Get a currency for a country | **implemented** | `orders.get_currency_for_country` |
| GET | `/rest/orders/currencies/exchange_rates/from/{currencyIso}` | Get the exchange rates from a currency | **implemented** | `orders.list_exchange_rates_from` |
| GET | `/rest/orders/currencies/exchange_rates/to/{currencyIso}` | Get the exchange rates to a currency | **implemented** | `orders.list_exchange_rates_to` |
| GET | `/rest/orders/currencies/{currencyIso}` | Get a currency | **implemented** | `orders.get_currency` |
| GET | `/rest/orders/currencies/{currencyIso}/countries` | List countries for a currency | **implemented** | `orders.list_currency_countries` |
| GET | `/rest/orders/currencies/{currencyIso}/exchangeRate` | Get the exchange rate for a currency | **implemented** | `orders.get_currency_exchange_rate` |
```

Update the top-of-file summary: `**196 / 1837**` → `**203 / 1837**`, and the `Order` row
`**91/307**` → `**98/307**` (both places).

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/modules/orders/currencies.py \
        src/plentymarkets/modules/orders/__init__.py \
        tests/test_orders_currencies.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add currency and exchange-rate lookups"
```

---

## Task 13: `coupons.py` — new file, campaign and coupon-code management

**Files:**
- Create: `src/plentymarkets/modules/orders/coupons.py`
- Modify: `src/plentymarkets/modules/orders/__init__.py`
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Test: Create `tests/test_orders_coupons.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `CouponsMixin` class (new), added to `OrdersModule`'s bases
  - `CouponsMixin.list_campaigns() -> dict[str, Any]`
  - `CouponsMixin.delete_coupon_code(code: str, without_used: int | None = None) -> dict[str, Any]`
  - `CouponsMixin.get_coupon_code(code: str, with_: str | None = None) -> dict[str, Any]`
  - `CouponsMixin.set_coupon_code_disabled(code: str, is_disabled: int) -> dict[str, Any]`
  - `CouponsMixin.get_campaign(campaign_id: int) -> dict[str, Any]`
  - `CouponsMixin.create_coupon_code(campaign_id: int, data: OrderCouponCodeCreatePayload | None = None) -> dict[str, Any]`
  - `OrderCouponCodeCreatePayload` TypedDict, exported from `plentymarkets`

None of these 6 endpoints are deprecated.

- [ ] **Step 1: Add `OrderCouponCodeCreatePayload` to `_types.py`**

In `src/plentymarkets/_types.py`, add immediately after `OrderPropertyTypeUpdatePayload` (from
Task 7):

```python
class OrderCouponCodeCreatePayload(TypedDict, total=False):
    """Payload for :meth:`OrdersModule.create_coupon_code`
    (``POST /rest/orders/coupons/campaigns/{campaignId}/codes``).

    PlentyMarkets' published OpenAPI spec redeclares ``campaignId`` as a
    body field even though it is already supplied as a path parameter;
    :meth:`OrdersModule.create_coupon_code` merges the ``campaign_id``
    argument into the request body automatically, so it is intentionally
    omitted from this TypedDict.

    Keys:
        code: The coupon code string. Auto-generated if omitted.
        value: The coupon's monetary or percentage value, depending on the
            campaign's configuration.
        usedCount: Initial used-count to seed the code with.
        usedAmount: Initial used-amount to seed the code with.
    """

    code: NotRequired[str]
    value: NotRequired[float]
    usedCount: NotRequired[int]
    usedAmount: NotRequired[float]
```

- [ ] **Step 2: Export `OrderCouponCodeCreatePayload` from `src/plentymarkets/__init__.py`**

Add it to both the `from ._types import (...)` block and `__all__`, alphabetized alongside the
other `Order*` entries.

- [ ] **Step 3: Write the failing tests**

Create `tests/test_orders_coupons.py`:

```python
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


# --- campaigns and coupon codes ---


async def test_list_campaigns_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"id": 1}]},
    )
    result = await orders.list_campaigns()
    assert result["entries"][0]["id"] == 1


async def test_delete_coupon_code_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/codes/SAVE10",
        json={},
    )
    result = await orders.delete_coupon_code("SAVE10")
    assert result == {}


async def test_get_coupon_code_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/codes/SAVE10",
        json={"code": "SAVE10", "campaignId": 1, "value": 10.0},
    )
    result = await orders.get_coupon_code("SAVE10")
    assert result["value"] == 10.0


async def test_set_coupon_code_disabled_puts_no_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/codes/SAVE10/disabled/1",
        json={},
    )
    result = await orders.set_coupon_code_disabled("SAVE10", 1)
    assert result == {}


async def test_get_campaign_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/1",
        json={"id": 1, "name": "Summer Sale"},
    )
    result = await orders.get_campaign(1)
    assert result["name"] == "Summer Sale"


async def test_create_coupon_code_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/1/codes",
        json={"code": "SAVE20", "campaignId": 1, "value": 20.0},
    )
    result = await orders.create_coupon_code(1, {"code": "SAVE20", "value": 20.0})
    assert result["code"] == "SAVE20"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "code": "SAVE20",
        "value": 20.0,
        "campaignId": 1,
    }
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_coupons.py -v`
Expected: FAIL — `coupons.py` does not exist yet.

- [ ] **Step 5: Create `coupons.py`**

```python
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import OrderCouponCodeCreatePayload, OrderCouponValidatePayload

from ._base import OrdersBase


class CouponsMixin(OrdersBase):
    """Coupon campaign, coupon code, and redemption/validation management.

    Covers `/rest/orders/coupons/*` (campaigns and code management) and
    `/rest/orders/{orderId}/coupons/*` (redemption against a specific
    order). None of these endpoints are deprecated.
    """

    async def list_campaigns(self) -> dict[str, Any]:
        """List all coupon campaigns.

        Note:
            The spec documents zero query parameters for this endpoint —
            despite the page-shaped response, there is no way to control
            ``page``/``itemsPerPage``, so no ``paginate_campaigns`` wrapper
            is possible. Verify against a live system whether pagination
            params are silently accepted anyway.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of campaigns.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Campaign dicts, each with:

                - ``id`` (int): The campaign ID.
                - ``name`` (str): The campaign name.
                - ``variable`` (str): Internal campaign variable name.
                - ``isPermittedForExternalReferrers`` (bool): Whether
                  external referrers may use this campaign.
                - ``includeShipping`` (bool): Whether the discount applies
                  to shipping costs.
                - ``unusedCodesCount`` (int): Number of unused codes.
                - ``usedCodesCount`` (int): Number of used codes.
                - ``startsAt`` (str): ISO 8601 campaign start date.
                - ``endsAt`` (str): ISO 8601 campaign end date.
                - ``minOrderValue`` (float): Minimum order value to qualify.
                - ``codeDurationWeeks`` (int): Code validity duration in
                  weeks.
                - ``discountType`` (str): Type of discount granted.
                - ``value`` (float): The discount value.
        """
        return await self._session.get("/rest/orders/coupons/campaigns")

    async def delete_coupon_code(
        self, code: str, without_used: int | None = None
    ) -> dict[str, Any]:
        """Delete a coupon code.

        Note:
            The spec types ``code`` as ``integer`` on this operation,
            inconsistent with the ``string`` type used on
            :meth:`get_coupon_code` — treated as ``str`` here uniformly
            (the coupon code format is alphanumeric,
            ``^[a-zA-Z0-9_-]{6,32}$``).

        Args:
            code: The coupon code.
            without_used: When set, restricts deletion behavior around
                already-used codes (exact semantics undocumented in the
                spec).

        Returns:
            The API's response dict.
        """
        params = self._build_params(None, withoutUsed=without_used)
        return await self._session.delete(
            f"/rest/orders/coupons/campaigns/codes/{code}", params=params
        )

    async def get_coupon_code(
        self, code: str, with_: str | None = None
    ) -> dict[str, Any]:
        """Get information about a coupon code.

        Note:
            The ``with`` query parameter is a plain string on this
            operation (not the usual ``array[string]`` used elsewhere in
            this module), so it bypasses ``_build_params``'s list-join
            convention.

        Args:
            code: The coupon code.
            with_: Related data to embed, as a single string (not a list).

        Returns:
            A dict with the following keys:

            - ``code`` (str): The coupon code.
            - ``campaignId`` (int): The campaign this code belongs to.
            - ``disable`` (bool): Whether the code is disabled.
            - ``consumed`` (bool): Whether the code has been used.
            - ``usedCount`` (int): Number of times the code has been used.
            - ``usedAmount`` (float): Total amount redeemed against this
              code.
            - ``value`` (float): The coupon's value.
        """
        params: dict[str, Any] = {}
        if with_ is not None:
            params["with"] = with_
        return await self._session.get(
            f"/rest/orders/coupons/campaigns/codes/{code}", params=params
        )

    async def set_coupon_code_disabled(
        self, code: str, is_disabled: int
    ) -> dict[str, Any]:
        """Enable or disable a coupon code.

        Note:
            The spec types both ``code`` and ``isDisabled`` as path
            segments of type ``integer``; ``code`` is treated as ``str``
            here uniformly with the rest of this mixin (see the Note on
            :meth:`delete_coupon_code`).

        Args:
            code: The coupon code.
            is_disabled: ``1`` to disable the code, ``0`` to enable it.

        Returns:
            The API's response dict.
        """
        return await self._session.put(
            f"/rest/orders/coupons/campaigns/codes/{code}/disabled/{is_disabled}"
        )

    async def get_campaign(self, campaign_id: int) -> dict[str, Any]:
        """Get a single coupon campaign by ID.

        Args:
            campaign_id: The campaign ID.

        Returns:
            A campaign dict (see :meth:`list_campaigns` for the field
            reference).
        """
        return await self._session.get(f"/rest/orders/coupons/campaigns/{campaign_id}")

    async def create_coupon_code(
        self, campaign_id: int, data: OrderCouponCodeCreatePayload | None = None
    ) -> dict[str, Any]:
        """Create a new coupon code under a campaign.

        Args:
            campaign_id: The campaign ID to create the code under.
            data: Optional code payload. Use
                :class:`~plentymarkets._types.OrderCouponCodeCreatePayload`
                for IDE autocomplete. ``campaignId`` is merged in
                automatically from ``campaign_id`` and must not be
                included.

        Returns:
            A dict with the following keys:

            - ``code`` (str): The (possibly auto-generated) coupon code.
            - ``campaignId`` (int): The campaign this code belongs to.
            - ``disable`` (bool): Whether the code is disabled.
            - ``consumed`` (bool): Whether the code has been used.
            - ``usedCount`` (int): Number of times the code has been used.
            - ``usedAmount`` (float): Total amount redeemed against this
              code.
            - ``value`` (float): The coupon's value.
        """
        return await self._session.post(
            f"/rest/orders/coupons/campaigns/{campaign_id}/codes",
            json={**(data or {}), "campaignId": campaign_id},
        )
```

- [ ] **Step 6: Wire `CouponsMixin` into `OrdersModule`**

In `src/plentymarkets/modules/orders/__init__.py`, replace:

```python
from .core import CoreMixin
from .currencies import CurrenciesMixin
from .dates import DatesMixin
```

with:

```python
from .core import CoreMixin
from .coupons import CouponsMixin
from .currencies import CurrenciesMixin
from .dates import DatesMixin
```

and replace:

```python
    ReferrersMixin,
    CurrenciesMixin,
    OrdersBase,
):
```

with:

```python
    ReferrersMixin,
    CurrenciesMixin,
    CouponsMixin,
    OrdersBase,
):
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_coupons.py -v`
Expected: all 6 tests pass. Then run `uv run pytest` (full suite) to confirm no regressions.

- [ ] **Step 8: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_campaigns` — list coupon campaigns via `GET /rest/orders/coupons/campaigns`
- feat: `OrdersModule.delete_coupon_code` — delete a coupon code via `DELETE /rest/orders/coupons/campaigns/codes/{code}`
- feat: `OrdersModule.get_coupon_code` — get coupon code information via `GET /rest/orders/coupons/campaigns/codes/{code}`
- feat: `OrdersModule.set_coupon_code_disabled` — enable/disable a coupon code via `PUT /rest/orders/coupons/campaigns/codes/{code}/disabled/{isDisabled}`
- feat: `OrdersModule.get_campaign` — get one coupon campaign via `GET /rest/orders/coupons/campaigns/{campaignId}`
- feat: `OrdersModule.create_coupon_code` — create a coupon code via `POST /rest/orders/coupons/campaigns/{campaignId}/codes`
- feat: `OrderCouponCodeCreatePayload` — TypedDict for `create_coupon_code`
- refactor: `modules/orders/` gains a `coupons.py` mixin (`CouponsMixin`) — no public API change
```

- [ ] **Step 9: Update `ROADMAP.md`**

```
| GET | `/rest/orders/coupons/campaigns` | Get list of campaigns | **implemented** | `orders.list_campaigns` |
| DELETE | `/rest/orders/coupons/campaigns/codes/{code}` | Delete a coupon | **implemented** | `orders.delete_coupon_code` |
| GET | `/rest/orders/coupons/campaigns/codes/{code}` | Get coupon code information | **implemented** | `orders.get_coupon_code` |
| PUT | `/rest/orders/coupons/campaigns/codes/{code}/disabled/{isDisabled}` | Disable or enable coupon | **implemented** | `orders.set_coupon_code_disabled` |
| GET | `/rest/orders/coupons/campaigns/{campaignId}` | Get campaign by Id | **implemented** | `orders.get_campaign` |
| POST | `/rest/orders/coupons/campaigns/{campaignId}/codes` | Create a coupon code | **implemented** | `orders.create_coupon_code` |
```

Update the top-of-file summary: `**203 / 1837**` → `**209 / 1837**`, and the `Order` row
`**98/307**` → `**104/307**` (both places).

- [ ] **Step 10: Commit**

```bash
git add src/plentymarkets/modules/orders/coupons.py \
        src/plentymarkets/modules/orders/__init__.py \
        src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        tests/test_orders_coupons.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add coupon campaign and code management"
```

---

## Task 14: `coupons.py` — coupon validation and order redemption

**Files:**
- Modify: `src/plentymarkets/modules/orders/coupons.py`
- Modify: `src/plentymarkets/_types.py`
- Modify: `src/plentymarkets/__init__.py`
- Test: `tests/test_orders_coupons.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `CouponsMixin.validate_coupons(coupons: list[str], plenty_id: int, ship_to_country: int, data: OrderCouponValidatePayload, call_from_scheduler: bool | None = None, tax_id_number: str | None = None, contact_class: int | None = None, contact_type: int | None = None) -> list[dict[str, Any]]`
  - `CouponsMixin.list_redeemed_coupon_codes(contact_id: int, page: int = 1, items_per_page: int = 50) -> dict[str, Any]`
  - `CouponsMixin.paginate_redeemed_coupon_codes(contact_id: int, items_per_page: int = 50) -> AsyncIterator[dict[str, Any]]`
  - `CouponsMixin.validate_coupon(coupon: str, plenty_id: int, ship_to_country: int, data: OrderCouponValidatePayload, call_from_scheduler: bool | None = None, tax_id_number: str | None = None, contact_class: int | None = None, contact_type: int | None = None) -> dict[str, Any]`
  - `CouponsMixin.redeem_coupon(order_id: int, coupon: str) -> dict[str, Any]`
  - `CouponsMixin.validate_order_coupon(order_id: int, coupon: str) -> list[Any]`
  - `OrderCouponValidatePayload` TypedDict, exported from `plentymarkets`

This is the last `coupons.py` task — 11/11 endpoints complete after this one. None are
deprecated.

- [ ] **Step 1: Add `OrderCouponValidatePayload` to `_types.py`**

In `src/plentymarkets/_types.py`, add immediately after `OrderCouponCodeCreatePayload`:

```python
class OrderCouponValidatePayload(TypedDict, total=False):
    """Payload for :meth:`OrdersModule.validate_coupons` and
    :meth:`OrdersModule.validate_coupon`
    (``POST /rest/orders/coupons/codes(/{coupon})``).

    Keys:
        contactId: ID of the contact the coupon would be applied for.
            **Required.**
        items: List of basket item dicts to validate the coupon against.
            **Required.**
        validationType: Validation mode. Exact accepted values undocumented
            in the spec.
        currency: ISO 4217 currency code for the validation.
        referrer: Referrer ID to validate against.
    """

    contactId: Required[int]
    items: Required[list[dict[str, Any]]]
    validationType: NotRequired[str]
    currency: NotRequired[str]
    referrer: NotRequired[float]
```

- [ ] **Step 2: Export `OrderCouponValidatePayload` from `src/plentymarkets/__init__.py`**

Add it to both the `from ._types import (...)` block and `__all__`, alphabetized alongside the
other `Order*` entries.

- [ ] **Step 3: Write the failing tests**

Append to `tests/test_orders_coupons.py`:

```python
# --- validation and redemption ---


async def test_validate_coupons_sends_params_and_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=(
            f"{BASE_URL}/rest/orders/coupons/codes?coupons=SAVE10"
            "&plentyId=12345&shipToCountry=1"
        ),
        json=[{"campaignId": 1, "couponCode": "SAVE10"}],
    )
    result = await orders.validate_coupons(
        coupons=["SAVE10"],
        plenty_id=12345,
        ship_to_country=1,
        data={"contactId": 7, "items": [{"itemId": 100, "quantity": 1}]},
    )
    assert result[0]["couponCode"] == "SAVE10"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "contactId": 7,
        "items": [{"itemId": 100, "quantity": 1}],
    }


async def test_list_redeemed_coupon_codes_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/codes/contacts/7?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_redeemed_coupon_codes(7)
    assert result["page"] == 1


async def test_paginate_redeemed_coupon_codes_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/codes/contacts/7?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"code": "A"}, {"code": "B"}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/codes/contacts/7?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"code": "C"}],
        },
    )
    results = [
        c
        async for c in orders.paginate_redeemed_coupon_codes(7, items_per_page=2)
    ]
    assert [r["code"] for r in results] == ["A", "B", "C"]


async def test_validate_coupon_sends_params_and_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=(
            f"{BASE_URL}/rest/orders/coupons/codes/SAVE10?plentyId=12345"
            "&shipToCountry=1"
        ),
        json={"campaignId": 1, "couponCode": "SAVE10"},
    )
    result = await orders.validate_coupon(
        "SAVE10",
        plenty_id=12345,
        ship_to_country=1,
        data={"contactId": 7, "items": [{"itemId": 100, "quantity": 1}]},
    )
    assert result["couponCode"] == "SAVE10"


async def test_redeem_coupon_posts_with_no_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/coupons/SAVE10",
        json={"campaignId": 1, "couponCode": "SAVE10"},
    )
    result = await orders.redeem_coupon(42, "SAVE10")
    assert result["couponCode"] == "SAVE10"


async def test_validate_order_coupon_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/coupons/SAVE10/validate",
        json=[{"valid": True}],
    )
    result = await orders.validate_order_coupon(42, "SAVE10")
    assert result == [{"valid": True}]
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_coupons.py -v -k "validate or redeem or redeemed"`
Expected: FAIL with `AttributeError`.

- [ ] **Step 5: Implement in `coupons.py`**

Add to `CouponsMixin`, after `create_coupon_code`:

```python
    async def validate_coupons(
        self,
        coupons: list[str],
        plenty_id: int,
        ship_to_country: int,
        data: OrderCouponValidatePayload,
        call_from_scheduler: bool | None = None,
        tax_id_number: str | None = None,
        contact_class: int | None = None,
        contact_type: int | None = None,
    ) -> list[dict[str, Any]]:
        """Validate multiple coupon codes at once, without redeeming them.

        Args:
            coupons: Coupon codes to validate.
            plenty_id: The client (store) ID.
            ship_to_country: Country ID of the delivery destination.
            data: Contact and basket payload. Use
                :class:`~plentymarkets._types.OrderCouponValidatePayload`
                for IDE autocomplete. Required keys: ``contactId``,
                ``items``.
            call_from_scheduler: Whether this validation is requested by a
                subscription-order scheduler run.
            tax_id_number: The contact's tax ID number.
            contact_class: The contact's class.
            contact_type: The contact's type.

        Returns:
            A list of validation result dicts, one per coupon, each with:

            - ``campaignId`` (int): The coupon's campaign ID.
            - ``validationType`` (str): The validation mode used.
            - ``contactId`` (int): The contact the coupon was validated
              for.
            - ``couponCode`` (str): The validated coupon code.
            - ``currency`` (str): Currency used for discount amounts.
            - ``exchangeRate`` (float): Exchange rate applied.
            - ``referrer`` (float): Referrer ID used.
            - ``salesDiscount`` (float): Total sales discount granted.
            - ``salesDiscountNet`` (float): Net sales discount granted.
            - ``itemDiscount`` (float): Total item-level discount granted.
            - ``shippingDiscount`` (float): Shipping discount granted.
            - ``restCouponAmount`` (float): Remaining unused coupon
              balance.
            - ``checkedItems`` (list): Basket items the coupon was checked
              against.
        """
        params = self._build_params(
            None,
            coupons=",".join(coupons),
            plentyId=plenty_id,
            shipToCountry=ship_to_country,
            callFromScheduler=call_from_scheduler,
            taxIdNumber=tax_id_number,
            contactClass=contact_class,
            contactType=contact_type,
        )
        return await self._session.post(  # type: ignore[return-value]
            "/rest/orders/coupons/codes", params=params, json=data
        )

    async def list_redeemed_coupon_codes(
        self, contact_id: int, page: int = 1, items_per_page: int = 50
    ) -> dict[str, Any]:
        """List coupon codes redeemed by a contact, with pagination.

        Args:
            contact_id: The contact ID.
            page: Page number (1-indexed).
            items_per_page: Results per page.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of redeemed codes.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Redeemed-code dicts, each with:

                - ``code`` (str): The coupon code.
                - ``contactId`` (int): The contact who redeemed it.
                - ``openAmount`` (float): Remaining unused balance.
                - ``redeemCount`` (int): Number of times redeemed.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
                - ``campaignId`` (int): The code's campaign ID.
                - ``externalTransactionId`` (str): External transaction
                  reference, if any.
        """
        params = self._build_params(
            None, page=page, itemsPerPage=items_per_page
        )
        return await self._session.get(
            f"/rest/orders/coupons/codes/contacts/{contact_id}", params=params
        )

    async def paginate_redeemed_coupon_codes(
        self, contact_id: int, items_per_page: int = 50
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every coupon code redeemed by a
        contact across all pages.

        Args:
            contact_id: The contact ID.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual redeemed-code dicts (see
            :meth:`list_redeemed_coupon_codes` for the field reference).
        """
        page = 1
        while True:
            result = await self.list_redeemed_coupon_codes(
                contact_id, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def validate_coupon(
        self,
        coupon: str,
        plenty_id: int,
        ship_to_country: int,
        data: OrderCouponValidatePayload,
        call_from_scheduler: bool | None = None,
        tax_id_number: str | None = None,
        contact_class: int | None = None,
        contact_type: int | None = None,
    ) -> dict[str, Any]:
        """Validate a single coupon code, without redeeming it.

        Args:
            coupon: The coupon code to validate.
            plenty_id: The client (store) ID.
            ship_to_country: Country ID of the delivery destination.
            data: Contact and basket payload (see :meth:`validate_coupons`).
            call_from_scheduler: Whether this validation is requested by a
                subscription-order scheduler run.
            tax_id_number: The contact's tax ID number.
            contact_class: The contact's class.
            contact_type: The contact's type.

        Returns:
            A single validation result dict (see :meth:`validate_coupons`
            for the field reference).
        """
        params = self._build_params(
            None,
            plentyId=plenty_id,
            shipToCountry=ship_to_country,
            callFromScheduler=call_from_scheduler,
            taxIdNumber=tax_id_number,
            contactClass=contact_class,
            contactType=contact_type,
        )
        return await self._session.post(
            f"/rest/orders/coupons/codes/{coupon}", params=params, json=data
        )

    async def redeem_coupon(self, order_id: int, coupon: str) -> dict[str, Any]:
        """Redeem a coupon code against an order.

        Args:
            order_id: The PlentyMarkets order ID to redeem the coupon on.
            coupon: The coupon code to redeem.

        Returns:
            A validation result dict describing the redemption (see
            :meth:`validate_coupons` for the field reference).
        """
        return await self._session.post(f"/rest/orders/{order_id}/coupons/{coupon}")

    async def validate_order_coupon(self, order_id: int, coupon: str) -> list[Any]:
        """Validate a coupon code against an existing order, without
        redeeming it.

        Note:
            The spec types both ``orderId`` and ``coupon`` as ``integer``
            path segments on this operation — inconsistent with
            :meth:`redeem_coupon`'s sibling endpoint, where ``coupon`` is
            typed ``string``. ``coupon`` is treated as ``str`` here
            uniformly. Response items are also declared as an untyped
            (``mixed``) schema; verify against a live system before relying
            on this endpoint's shape.

        Args:
            order_id: The PlentyMarkets order ID.
            coupon: The coupon code to validate.

        Returns:
            An unverified list of validation result entries.
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/coupons/{coupon}/validate"
        )
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_coupons.py -v`
Expected: all 12 tests in the file pass. Then run the full suite: `uv run pytest`.

- [ ] **Step 7: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.validate_coupons` — validate multiple coupon codes via `POST /rest/orders/coupons/codes`
- feat: `OrdersModule.list_redeemed_coupon_codes` / `paginate_redeemed_coupon_codes` — list/iterate a contact's redeemed coupon codes via `GET /rest/orders/coupons/codes/contacts/{contactId}`
- feat: `OrdersModule.validate_coupon` — validate a single coupon code via `POST /rest/orders/coupons/codes/{coupon}`
- feat: `OrdersModule.redeem_coupon` — redeem a coupon code against an order via `POST /rest/orders/{orderId}/coupons/{coupon}`
- feat: `OrdersModule.validate_order_coupon` — validate a coupon against an existing order via `POST /rest/orders/{orderId}/coupons/{coupon}/validate`
- feat: `OrderCouponValidatePayload` — TypedDict for `validate_coupons`/`validate_coupon`
- `Order` reaches 109/307 endpoint coverage under the `Order` API tag (coupons milestone complete)
```

- [ ] **Step 8: Update `ROADMAP.md`**

```
| POST | `/rest/orders/coupons/codes` | Validate multiple coupons | **implemented** | `orders.validate_coupons` |
| GET | `/rest/orders/coupons/codes/contacts/{contactId}` | List redeemed coupon codes of a contact | **implemented** | `orders.list_redeemed_coupon_codes` |
| POST | `/rest/orders/coupons/codes/{coupon}` | Validate a coupon | **implemented** | `orders.validate_coupon` |
| POST | `/rest/orders/{orderId}/coupons/{coupon}` | Redeem a coupon code | **implemented** | `orders.redeem_coupon` |
| POST | `/rest/orders/{orderId}/coupons/{coupon}/validate` | Validate coupon for order | **implemented** | `orders.validate_order_coupon` |
```

Update the top-of-file summary: `**209 / 1837**` → `**214 / 1837**`, and the `Order` row
`**104/307**` → `**109/307**` (both places).

- [ ] **Step 9: Commit**

```bash
git add src/plentymarkets/modules/orders/coupons.py \
        src/plentymarkets/_types.py src/plentymarkets/__init__.py \
        tests/test_orders_coupons.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add coupon validation and order redemption"
```

---

## Task 15: `taric.py` — new file, TARIC VAT assignment CRUD

**Files:**
- Create: `src/plentymarkets/modules/orders/taric.py`
- Modify: `src/plentymarkets/modules/orders/__init__.py`
- Test: Create `tests/test_orders_taric.py`

**Interfaces:**
- Consumes: `OrdersBase._build_params`, `OrdersBase._session`
- Produces:
  - `TaricMixin` class (new), added to `OrdersModule`'s bases
  - `TaricMixin.list_taric_vat_assignments(page: int = 1, items_per_page: int = 50, country_id: int | None = None, taric_code: str | None = None) -> dict[str, Any]`
  - `TaricMixin.paginate_taric_vat_assignments(country_id: int | None = None, taric_code: str | None = None, items_per_page: int = 50) -> AsyncIterator[dict[str, Any]]`
  - `TaricMixin.delete_taric_vat_assignment(taric_code: str, country_id: int) -> dict[str, Any]`
  - `TaricMixin.get_taric_vat_assignment(taric_code: str, country_id: int) -> dict[str, Any]`
  - `TaricMixin.create_taric_vat_assignment(taric_code: str, country_id: int, vat_field: str) -> dict[str, Any]`
  - `TaricMixin.update_taric_vat_assignment(taric_code: str, country_id: int, vat_field: str) -> dict[str, Any]`

None of these 5 endpoints are deprecated. This is the last task that adds new endpoints — after
this task, Order tag coverage reaches 114/307.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_orders_taric.py`:

```python
import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_list_taric_vat_assignments_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_taric_vat_assignments()
    assert result["page"] == 1


async def test_paginate_taric_vat_assignments_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [
        t async for t in orders.paginate_taric_vat_assignments(items_per_page=2)
    ]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_delete_taric_vat_assignment_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={},
    )
    result = await orders.delete_taric_vat_assignment("8471", 1)
    assert result == {}
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_get_taric_vat_assignment_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={"id": 1, "taricCode": "8471", "countryId": 1, "vatField": "1"},
    )
    result = await orders.get_taric_vat_assignment("8471", 1)
    assert result["taricCode"] == "8471"


async def test_create_taric_vat_assignment_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={"id": 1, "taricCode": "8471", "countryId": 1, "vatField": "1"},
    )
    result = await orders.create_taric_vat_assignment("8471", 1, vat_field="1")
    assert result["id"] == 1
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "taricCode": "8471",
        "countryId": 1,
        "vatField": "1",
    }


async def test_update_taric_vat_assignment_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={"id": 1, "taricCode": "8471", "countryId": 1, "vatField": "2"},
    )
    result = await orders.update_taric_vat_assignment("8471", 1, vat_field="2")
    assert result["vatField"] == "2"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "taricCode": "8471",
        "countryId": 1,
        "vatField": "2",
    }
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_orders_taric.py -v`
Expected: FAIL — `taric.py` does not exist yet.

- [ ] **Step 3: Create `taric.py`**

```python
from __future__ import annotations

from typing import Any, AsyncIterator

from ._base import OrdersBase


class TaricMixin(OrdersBase):
    """TARIC VAT assignment configuration (`/rest/system/settings/taric_vat_assignment`).

    Tagged ``Order`` in PlentyMarkets' OpenAPI spec, but this is genuinely
    tax/system configuration (mapping TARIC customs codes to VAT rates per
    country), not order data.
    """

    async def list_taric_vat_assignments(
        self,
        page: int = 1,
        items_per_page: int = 50,
        country_id: int | None = None,
        taric_code: str | None = None,
    ) -> dict[str, Any]:
        """List TARIC VAT assignments, with pagination and filters.

        Note:
            The spec types ``taricCode`` as ``integer`` for this filter,
            inconsistent with the ``string`` path-param type used on the
            single-resource endpoints below — treated as ``str`` here
            uniformly (TARIC codes match ``^[0-9a-z]{1,14}$``).

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page.
            country_id: Filter by country ID.
            taric_code: Filter by TARIC code.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching assignments.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Assignment dicts (see
              :meth:`get_taric_vat_assignment` for the field reference).
        """
        params = self._build_params(
            None,
            page=page,
            itemsPerPage=items_per_page,
            countryId=country_id,
            taricCode=taric_code,
        )
        return await self._session.get(
            "/rest/system/settings/taric_vat_assignment", params=params
        )

    async def paginate_taric_vat_assignments(
        self,
        country_id: int | None = None,
        taric_code: str | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every TARIC VAT assignment across all
        pages.

        Args:
            country_id: Filter by country ID.
            taric_code: Filter by TARIC code.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual assignment dicts (see
            :meth:`get_taric_vat_assignment` for the field reference).
        """
        page = 1
        while True:
            result = await self.list_taric_vat_assignments(
                page=page,
                items_per_page=items_per_page,
                country_id=country_id,
                taric_code=taric_code,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def delete_taric_vat_assignment(
        self, taric_code: str, country_id: int
    ) -> dict[str, Any]:
        """Delete a TARIC VAT assignment.

        Note:
            The spec declares a requestBody for this DELETE operation that
            just redeclares ``taricCode``/``countryId`` — both already
            supplied as path parameters and nothing new. No body is sent,
            matching how :meth:`delete_status_definition`/
            :meth:`delete_order_item` never resend path-supplied fields.

        Args:
            taric_code: The TARIC customs code.
            country_id: The country ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}"
        )

    async def get_taric_vat_assignment(
        self, taric_code: str, country_id: int
    ) -> dict[str, Any]:
        """Get a single TARIC VAT assignment.

        Args:
            taric_code: The TARIC customs code.
            country_id: The country ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The assignment record ID.
            - ``taricCode`` (str): The TARIC customs code.
            - ``countryId`` (int): The country ID.
            - ``vatField`` (str): The VAT rate ID for this TARIC
              code/country combination.
        """
        return await self._session.get(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}"
        )

    async def create_taric_vat_assignment(
        self, taric_code: str, country_id: int, vat_field: str
    ) -> dict[str, Any]:
        """Create a TARIC VAT assignment.

        Args:
            taric_code: The TARIC customs code, matching
                ``^[0-9a-z]{1,14}$``.
            country_id: The country ID this configuration belongs to.
            vat_field: The VAT rate ID for this TARIC code/country
                combination.

        Returns:
            The created assignment dict (see
            :meth:`get_taric_vat_assignment` for the field reference).
        """
        return await self._session.post(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}",
            json={
                "taricCode": taric_code,
                "countryId": country_id,
                "vatField": vat_field,
            },
        )

    async def update_taric_vat_assignment(
        self, taric_code: str, country_id: int, vat_field: str
    ) -> dict[str, Any]:
        """Update a TARIC VAT assignment.

        Args:
            taric_code: The TARIC customs code.
            country_id: The country ID.
            vat_field: The new VAT rate ID for this TARIC code/country
                combination.

        Returns:
            The updated assignment dict (see
            :meth:`get_taric_vat_assignment` for the field reference).
        """
        return await self._session.put(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}",
            json={
                "taricCode": taric_code,
                "countryId": country_id,
                "vatField": vat_field,
            },
        )
```

- [ ] **Step 4: Wire `TaricMixin` into `OrdersModule`**

In `src/plentymarkets/modules/orders/__init__.py`, replace:

```python
from .status_history import StatusHistoryMixin
from .statuses import StatusMixin
from .transactions import TransactionsMixin
```

with:

```python
from .status_history import StatusHistoryMixin
from .statuses import StatusMixin
from .taric import TaricMixin
from .transactions import TransactionsMixin
```

and replace:

```python
    CurrenciesMixin,
    CouponsMixin,
    OrdersBase,
):
```

with:

```python
    CurrenciesMixin,
    CouponsMixin,
    TaricMixin,
    OrdersBase,
):
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_orders_taric.py -v`
Expected: all 6 tests pass. Then run `uv run pytest` (full suite) — this is the last
new-endpoint task, so this full-suite run should show all 69 endpoints' tests green together.

- [ ] **Step 6: Update `CHANGELOG.md`**

Add under the `### Order` section:

```markdown
- feat: `OrdersModule.list_taric_vat_assignments` / `paginate_taric_vat_assignments` — list/iterate TARIC VAT assignments via `GET /rest/system/settings/taric_vat_assignment`
- feat: `OrdersModule.delete_taric_vat_assignment` — delete a TARIC VAT assignment via `DELETE /rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}`
- feat: `OrdersModule.get_taric_vat_assignment` — get one TARIC VAT assignment via `GET /rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}`
- feat: `OrdersModule.create_taric_vat_assignment` — create a TARIC VAT assignment via `POST /rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}`
- feat: `OrdersModule.update_taric_vat_assignment` — update a TARIC VAT assignment via `PUT /rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}`
- `Order` reaches 114/307 endpoint coverage under the `Order` API tag (Phase 4 "core order metadata" milestone complete: batch/contact/accounting lookups, order-item dates, order & order-item properties, referrers, currencies, coupons, TARIC VAT assignments)
- refactor: `modules/orders/` gains a `taric.py` mixin (`TaricMixin`) — no public API change
```

- [ ] **Step 7: Update `ROADMAP.md`**

```
| GET | `/rest/system/settings/taric_vat_assignment` | List taric vat assignments | **implemented** | `orders.list_taric_vat_assignments` |
| DELETE | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Delete taric vat assignment | **implemented** | `orders.delete_taric_vat_assignment` |
| GET | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Get taric vat assignment | **implemented** | `orders.get_taric_vat_assignment` |
| POST | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Create taric vat assignment | **implemented** | `orders.create_taric_vat_assignment` |
| PUT | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Update taric vat assignment | **implemented** | `orders.update_taric_vat_assignment` |
```

Update the top-of-file summary: `**214 / 1837**` → `**219 / 1837**`, and the `Order` row
`**109/307**` → `**114/307**` (both places, and the `### Order` section's own
`45/307 implemented.` line → `114/307 implemented.`).

- [ ] **Step 8: Commit**

```bash
git add src/plentymarkets/modules/orders/taric.py \
        src/plentymarkets/modules/orders/__init__.py \
        tests/test_orders_taric.py CHANGELOG.md ROADMAP.md
git commit -m "feat(orders): add TARIC VAT assignment CRUD"
```

---

## Task 16: Final verification and version bump

**Files:**
- Modify: `pyproject.toml` (version bump, handled by `cz bump`)
- Modify: `CHANGELOG.md` (versioning of `[Unreleased]`, handled by `cz bump`'s pre-bump hook)
- Read-only check: `ROADMAP.md`

**Interfaces:**
- Consumes: `commitizen` (`cz`), already configured in `pyproject.toml`
  (`[tool.commitizen]`: `version = "0.3.2"`, `tag_format = "v$version"`,
  `version_files = ["pyproject.toml:version"]`,
  `pre_bump_hooks = ["python3 scripts/bump_changelog.py"]`)
- Produces: `pyproject.toml` version `0.4.0`, a versioned `## [0.4.0] - <date>` section in
  `CHANGELOG.md`, a `bump:` commit, and a `v0.4.0` git tag.

This phase covers 69 of the 307 `Order`-tagged endpoints (Phase 4 of the roadmap in
`/home/hammer/.claude/plans/pls-plan-the-next-goofy-origami.md`) — Shipping (58 endpoints,
Phase 5) and the 13 document-type resources (135 endpoints, Phase 6+) remain for future plans.
This task verifies only the 69 endpoints in scope here, not full `Order` tag coverage.

---

- [ ] **Step 1: Confirm every endpoint touched by Tasks 1-15 is marked implemented in `ROADMAP.md`**

Run:

```bash
grep -A320 '### `Order`' ROADMAP.md | grep -E '\| planned \|'
```

Expected: none of the 69 paths listed across Tasks 1-15's "Step: Update `ROADMAP.md`" sections
appear in the output — every row this phase touched now reads `**implemented**` (with the
`deprecated (...)` annotation preserved alongside it where applicable, per Task 6/8's
convention). Rows for endpoints *outside* this phase's scope (Shipping, document-type resources)
are expected to still read `planned` or `deprecated (...)` — that's correct; don't touch them.

Also confirm the running per-task coverage math landed correctly:

```bash
grep -m1 '^\*\*.*implemented\*\*' ROADMAP.md
grep -m1 '45/307\|114/307' ROADMAP.md
```

Expected: the top-of-file summary reads `**219 / 1837**` and the `Order` row/section both read
`114/307` (not `45/307` — if either still shows the old number, an earlier task's Step 6/7/8/9
ROADMAP update was missed; go back and fix it before proceeding).

- [ ] **Step 2: Run the full test suite**

Run: `uv run pytest -v`
Expected: every test passes, zero failures. This includes the original 45-endpoint orders test
suite (`test_orders_core.py`, `test_orders_dates.py`, `test_orders_items.py`,
`test_orders_reorders.py`, `test_orders_statuses.py`, `test_orders_status_history.py`,
`test_orders_transactions.py`) plus this phase's ~85 new tests across those same two extended
files and the 5 new `test_orders_properties.py`/`test_orders_referrers.py`/
`test_orders_currencies.py`/`test_orders_coupons.py`/`test_orders_taric.py` files, plus every
pre-existing pim/items/stock/contacts/session test suite.

- [ ] **Step 3: Run the project's type checker**

Run: `uv run mypy src/` (or the project's configured equivalent — check `pyproject.toml`
`[tool.mypy]`/`[tool.pyright]` if unsure which is wired up).
Expected: no new errors introduced by this phase's ~74 new methods, 8 new TypedDicts, and 5 new
mixin files. Pay particular attention to the `# type: ignore[return-value]` spots added in
Tasks 1, 6, 10, 12, 14, 15 (`get_orders_batch`, `list_item_dates`, `list_item_properties`,
`list_currencies`, `list_currency_countries`, `list_exchange_rates_from`/`to`, `validate_coupons`,
`validate_order_coupon`, `list_property_types`) — confirm each is still necessary and not masking
an unrelated type error.

- [ ] **Step 4: Run the version bump**

```bash
uv run cz bump --increment MINOR
```

This reads `[tool.commitizen]` from `pyproject.toml`, runs `scripts/bump_changelog.py`
(versioning the `[Unreleased]` section into `## [0.4.0] - <today's date>`), updates
`pyproject.toml`'s `version = "0.4.0"`, and creates a `bump: version 0.3.2 → 0.4.0` commit plus a
`v0.4.0` tag automatically — no manual `git commit` step needed here, unlike every prior task.

- [ ] **Step 5: Verify the bump**

```bash
git log --oneline -3
grep '^version' pyproject.toml
grep -m1 '^## \[' CHANGELOG.md
```

Expected: the log shows the new `bump:` commit at HEAD, `pyproject.toml` reads
`version = "0.4.0"`, and `CHANGELOG.md`'s first `## [...]` heading reads `## [0.4.0] - <today's
date>` with an empty `## [Unreleased]` section above it.

---

## Plan Complete

Once Task 16 lands, `OrdersModule` covers 114/307 `Order`-tagged endpoints (up from 45/307), the
package is at `0.4.0`, and the single feature branch (per `CLAUDE.md`'s branch workflow) is
ready to merge back into `staging`. The next phase (Shipping, 58 endpoints, or the first
document-type resource — see the roadmap plan file referenced above) can be planned separately
once this one is merged.
