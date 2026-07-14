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
