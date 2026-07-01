from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import StockCorrectionPayload

from .._session import _Session


class StockModule:
    """Wraps the PlentyMarkets ``/rest/stockmanagement/warehouses/{warehouseId}/stock``
    endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<StockModule /rest/stockmanagement>"

    async def get_by_warehouse(
        self,
        warehouse_id: int,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
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

                - ``itemId`` (int): Item ID.
                - ``variationId`` (int): Variation ID.
                - ``warehouseId`` (int): Warehouse ID.
                - ``stockPhysical`` (float): Total physical stock on hand.
                - ``stockNet`` (float): Stock available for sale.
                - ``reservedStock`` (float): Stock reserved by open orders.
                - ``reservedEbay`` (float): Stock reserved for eBay listings.
                - ``reservedBundle`` (float): Stock reserved by bundle
                  components.
                - ``reorderDelta`` (float): Difference to the reorder
                  threshold.
                - ``reordered`` (int): Quantity currently on reorder.
                - ``warehousePriority`` (int): Priority of this warehouse for
                  stock allocation.
                - ``averagePurchasePrice`` (float): Average net purchase price.
                - ``averageSale`` (float): Average sale price.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def correct(self, warehouse_id: int, data: StockCorrectionPayload) -> dict[str, Any]:
        """Correct the stock of a variation in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            data: Correction payload. Use
                :class:`~plentymarkets._types.StockCorrectionPayload` for IDE
                autocomplete. Only ``quantity`` is required; see the
                TypedDict for the full set of optional keys.

        Returns:
            The API response dict on success, or ``{}`` if the response has no body.
        """
        return await self._session.put(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/correction",
            json=data,
        )

    async def paginate_stock(
        self, warehouse_id: int, items_per_page: int = 50
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every stock entry in a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual stock entry dicts, each with the following keys:

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
