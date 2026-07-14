from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from ..._types import OrderItemTransactionCreatePayload

from ._base import OrdersBase


class TransactionsMixin(OrdersBase):
    """Order item transaction (stock movement) management.

    These methods manage transactions (stock movements) recorded against
    order items, via the flat `/rest/orders/items/transactions/*` family
    (addressed by transaction ID) and the `/rest/orders/items/{orderItemId}
    /transactions` family (scoped to one order item). Both are current, not
    deprecated. PlentyMarkets also exposes an order-item *dates* family and
    an order/order-item *properties* family under similar paths, but every
    endpoint in both is deprecated in favor of `PUT /rest/orders/{orderId}`
    — this client intentionally does not implement deprecated endpoints, so
    neither family is implemented here or elsewhere in this package.
    """

    async def search_item_transactions(
        self,
        order_item_id: int | None = None,
        order_id: int | None = None,
        direction: str | None = None,
        status: str | None = None,
        is_booked: bool | None = None,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """Search order item transactions with filters.

        Note:
            PlentyMarkets documents the ``status`` filter here as ``"in"``
            (incoming) or ``"out"`` (outgoing) — i.e. it actually filters on
            *direction*. This is a different value domain than the
            ``status`` field on the returned transaction objects, which is
            ``"regular"`` or ``"cancelled"``. Likely a spec documentation
            inconsistency; verify against a live system before relying on
            this filter.

        Args:
            order_item_id: Filter by order item ID.
            order_id: Filter by order ID.
            direction: Filter by transaction direction, ``"in"`` or ``"out"``.
            status: Filter by transaction "status" as documented by the API
                (``"in"``/``"out"`` — see Note above).
            is_booked: When set, only return booked (or unbooked)
                transactions.
            columns: Restrict the response to these transaction properties.
            with_: Related data to embed. Available: ``"orderItem"``,
                ``"warehouseLocation"``.
            sort_by: Sort field. One of ``"createdAt"``, ``"updatedAt"``,
                ``"orderItemId"``, ``"receiptId"``, ``"quantity"``. Defaults
                to ``"orderItemId"``.
            sort_order: Sort direction, ``"asc"`` or ``"desc"``. Defaults to
                ``"asc"``.
            page: Page number (1-indexed).
            items_per_page: Results per page.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching transactions.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Order item transaction dicts, each
              with:

                - ``id`` (int): The transaction ID.
                - ``orderItemId`` (int): The order item this transaction
                  belongs to.
                - ``quantity`` (float): The transacted quantity.
                - ``userId`` (int): ID of the user attributed to the
                  transaction.
                - ``identification`` (str): Arbitrary external
                  identification string.
                - ``direction`` (str): ``"in"`` or ``"out"``.
                - ``status`` (str): ``"regular"`` or ``"cancelled"``.
                - ``receiptId`` (int): Receipt ID the transaction is linked
                  to.
                - ``warehouseLocationId`` (int): Warehouse location ID.
                - ``batch`` (str): Batch identifier of the transacted stock.
                - ``bestBeforeDate`` (str): Best-before date, ISO 8601.
                - ``batchBestBeforeDateId`` (int): Deprecated by
                  PlentyMarkets; replaced by ``batch`` and
                  ``bestBeforeDate``.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        params = self._build_params(
            None,
            with_=with_,
            columns=",".join(columns) if columns else None,
            orderItemId=order_item_id,
            orderId=order_id,
            direction=direction,
            status=status,
            isBooked=is_booked,
            sortBy=sort_by,
            sortOrder=sort_order,
            page=page,
            itemsPerPage=items_per_page,
        )
        return await self._session.get(
            "/rest/orders/items/transactions", params=params
        )

    async def paginate_item_transactions(
        self,
        order_item_id: int | None = None,
        order_id: int | None = None,
        direction: str | None = None,
        status: str | None = None,
        is_booked: bool | None = None,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every order item transaction across all pages.

        Args:
            order_item_id: Filter by order item ID.
            order_id: Filter by order ID.
            direction: Filter by transaction direction, ``"in"`` or ``"out"``.
            status: Filter by transaction "status" as documented by the API
                (see the Note on :meth:`search_item_transactions`).
            is_booked: When set, only return booked (or unbooked)
                transactions.
            columns: Restrict the response to these transaction properties.
            with_: Related data to embed (see
                :meth:`search_item_transactions`).
            sort_by: Sort field (see :meth:`search_item_transactions`).
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual order item transaction dicts (see
            :meth:`search_item_transactions` for the field reference).
        """
        page = 1
        while True:
            result = await self.search_item_transactions(
                order_item_id=order_item_id,
                order_id=order_id,
                direction=direction,
                status=status,
                is_booked=is_booked,
                columns=columns,
                with_=with_,
                sort_by=sort_by,
                sort_order=sort_order,
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

    async def update_item_transaction(
        self,
        transaction_id: int,
        warehouse_location_id: int | None = None,
        batch: str | None = None,
        best_before_date: str | None = None,
    ) -> dict[str, Any]:
        """Update an order item transaction.

        Args:
            transaction_id: The transaction ID.
            warehouse_location_id: New warehouse location ID.
            batch: New batch identifier.
            best_before_date: New best-before date, ISO 8601.

        Returns:
            The updated transaction dict (see
            :meth:`search_item_transactions` for the field reference).
        """
        data: dict[str, Any] = {}
        if warehouse_location_id is not None:
            data["warehouseLocationId"] = warehouse_location_id
        if batch is not None:
            data["batch"] = batch
        if best_before_date is not None:
            data["bestBeforeDate"] = best_before_date
        return await self._session.put(
            f"/rest/orders/items/transactions/{transaction_id}", json=data
        )

    async def delete_item_transaction(self, transaction_id: int) -> dict[str, Any]:
        """Delete an order item transaction.

        Note:
            PlentyMarkets' published OpenAPI spec declares no fields at all
            for the response of this endpoint (a bare placeholder schema).
            Response shape is unverified. Verify against a live system
            before relying on it.

        Args:
            transaction_id: The transaction ID.

        Returns:
            The API's response dict; likely empty on success.
        """
        return await self._session.delete(
            f"/rest/orders/items/transactions/{transaction_id}"
        )

    async def book_item_transactions(
        self,
        transaction_ids: list[int],
        delivery_note_number: str | None = None,
    ) -> dict[str, Any]:
        """Bulk-book order item transactions by ID.

        Note:
            PlentyMarkets' published OpenAPI spec declares no fields at all
            for the response of this endpoint (a bare placeholder schema).
            Response shape is unverified. Verify against a live system
            before relying on it.

        Args:
            transaction_ids: IDs of the transactions to book.
            delivery_note_number: For incoming items, an external delivery
                note number. For outgoing items, an external or internal
                delivery note number.

        Returns:
            The API's response dict.
        """
        params = self._build_params(
            None,
            transactionIds=",".join(str(t) for t in transaction_ids),
            deliveryNoteNumber=delivery_note_number,
        )
        return await self._session.post(
            "/rest/orders/items/transactions/booking", params=params
        )

    async def list_item_transactions(
        self,
        order_item_id: int,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """List all transactions of a single order item.

        Args:
            order_item_id: The order item ID.
            columns: Restrict the response to these transaction properties.
            with_: Related data to embed (see
                :meth:`search_item_transactions`).

        Returns:
            A list of transaction dicts (see :meth:`search_item_transactions`
            for the field reference).
        """
        params = self._build_params(
            None,
            with_=with_,
            columns=",".join(columns) if columns else None,
        )
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/items/{order_item_id}/transactions", params=params
        )

    async def create_item_transaction(
        self, order_item_id: int, data: OrderItemTransactionCreatePayload
    ) -> dict[str, Any]:
        """Create a transaction for an order item.

        Args:
            order_item_id: The order item ID.
            data: Transaction payload. Use
                :class:`~plentymarkets._types.OrderItemTransactionCreatePayload`
                for IDE autocomplete. Required keys: ``quantity``,
                ``direction``, ``status``. ``orderItemId`` is merged in
                automatically from ``order_item_id`` and must not be
                included.

        Returns:
            The created transaction dict (see
            :meth:`search_item_transactions` for the field reference).
        """
        return await self._session.post(
            f"/rest/orders/items/{order_item_id}/transactions",
            json={**data, "orderItemId": order_item_id},
        )

    async def book_item_in(
        self, order_item_id: int, delivery_note_number: str | None = None
    ) -> dict[str, Any]:
        """Book an order item's full quantity in.

        Note:
            Distinct from :meth:`book_item_transactions`, which bulk-books
            specific transaction IDs rather than a whole order item.
            PlentyMarkets' published OpenAPI spec declares no fields at all
            for the response of this endpoint (a bare placeholder schema).
            Response shape is unverified. Verify against a live system
            before relying on it.

        Args:
            order_item_id: The order item ID.
            delivery_note_number: Delivery note number provided by the
                supplier.

        Returns:
            The API's response dict.
        """
        params = self._build_params(None, deliveryNoteNumber=delivery_note_number)
        return await self._session.post(
            f"/rest/orders/items/{order_item_id}/booking", params=params
        )
