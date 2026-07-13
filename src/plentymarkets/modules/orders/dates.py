from __future__ import annotations

from typing import Any

from ._base import OrdersBase


class DatesMixin(OrdersBase):
    """Order date types and per-order date values."""

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
