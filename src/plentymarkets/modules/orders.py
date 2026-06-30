from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import OrderCreatePayload

from .._session import _Session


class OrdersModule:
    """Wraps the PlentyMarkets ``/rest/orders`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

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
