from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import (
        OrderCreatePayload,
        OrderItemTransactionCreatePayload,
        OrderStatusNamePayload,
        OrderTransactionsCreatePayload,
    )

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

    async def list_status_history(
        self,
        order_id: int | None = None,
        status_id: float | None = None,
        created_at_from: str | None = None,
        created_at_to: str | None = None,
        user_id: int | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """Search status history entries across all orders.

        Args:
            order_id: Filter to a single order's history.
            status_id: Filter to history entries for a specific status.
            created_at_from: ISO 8601 lower bound for the entry creation date.
            created_at_to: ISO 8601 upper bound for the entry creation date.
            user_id: Filter to history entries created by a specific user.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching entries.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Status history dicts, each with:

                - ``id`` (int): The status history entry ID.
                - ``orderId`` (int): The order ID.
                - ``statusId`` (float): The status ID.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``userId`` (int): ID of the user who triggered the entry.
                - ``procedureText`` (str): Informational text describing the
                  procedure that created the entry.
        """
        params = self._build_params(
            None,
            orderId=order_id,
            statusId=status_id,
            createdAtFrom=created_at_from,
            createdAtTo=created_at_to,
            userId=user_id,
            page=page,
            itemsPerPage=items_per_page,
        )
        return await self._session.get("/rest/orders/status-history", params=params)

    async def paginate_status_history(
        self,
        order_id: int | None = None,
        status_id: float | None = None,
        created_at_from: str | None = None,
        created_at_to: str | None = None,
        user_id: int | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every matching status history entry across all pages.

        Args:
            order_id: Filter to a single order's history.
            status_id: Filter to history entries for a specific status.
            created_at_from: ISO 8601 lower bound for the entry creation date.
            created_at_to: ISO 8601 upper bound for the entry creation date.
            user_id: Filter to history entries created by a specific user.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual status history dicts (see :meth:`list_status_history`).
        """
        page = 1
        while True:
            result = await self.list_status_history(
                order_id=order_id,
                status_id=status_id,
                created_at_from=created_at_from,
                created_at_to=created_at_to,
                user_id=user_id,
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

    async def get_order_status_history(self, order_id: int) -> list[dict[str, Any]]:
        """Get the full status history of a single order.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A list of status history dicts (see :meth:`list_status_history`
            for the field reference).
        """
        return await self._session.get(f"/rest/orders/{order_id}/status-history")  # type: ignore[return-value]

    async def list_date_types(self) -> list[dict[str, Any]]:
        """List all order date types.

        Returns:
            A list of date type dicts, each with:

            - ``id`` (int): The date type ID. Common values: 1=Deleted on,
              2=Created on, 3=Paid date, 4=Last update, 5=Completed on,
              6=Return date, 7=Payment due date, 8=Estimated shipping date,
              9=Start date, 10=End date, 11=Possible delivery date,
              12=Market transfer date, 13=Subscription cancelled on,
              14=Subscription last run, 15=Subscription next run,
              19=Confirmation link valid until.
            - ``isErasable`` (bool): Whether this type can be deleted.
            - ``position`` (int): Display sort position.
        """
        return await self._session.get("/rest/orders/dates/types")  # type: ignore[return-value]

    async def get_date_type(self, type_id: int) -> dict[str, Any]:
        """Get a single order date type by ID.

        Args:
            type_id: The order date type ID.

        Returns:
            A date type dict (see :meth:`list_date_types` for the field
            reference).
        """
        return await self._session.get(f"/rest/orders/dates/types/{type_id}")

    async def list_date_type_names(self, type_id: int) -> list[dict[str, Any]]:
        """List the translated names of an order date type.

        Args:
            type_id: The order date type ID.

        Returns:
            A list of date type name dicts, each with:

            - ``id`` (int): The name record ID.
            - ``typeId`` (int): The date type ID this name belongs to.
            - ``lang`` (str): Two-letter ISO 639-1 language code.
            - ``name`` (str): The translated display name.
        """
        return await self._session.get(f"/rest/orders/dates/types/{type_id}/names")  # type: ignore[return-value]

    async def get_date_type_name(self, type_id: int, lang: str) -> dict[str, Any]:
        """Get a single translated name of an order date type.

        Args:
            type_id: The order date type ID.
            lang: Two-letter ISO 639-1 language code, e.g. ``"en"``.

        Returns:
            A date type name dict (see :meth:`list_date_type_names` for the
            field reference).
        """
        return await self._session.get(
            f"/rest/orders/dates/types/{type_id}/names/{lang}"
        )

    async def list_order_dates(self, order_id: int) -> list[dict[str, Any]]:
        """List all dates recorded on an order.

        Note:
            PlentyMarkets' published schema for this object (``OrderDate``)
            does not document a date *value* field, only ``id``, ``orderId``,
            ``typeId``, ``createdAt``, and ``updatedAt`` — surprising for an
            endpoint whose purpose is listing an order's date values. Verify
            against a live system; the value may be present in the response
            under a key not covered by the published spec.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A list of order date dicts, each with:

            - ``id`` (int): The order date record ID.
            - ``orderId`` (int): The order ID this date belongs to.
            - ``typeId`` (int): The date type ID (see :meth:`list_date_types`).
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.get(f"/rest/orders/{order_id}/dates")  # type: ignore[return-value]

    async def get_order_date(self, order_id: int, type_id: int) -> dict[str, Any]:
        """Get a single date recorded on an order by date type.

        Note:
            See the caveat on :meth:`list_order_dates` regarding the
            published schema's missing date-value field.

        Args:
            order_id: The PlentyMarkets order ID.
            type_id: The order date type ID (see :meth:`list_date_types`).

        Returns:
            An order date dict (see :meth:`list_order_dates` for the field
            reference).
        """
        return await self._session.get(f"/rest/orders/{order_id}/dates/{type_id}")

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

    # -- Order item transactions ----------------------------------------------
    #
    # These methods manage transactions (stock movements) recorded against
    # order items, via the flat `/rest/orders/items/transactions/*` family
    # (addressed by transaction ID) and the `/rest/orders/items/{orderItemId}
    # /transactions` family (scoped to one order item). Both are current
    # (not deprecated), unlike the sibling order-item dates/properties
    # families, which PlentyMarkets has deprecated in favor of
    # `PUT /rest/orders/{orderId}` and are intentionally not implemented here.

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

    # -- Order items, serial numbers & package numbers -------------------------

    async def list_order_items(
        self,
        order_id: int,
        with_: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """List an order's items with pagination.

        Note:
            PlentyMarkets documents ``sortBy``'s allowed values as
            ``"itemVariationId"``, ``"orderItemName"``, ``"createdAt"``,
            ``"updatedAt"``, or ``"id"``, but documents its default as
            ``"orderItemId"`` — a value that isn't in that same enum. Likely
            a spec documentation inconsistency; verify against a live system.

        Args:
            order_id: The PlentyMarkets order ID.
            with_: Related data to embed. Available: ``"variation"``,
                ``"giftCardCodes"``, ``"transactions"``, ``"serialNumbers"``,
                ``"variationBarcodes"``.
            sort_by: Sort field (see Note above).
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching order items.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Order item dicts, each with:

                - ``id`` (int): The order item ID.
                - ``orderId`` (int): The order this item belongs to.
                - ``typeId`` (int): The order item type.
                - ``referrerId`` (float): Sales referrer ID.
                - ``itemVariationId`` (int): The variation ID.
                - ``quantity`` (float): The ordered quantity.
                - ``orderItemName`` (str): The item's display name.
                - ``attributeValues`` (str): Selected attribute values.
                - ``shippingProfileId`` (int): Shipping profile ID.
                - ``countryVatId`` (int): Country VAT ID.
                - ``vatField`` (int): VAT field reference.
                - ``vatRate`` (float): The applied VAT rate.
                - ``position`` (int): Position of the item within the order.
                - ``warehouseId`` (int): Warehouse ID.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        params = self._build_params(
            None,
            with_=with_,
            sortBy=sort_by,
            sortOrder=sort_order,
            page=page,
            itemsPerPage=items_per_page,
        )
        return await self._session.get(f"/rest/orders/{order_id}/items", params=params)

    async def paginate_order_items(
        self,
        order_id: int,
        with_: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every item of an order across all pages.

        Args:
            order_id: The PlentyMarkets order ID.
            with_: Related data to embed (see :meth:`list_order_items`).
            sort_by: Sort field (see :meth:`list_order_items`).
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual order item dicts (see :meth:`list_order_items` for
            the field reference).
        """
        page = 1
        while True:
            result = await self.list_order_items(
                order_id,
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

    async def delete_order_item(
        self, order_id: int, order_item_id: int
    ) -> dict[str, Any]:
        """Delete an order item.

        Args:
            order_id: The PlentyMarkets order ID.
            order_item_id: The order item ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/orders/{order_id}/items/{order_item_id}"
        )

    async def list_order_serial_numbers(self, order_id: int) -> list[dict[str, Any]]:
        """List serial numbers bound to any item of an order.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A list of serial number dicts, each with:

            - ``serialNumberId`` (int): The serial number record ID.
            - ``orderId`` (int): The order this serial number belongs to.
            - ``orderItemId`` (int): The order item it's bound to.
            - ``serialNumber`` (str): The serial number value.
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/items/serialNumbers"
        )

    async def list_order_item_serial_numbers(
        self, order_id: int, order_item_id: int
    ) -> list[dict[str, Any]]:
        """List serial numbers bound to a single order item.

        Args:
            order_id: The PlentyMarkets order ID.
            order_item_id: The order item ID.

        Returns:
            A list of serial number dicts (see
            :meth:`list_order_serial_numbers` for the field reference).
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/items/{order_item_id}/serialNumbers"
        )

    async def create_order_item_serial_number(
        self, order_id: int, order_item_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a serial number and bind it to an order item.

        Note:
            **Schema gap.** PlentyMarkets' published OpenAPI spec declares no
            request body schema at all for this endpoint. ``data`` is passed
            through as-is; the likely shape is ``{"serialNumber": "..."}``,
            possibly with additional fields, but this is unverified. Tracked
            in ROADMAP.md's "Known Schema Gaps" section — verify against a
            live system and tighten to a proper TypedDict once confirmed.

        Args:
            order_id: The PlentyMarkets order ID.
            order_item_id: The order item ID.
            data: Serial number payload; shape unverified (see Note above).

        Returns:
            The created serial number dict (see
            :meth:`list_order_serial_numbers` for the field reference).
        """
        return await self._session.post(
            f"/rest/orders/{order_id}/items/{order_item_id}/serialNumbers",
            json=data,
        )

    async def list_order_package_numbers(self, order_id: int) -> list[str]:
        """List an order's package numbers.

        Note:
            PlentyMarkets' published OpenAPI spec resolves this endpoint's
            array item schema to a generic untyped placeholder rather than
            ``type: string``; ``list[str]`` is inferred from the endpoint's
            description ("List package numbers of an order"). Verify against
            a live system before relying on it.

        Args:
            order_id: The PlentyMarkets order ID.

        Returns:
            A list of package number strings.
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/packagenumbers"
        )

    # -- Warehouse locations & item-level reorders ------------------------------

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

    # -- Order-level reorders & bulk transactions -------------------------------

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
            :meth:`get`); the most useful fields are:

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
            new transaction (see :meth:`search_item_transactions` for the
            field reference).
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/transactions", json=data
        )
