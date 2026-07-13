from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from ..._types import OrderCreatePayload

from ._base import OrdersBase


class CoreMixin(OrdersBase):
    """Order CRUD, search, and family/account-URL lookups."""

    async def get(self, order_id: int) -> dict[str, Any]:
        """Get a single order by ID.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The order ID.
            - ``typeId`` (int): Order type. 1=order, 2=delivery, 3=returns,
              4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
              9=multiorder.
            - ``statusId`` (float): Current order status ID (e.g. ``5.0``).
            - ``ownerId`` (int): ID of the user who owns the order.
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``locationId`` (int): Accounting location ID.
            - ``warehouseId`` (int): Warehouse ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``orderItems`` (list[dict]): List of order item dicts.
            - ``addressRelations`` (list[dict]): Billing/delivery address
              relations.
            - ``orderProperties`` (list[dict]): Custom order properties.
            - ``amounts`` (list[dict]): Order amount breakdowns per currency.
            - ``dates`` (list[dict]): Significant dates (e.g. payment due).
            - ``relations`` (list[dict]): Related contacts, warehouses, etc.
        """
        return await self._session.get(f"/rest/orders/{order_id}")

    async def list(self, page: int = 1, items_per_page: int = 50) -> dict[str, Any]:
        """List orders with pagination.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching orders.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Order dicts, each with:

                - ``id`` (int): The order ID.
                - ``typeId`` (int): Order type. 1=order, 2=delivery, 3=returns,
                  4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
                  9=multiorder.
                - ``statusId`` (float): Current order status ID (e.g. ``5.0``).
                - ``ownerId`` (int): ID of the user who owns the order.
                - ``referrerId`` (float): Sales referrer ID.
                - ``plentyId`` (int): Client (store) ID.
                - ``locationId`` (int): Accounting location ID.
                - ``warehouseId`` (int): Warehouse ID.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
                - ``orderItems`` (list[dict]): List of order item dicts.
                - ``addressRelations`` (list[dict]): Billing/delivery address
                  relations.
                - ``orderProperties`` (list[dict]): Custom order properties.
                - ``amounts`` (list[dict]): Order amount breakdowns per currency.
                - ``dates`` (list[dict]): Significant dates (e.g. payment due).
                - ``relations`` (list[dict]): Related contacts, warehouses, etc.
        """
        return await self._session.get(
            "/rest/orders",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def create(self, data: OrderCreatePayload) -> dict[str, Any]:
        """Create a new order.

        Args:
            data: Order payload. Use :class:`~plentymarkets._types.OrderCreatePayload`
                for IDE autocomplete. Required keys: ``typeId``, ``plentyId``.
                Optional keys: ``statusId``, ``ownerId``, ``lockStatus``,
                ``orderItems``, ``properties``, ``addressRelations``, ``relations``.

        Returns:
            The created order dict with the following keys:

            - ``id`` (int): The order ID.
            - ``typeId`` (int): Order type. 1=order, 2=delivery, 3=returns,
              4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
              9=multiorder.
            - ``statusId`` (float): Current order status ID (e.g. ``5.0``).
            - ``ownerId`` (int): ID of the user who owns the order.
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``locationId`` (int): Accounting location ID.
            - ``warehouseId`` (int): Warehouse ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``orderItems`` (list[dict]): List of order item dicts.
            - ``addressRelations`` (list[dict]): Billing/delivery address relations.
            - ``orderProperties`` (list[dict]): Custom order properties.
            - ``amounts`` (list[dict]): Order amount breakdowns per currency.
            - ``dates`` (list[dict]): Significant dates (e.g. payment due).
            - ``relations`` (list[dict]): Related contacts, warehouses, etc.
        """
        return await self._session.post("/rest/orders", json=data)

    async def update_status(self, order_id: int, status_id: float) -> dict[str, Any]:
        """Update the status of an order.

        Args:
            order_id: The PlentyMarkets order ID.
            status_id: Target status ID (e.g. ``5.0`` = cleared for shipping,
                ``7.0`` = outgoing items booked, ``8.0`` = cancelled).

        Returns:
            The updated order dict with the following keys:

            - ``id`` (int): The order ID.
            - ``typeId`` (int): Order type. 1=order, 2=delivery, 3=returns,
              4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
              9=multiorder.
            - ``statusId`` (float): Current order status ID (e.g. ``5.0``).
            - ``ownerId`` (int): ID of the user who owns the order.
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``locationId`` (int): Accounting location ID.
            - ``warehouseId`` (int): Warehouse ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``orderItems`` (list[dict]): List of order item dicts.
            - ``addressRelations`` (list[dict]): Billing/delivery address relations.
            - ``orderProperties`` (list[dict]): Custom order properties.
            - ``amounts`` (list[dict]): Order amount breakdowns per currency.
            - ``dates`` (list[dict]): Significant dates (e.g. payment due).
            - ``relations`` (list[dict]): Related contacts, warehouses, etc.
        """
        return await self._session.put(
            f"/rest/orders/{order_id}", json={"statusId": status_id}
        )

    async def paginate_orders(
        self, items_per_page: int = 50
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every order across all pages.

        Args:
            items_per_page: Results per page request (max 250).

        Yields:
            Individual order dicts, each with the following keys:

            - ``id`` (int): The order ID.
            - ``typeId`` (int): Order type. 1=order, 2=delivery, 3=returns,
              4=credit note, 5=warranty, 6=repair, 7=offer, 8=advance order,
              9=multiorder.
            - ``statusId`` (float): Current order status ID (e.g. ``5.0``).
            - ``ownerId`` (int): ID of the user who owns the order.
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``locationId`` (int): Accounting location ID.
            - ``warehouseId`` (int): Warehouse ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``orderItems`` (list[dict]): List of order item dicts.
            - ``addressRelations`` (list[dict]): Billing/delivery address relations.
            - ``orderProperties`` (list[dict]): Custom order properties.
            - ``amounts`` (list[dict]): Order amount breakdowns per currency.
            - ``dates`` (list[dict]): Significant dates (e.g. payment due).
            - ``relations`` (list[dict]): Related contacts, warehouses, etc.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=items_per_page)
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def delete(self, order_id: int) -> dict[str, Any]:
        """Delete an order.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(f"/rest/orders/{order_id}")

    async def cancel(
        self,
        order_id: int,
        status_id: float | None = None,
        message: str | None = None,
    ) -> dict[str, Any]:
        """Cancel an order.

        Args:
            order_id: The PlentyMarkets order ID.
            status_id: Order status ID to set on cancellation.
            message: Message displayed in the order's status history.

        Returns:
            The updated order dict (see :meth:`get` for the field reference).
        """
        data: dict[str, Any] = {}
        if status_id is not None:
            data["statusId"] = status_id
        if message is not None:
            data["message"] = message
        return await self._session.put(f"/rest/orders/{order_id}/cancel", json=data)

    async def get_family(self, order_id: int) -> dict[str, Any]:
        """Get information about an order's family (related advance/sales orders).

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A dict with the following keys:

            - ``originOrderId`` (int): ID of the order this order originated
              from (e.g. the advance order a sales order was converted from).
            - ``mainSalesOrderId`` (int): ID of the main sales order in the
              family.
        """
        return await self._session.get(f"/rest/orders/{order_id}/family")

    async def get_my_account_url(self, order_id: int) -> list[Any]:
        """Get the "My Account" URL(s) for an order.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as an untyped (``mixed``) array rather than a JSON
            schema. Based on the endpoint's purpose, it typically contains a
            single URL string. Verify against a live system before relying
            on its shape.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A list of URL strings pointing to the order in the shop's "My
            Account" area.
        """
        return await self._session.get(f"/rest/orders/{order_id}/my_account_url")  # type: ignore[return-value]

    async def search(
        self,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        lazy_loaded: bool | None = None,
        page: int = 1,
        items_per_page: int = 50,
        use_post: bool = False,
    ) -> dict[str, Any]:
        """Search orders with filters, unlike :meth:`list` which only paginates.

        Args:
            filters: Optional dict of filter query parameters, e.g.
                ``{"orderId": 42, "plentyId": 12345, "statusId": 5.0,
                "referrerId": 1.0, "ownerId": 1, "itemId": 100,
                "contactData": "smith", "hasValidInvoice": True}``. The API
                supports ~45 filter keys, including dynamic ones like
                ``orderProperty_{typeId}`` and ``orderDate_{typeId}`` — pass
                any of them as extra keys in this dict.
            with_: Optional list of related data to embed.
            sort_by: Field name to sort results by.
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            lazy_loaded: Whether to skip loading nested relations for speed.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).
            use_post: When ``True``, send the request as ``POST`` instead of
                ``GET`` (still via query parameters, no JSON body) — useful
                to avoid URL length limits with many filters. Both variants
                hit functionally identical endpoints.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching orders.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``firstOnPage`` (int): Index of the first entry on this page.
            - ``lastOnPage`` (int): Index of the last entry on this page.
            - ``itemsPerPage`` (int): Results per page, as requested.
            - ``entries`` (list[dict]): Order dicts (see :meth:`get` for the
              field reference).
        """
        params = self._build_params(
            filters,
            with_=with_,
            page=page,
            itemsPerPage=items_per_page,
            sortBy=sort_by,
            sortOrder=sort_order,
            lazyLoaded=lazy_loaded,
        )
        method = self._session.post if use_post else self._session.get
        return await method("/rest/orders/search", params=params)

    async def paginate_search(
        self,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        lazy_loaded: bool | None = None,
        items_per_page: int = 50,
        use_post: bool = False,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every order matching a search across all pages.

        Args:
            filters: Optional dict of filter query parameters (see
                :meth:`search`).
            with_: Optional list of related data to embed.
            sort_by: Field name to sort results by.
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            lazy_loaded: Whether to skip loading nested relations for speed.
            items_per_page: Results per page request (max 250).
            use_post: When ``True``, send each page request as ``POST``
                instead of ``GET`` (see :meth:`search`).

        Yields:
            Individual order dicts (see :meth:`get` for the field reference).
        """
        page = 1
        while True:
            result = await self.search(
                filters,
                with_=with_,
                sort_by=sort_by,
                sort_order=sort_order,
                lazy_loaded=lazy_loaded,
                page=page,
                items_per_page=items_per_page,
                use_post=use_post,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

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
