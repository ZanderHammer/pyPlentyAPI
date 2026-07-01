from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import (
        StockCorrectionPayload,
        StockRedistributionPayload,
    )

from .._session import _Session


class StockModule:
    """Wraps the PlentyMarkets ``/rest/stockmanagement`` endpoints: stock
    levels, warehouses, storage locations, and stock movements/bookings.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<StockModule /rest/stockmanagement>"

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

    # -- Stock (global) ----------------------------------------------------

    async def list_stock(
        self,
        filters: dict[str, Any] | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """List stock levels across all warehouses.

        Args:
            filters: Optional dict of filter query parameters, e.g.
                ``{"updatedAtFrom": "2026-01-01T00:00:00+00:00",
                "updatedAtTo": "2026-01-31T23:59:59+00:00", "variationId": 5,
                "columns": "variationId,warehouseId,stockNet"}``.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching stock entries.
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
        params = self._build_params(filters, page=page, itemsPerPage=items_per_page)
        return await self._session.get("/rest/stockmanagement/stock", params=params)

    async def paginate_all_stock(
        self,
        filters: dict[str, Any] | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every stock entry across all warehouses.

        Args:
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock`).
            items_per_page: Results per page request (max 250).

        Yields:
            Individual stock entry dicts (see :meth:`list_stock`).
        """
        page = 1
        while True:
            result = await self.list_stock(filters, page=page, items_per_page=items_per_page)
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def list_stock_archive_years(self) -> list[Any]:
        """List the archive years available for stock movement history.

        Returns:
            A list of years (int or str, depending on the shop's data) for
            which archived stock movements exist.
        """
        return await self._session.get("/rest/stockmanagement/stock/archives")  # type: ignore[return-value]

    async def list_stock_by_type(
        self,
        type_: str,
        filters: dict[str, Any] | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """List stock levels for a warehouse type.

        Args:
            type_: Warehouse type name. Only ``"sales"`` is currently
                supported by the API.
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock`).
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the same shape as :meth:`list_stock`.
        """
        params = self._build_params(filters, page=page, itemsPerPage=items_per_page)
        return await self._session.get(
            f"/rest/stockmanagement/stock/types/{type_}", params=params
        )

    async def paginate_stock_by_type(
        self,
        type_: str,
        filters: dict[str, Any] | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every stock entry for a warehouse type.

        Args:
            type_: Warehouse type name. Only ``"sales"`` is currently
                supported by the API.
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock`).
            items_per_page: Results per page request (max 250).

        Yields:
            Individual stock entry dicts (see :meth:`list_stock`).
        """
        page = 1
        while True:
            result = await self.list_stock_by_type(
                type_, filters, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def redistribute_stock(self, data: StockRedistributionPayload) -> dict[str, Any]:
        """Move stock of a variation from one warehouse to another.

        Args:
            data: Redistribution payload. Use
                :class:`~plentymarkets._types.StockRedistributionPayload` for
                IDE autocomplete. ``currentWarehouseId``, ``newWarehouseId``,
                and ``quantity`` are required; see the TypedDict for the full
                set of optional keys, or pass ``redistributions`` for a bulk
                request across several variations.

        Returns:
            The API response dict on success, or ``{}`` if the response has
            no body.
        """
        return await self._session.put(
            "/rest/stockmanagement/stock/redistribute", json=data
        )

    # -- Per-warehouse stock --------------------------------------------------

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
            A dict with the same shape as :meth:`list_stock`.
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

