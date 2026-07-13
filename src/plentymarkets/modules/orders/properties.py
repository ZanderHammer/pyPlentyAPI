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
