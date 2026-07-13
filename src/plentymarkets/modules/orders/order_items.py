from __future__ import annotations

from typing import Any, AsyncIterator

from ._base import OrdersBase


class ItemsMixin(OrdersBase):
    """Order items, serial numbers, and package numbers."""

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
