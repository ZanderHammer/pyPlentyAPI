from __future__ import annotations

from typing import Any, AsyncIterator

from ._base import OrdersBase


class StatusHistoryMixin(OrdersBase):
    """Order status history search/lookup."""

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
