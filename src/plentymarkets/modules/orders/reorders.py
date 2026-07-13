from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import OrderTransactionsCreatePayload

from ._base import OrdersBase


class ReordersMixin(OrdersBase):
    """Warehouse-location attach/detach and reorder generation/creation."""

    async def attach_order_item_warehouse_locations(
        self, order_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Attach warehouse locations to an order's items.

        Note:
            **Schema gap.** PlentyMarkets' published OpenAPI spec declares no
            request body schema at all for this endpoint, and its response
            (``SimpleRestResponse``) is also a bare placeholder with no
            declared fields. ``data`` is passed through as-is; the likely
            shape is a list of order-item-to-warehouse-location mappings,
            but this is unverified. Tracked in ROADMAP.md's "Known Schema
            Gaps" section — verify against a live system and tighten to a
            proper TypedDict once confirmed.

        Args:
            order_id: The PlentyMarkets order ID.
            data: Warehouse location payload; shape unverified (see Note
                above).

        Returns:
            The API's response dict; shape unverified (see Note above).
        """
        return await self._session.post(
            f"/rest/orders/{order_id}/items/warehouse_locations/attach",
            json=data,
        )

    async def detach_order_item_warehouse_locations(
        self, order_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Detach warehouse locations from an order's items.

        Note:
            **Schema gap** — same caveats as
            :meth:`attach_order_item_warehouse_locations`: no request body
            schema and no response schema declared in the spec. Tracked in
            ROADMAP.md's "Known Schema Gaps" section.

        Args:
            order_id: The PlentyMarkets order ID.
            data: Warehouse location payload; shape unverified (see
                :meth:`attach_order_item_warehouse_locations`).

        Returns:
            The API's response dict; shape unverified.
        """
        return await self._session.post(
            f"/rest/orders/{order_id}/items/warehouse_locations/detach",
            json=data,
        )

    async def generate_order_item_reorders(
        self, order_id: int, data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Generate reorder(s) for an order's items.

        Note:
            **Schema gap.** PlentyMarkets' published OpenAPI spec declares no
            request body schema at all for this endpoint, and its response
            items use a generic untyped placeholder schema. ``data`` is
            passed through as-is (omitted entirely when ``None``, since the
            spec doesn't even declare an optional empty body); the likely
            request shape is a list of order item IDs and/or quantities to
            reorder, but this is unverified. Tracked in ROADMAP.md's "Known
            Schema Gaps" section — verify against a live system and tighten
            to a proper TypedDict once confirmed. This is the item-scoped
            sibling of :meth:`generate_order_reorders`.

        Args:
            order_id: The PlentyMarkets order ID.
            data: Reorder-generation payload; shape unverified (see Note
                above).

        Returns:
            A list of untyped dicts; shape unverified (see Note above).
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/items/reorders/generate", json=data
        )

    async def create_order_reorder(
        self, order_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a reorder from a parent order.

        Note:
            **Schema gap.** PlentyMarkets documents this endpoint as
            requiring "the parent order ID and the quantities to use" but
            declares no request body schema at all. ``data`` is passed
            through as-is; exact key names are unverified. Tracked in
            ROADMAP.md's "Known Schema Gaps" section — verify against a live
            system and tighten to a proper TypedDict once confirmed. The
            response reuses the general order object shape (~20 fields);
            only the most useful ones are documented below.

        Args:
            order_id: The PlentyMarkets ID of the parent order.
            data: Reorder payload; shape unverified (see Note above).

        Returns:
            The created reorder dict. Reuses the general order shape (see
            :meth:`~plentymarkets.modules.orders.core.CoreMixin.get`); the
            most useful fields are:

            - ``id`` (int): The new reorder's ID.
            - ``typeId`` (int): Order type (``12`` = reorder).
            - ``statusId`` (float): Current order status ID.
            - ``ownerId`` (int): ID of the user who owns the reorder.
            - ``plentyId`` (int): Client (store) ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.post(
            f"/rest/orders/{order_id}/reorders", json=data
        )

    async def generate_order_reorders(
        self, order_id: int, data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Generate reorder(s) for an order.

        Note:
            **Schema gap** — same caveats as
            :meth:`generate_order_item_reorders`: no request body schema and
            an untyped response item schema declared in the spec. ``data``
            is omitted entirely when ``None``. Tracked in ROADMAP.md's
            "Known Schema Gaps" section. This is the order-scoped sibling of
            :meth:`generate_order_item_reorders` (item-scoped).

        Args:
            order_id: The PlentyMarkets order ID.
            data: Reorder-generation payload; shape unverified (see Note
                above).

        Returns:
            A list of untyped dicts; shape unverified (see Note above).
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/reorders/generate", json=data
        )

    async def validate_order_reorders(
        self, order_id: int, data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Validate an order's items before creating a reorder from them.

        Note:
            **Schema gap** — same caveats as :meth:`create_order_reorder`
            and :meth:`generate_order_reorders`: no request body schema and
            an untyped response item schema declared in the spec. ``data``
            is omitted entirely when ``None``. Tracked in ROADMAP.md's
            "Known Schema Gaps" section.

        Args:
            order_id: The PlentyMarkets ID of the parent order.
            data: Validation payload; shape unverified (see Note above).

        Returns:
            A list of untyped dicts; shape unverified (see Note above).
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/reorders/generate/validate", json=data
        )

    async def create_order_transactions(
        self, order_id: int, data: OrderTransactionsCreatePayload
    ) -> list[dict[str, Any]]:
        """Bulk-create item transactions for every item of an order that lacks one.

        Args:
            order_id: The PlentyMarkets order ID.
            data: Transaction payload. Use
                :class:`~plentymarkets._types.OrderTransactionsCreatePayload`
                for IDE autocomplete. Required keys: ``direction``,
                ``status``.

        Returns:
            A list of transaction dicts, one per order item that received a
            new transaction (see
            :meth:`~plentymarkets.modules.orders.transactions.TransactionsMixin.search_item_transactions`
            for the field reference).
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/transactions", json=data
        )
