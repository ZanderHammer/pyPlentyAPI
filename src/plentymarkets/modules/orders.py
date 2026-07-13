from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import OrderCreatePayload, OrderStatusNamePayload

from .._session import _Session


class OrdersModule:
    """Wraps the PlentyMarkets ``/rest/orders`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<OrdersModule /rest/orders>"

    @staticmethod
    def _build_params(
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        params: dict[str, Any] = dict(filters) if filters else {}
        if with_:
            params["with"] = ",".join(with_)
        params.update({k: v for k, v in extra.items() if v is not None})
        return params

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

    # -- Order status definitions --------------------------------------------
    #
    # These methods manage order *status entities themselves* (their color,
    # visibility flags, and translated names) via `/rest/orders/statuses/*`.
    # This is unrelated to `update_status(order_id, status_id)` above, which
    # sets the `statusId` field *on an order*.

    async def list_status_definitions(
        self,
        status_id_from: float | None = None,
        status_id_to: float | None = None,
        language: str | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """Search order status definitions.

        Args:
            status_id_from: Lower bound (inclusive) of status ID to search from.
            status_id_to: Upper bound (inclusive) of status ID to search to.
            language: Two-letter ISO 639-1 language code to filter/localize
                status names by.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching statuses.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Status definition dicts, each with:

                - ``statusId`` (float): The status ID.
                - ``isErasable`` (bool): Whether the status can be deleted.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
                - ``isFrontendVisible`` (bool): Visibility in the online store.
                - ``isReorderVisible`` (bool): Visibility for reorders.
                - ``isRedistributionVisible`` (bool): Visibility for
                  redistributions.
                - ``color`` (str): Hex color code of the status.
        """
        params = self._build_params(
            None,
            statusIdFrom=status_id_from,
            statusIdTo=status_id_to,
            language=language,
            page=page,
            itemsPerPage=items_per_page,
        )
        return await self._session.get("/rest/orders/statuses", params=params)

    async def paginate_status_definitions(
        self,
        status_id_from: float | None = None,
        status_id_to: float | None = None,
        language: str | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every order status definition across all pages.

        Args:
            status_id_from: Lower bound (inclusive) of status ID to search from.
            status_id_to: Upper bound (inclusive) of status ID to search to.
            language: Two-letter ISO 639-1 language code to filter/localize
                status names by.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual status definition dicts (see
            :meth:`list_status_definitions`).
        """
        page = 1
        while True:
            result = await self.list_status_definitions(
                status_id_from=status_id_from,
                status_id_to=status_id_to,
                language=language,
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

    async def list_all_status_definitions(self) -> list[dict[str, Any]]:
        """List every order status definition, unpaginated.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as a generic ``Collection`` (empty schema) rather than a
            typed list. Based on the endpoint's name and its sibling
            :meth:`list_status_definitions`, this is inferred to return a
            bare array of status definition dicts. Verify against a live
            system before relying on it.

        Returns:
            A list of status definition dicts (see
            :meth:`list_status_definitions` for the field reference).
        """
        return await self._session.get("/rest/orders/statuses/all")  # type: ignore[return-value]

    async def create_status_definition(
        self, status_id: float, names: list[OrderStatusNamePayload]
    ) -> dict[str, Any]:
        """Create a new order status definition.

        Args:
            status_id: The ID to assign to the new status.
            names: List of translated name dicts. Use
                :class:`~plentymarkets._types.OrderStatusNamePayload` for IDE
                autocomplete.

        Returns:
            The created status definition dict (see
            :meth:`list_status_definitions` for the field reference).
        """
        return await self._session.post(
            "/rest/orders/statuses",
            json={"statusId": status_id, "names": names},
        )

    async def get_status_definition(self, status_id: float) -> dict[str, Any]:
        """Get a single order status definition by ID.

        Args:
            status_id: The order status ID.

        Returns:
            A status definition dict (see :meth:`list_status_definitions`
            for the field reference).
        """
        return await self._session.get(f"/rest/orders/statuses/{status_id}")

    async def rename_status_definition(
        self, status_id: float, names: list[OrderStatusNamePayload]
    ) -> dict[str, Any]:
        """Update the translated names of an order status definition.

        Args:
            status_id: The order status ID.
            names: List of translated name dicts. Use
                :class:`~plentymarkets._types.OrderStatusNamePayload` for IDE
                autocomplete.

        Returns:
            The updated status definition dict (see
            :meth:`list_status_definitions` for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/statuses/{status_id}", json={"names": names}
        )

    async def delete_status_definition(self, status_id: float) -> dict[str, Any]:
        """Delete an order status definition.

        Args:
            status_id: The order status ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(f"/rest/orders/statuses/{status_id}")

    async def update_status_definition_properties(
        self, status_ids: list[float], new_values: list[str]
    ) -> dict[str, Any]:
        """Bulk-update properties (color/visibility flags) across several
        order status definitions at once.

        Args:
            status_ids: Status IDs to apply the new values to.
            new_values: List of ``"key:value"`` strings, one per property to
                change. The status color must be a hex code (e.g.
                ``"color:#ff0000"``); all other properties
                (``isFrontendVisible``, ``isReorderVisible``,
                ``isRedistributionVisible``) take ``0`` (inactive) or ``1``
                (active), e.g. ``"isFrontendVisible:1"``.

        Returns:
            The API response dict on success, or ``{}`` if the response has
            no body.
        """
        params = {
            "newStatusValues": ",".join(new_values),
            "selectedStatusList": ",".join(str(s) for s in status_ids),
        }
        return await self._session.post(
            "/rest/orders/statuses/group_functions", params=params
        )

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
