from __future__ import annotations

from typing import AsyncIterator

from .._session import _Session


class StockModule:
    """Wraps the PlentyMarkets ``/rest/stock`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get_by_warehouse(
        self,
        warehouse_id: int,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict:
        """Get stock levels for all variations in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of variation stock entries.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Stock entry dicts, each with:

                - ``warehouseId`` (int): Warehouse ID.
                - ``itemId`` (int): Item ID.
                - ``variationId`` (int): Variation ID.
                - ``netStock`` (float): Stock available for sale.
                - ``physicalStock`` (float): Total physical stock on hand.
                - ``reservedStock`` (float): Stock reserved by open orders.
                - ``reorderLevel`` (float): Reorder trigger threshold.
                - ``maximumStock`` (float): Maximum stock threshold.
                - ``averagePurchasePrice`` (float): Average net purchase price.
        """
        return await self._session.get(
            f"/rest/stock/warehouses/{warehouse_id}/items",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def correct(self, warehouse_id: int, data: dict) -> dict:
        """Correct the stock of a variation in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            data: Correction payload dict with the following keys:

                - ``variationId`` (int): Variation ID to correct.
                - ``quantity`` (float): New absolute stock quantity.
                - ``reasonId`` (int): Correction reason ID (e.g. 301=stock
                  correction, 304=incoming items).
                - ``warehouseLocationId`` (int): Storage location ID (0 for
                  the warehouse default).

        Returns:
            The API response dict on success, or ``{}`` if the response has no body.
        """
        return await self._session.put(
            f"/rest/stock/warehouses/{warehouse_id}/stock/correction",
            json=data,
        )

    async def paginate_stock(
        self, warehouse_id: int, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every stock entry in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual stock entry dicts; same keys as ``get_by_warehouse()``
            entries.
        """
        page = 1
        while True:
            result = await self.get_by_warehouse(
                warehouse_id, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
