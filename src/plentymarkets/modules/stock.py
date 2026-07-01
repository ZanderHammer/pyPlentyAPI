from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import (
        StockCorrectionPayload,
        StockDischargePayload,
        StockIntakePayload,
        StockRedistributionPayload,
        UnpackVariationPayload,
        WarehouseCreatePayload,
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

    # -- Warehouses ----------------------------------------------------------

    async def list_warehouses(self, with_: list[str] | None = None) -> dict[str, Any]:
        """List all warehouses.

        Args:
            with_: Optional list of related data to embed, e.g.
                ``["stockMovementSettings"]``.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Warehouse dicts, each with:

                - ``id`` (int): Warehouse ID.
                - ``name`` (str): Warehouse name.
                - ``note`` (str): Free-text note.
                - ``typeId`` (int): Warehouse type (0=sales, 1=repair,
                  4=storage, 5=transit, 6=distribution, 7=other).
                - ``priority`` (int): Allocation priority; higher wins.
                - ``allocationReferrerIds`` (list): Referrer IDs used for
                  automatic warehouse detection.
                - ``onStockAvailability`` (int): Availability ID shown when
                  stock is available.
                - ``outOfStockAvailability`` (int): Availability ID shown
                  when no stock is available.
                - ``splitByShippingProfile`` (bool): Whether orders are
                  split by shipping profile.
                - ``storageLocationType`` (str): Storage location size class.
                - ``storageLocationZone`` (int): Storage location zone ID.
                - ``repairWarehouseId`` (int): Associated repair warehouse ID.
                - ``isInventoryModeActive`` (bool): Whether stocktaking mode
                  is active.
                - ``logisticsType`` (str): Fulfilment provider (``"own"``,
                  ``"amazon"``, ``"dhlFulfillment"``).
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        params = self._build_params(with_=with_)
        return await self._session.get(
            "/rest/stockmanagement/warehouses", params=params or None
        )

    async def create_warehouse(self, data: WarehouseCreatePayload) -> dict[str, Any]:
        """Create a new warehouse.

        Args:
            data: Warehouse payload. Use
                :class:`~plentymarkets._types.WarehouseCreatePayload` for IDE
                autocomplete. ``name``, ``typeId``, and ``logisticsType`` are
                required.

        Returns:
            The created warehouse dict (see :meth:`list_warehouses` for the
            field reference).
        """
        return await self._session.post("/rest/stockmanagement/warehouses", json=data)

    async def get_warehouse(
        self, warehouse_id: int, with_: list[str] | None = None
    ) -> dict[str, Any]:
        """Get a single warehouse by ID.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            with_: Optional list of related data to embed.

        Returns:
            The warehouse dict (see :meth:`list_warehouses` for the field
            reference).
        """
        params = self._build_params(with_=with_)
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}", params=params or None
        )

    async def get_storage_location(
        self,
        warehouse_id: int,
        storage_location_id: int,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a single storage location within a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            storage_location_id: The storage location ID.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``id`` (int): Storage location ID.
            - ``warehouseId`` (int): Warehouse ID it belongs to.
            - ``rackId`` (int): Rack ID it belongs to.
            - ``shelfId`` (int): Shelf ID it belongs to.
            - ``name`` (str): Storage location name.
            - ``type`` (int): Size class (small, medium, large, europallet).
            - ``position`` (int): Position within the shelf/rack.
        """
        params = self._build_params(with_=with_)
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}"
            f"/management/storageLocations/{storage_location_id}",
            params=params or None,
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

    async def book_incoming_items(
        self, warehouse_id: int, data: StockIntakePayload
    ) -> dict[str, Any]:
        """Book incoming stock (e.g. a delivery) into a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            data: Intake payload. Use
                :class:`~plentymarkets._types.StockIntakePayload` for IDE
                autocomplete. ``deliveredAt``, ``quantity``, and ``reasonId``
                are required; see the TypedDict for the full set of optional
                keys, or pass ``incomingItems`` for a bulk request across
                several variations.

        Returns:
            The API response dict on success, or ``{}`` if the response has
            no body.
        """
        return await self._session.put(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/bookIncomingItems",
            json=data,
        )

    async def book_outgoing_items(
        self, warehouse_id: int, data: StockDischargePayload
    ) -> dict[str, Any]:
        """Book outgoing stock (e.g. a write-off) out of a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            data: Discharge payload. Use
                :class:`~plentymarkets._types.StockDischargePayload` for IDE
                autocomplete. ``deliveredAt``, ``quantity``, and ``reasonId``
                are required; see the TypedDict for the full set of optional
                keys, or pass ``outgoingItems`` for a bulk request across
                several variations.

        Returns:
            The API response dict on success, or ``{}`` if the response has
            no body.
        """
        return await self._session.put(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/bookOutgoingItems",
            json=data,
        )

    async def unpack_variation(
        self, warehouse_id: int, data: UnpackVariationPayload
    ) -> dict[str, Any]:
        """Unpack a bundle/set variation into its component variations.

        Note:
            PlentyMarkets' published OpenAPI spec does not document a clean
            request schema for this endpoint (see
            :class:`~plentymarkets._types.UnpackVariationPayload`). Verify
            the payload shape against a live system before relying on it.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            data: Unpack payload. Use
                :class:`~plentymarkets._types.UnpackVariationPayload` for IDE
                autocomplete.

        Returns:
            The updated warehouse dict on success, or ``{}`` if the response
            has no body.
        """
        return await self._session.put(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/unpackVariation",
            json=data,
        )

    async def book_stocktaking(
        self,
        warehouse_id: int,
        warehouse_location_id: int,
        data: StockCorrectionPayload,
    ) -> dict[str, Any]:
        """Book a stocktaking correction for a storage location.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            warehouse_location_id: The storage location ID being counted.
            data: Correction payload. Use
                :class:`~plentymarkets._types.StockCorrectionPayload` for IDE
                autocomplete — this endpoint uses the same request schema as
                :meth:`correct`. Only ``quantity`` is required.

        Returns:
            The API response dict on success, or ``{}`` if the response has
            no body.
        """
        return await self._session.put(
            f"/rest/stockmanagement/warehouses/{warehouse_id}"
            f"/{warehouse_location_id}/stock/bookStocktaking",
            json=data,
        )

    async def list_stock_movements(
        self,
        warehouse_id: int,
        filters: dict[str, Any] | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """List stock movement history for a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            filters: Optional dict of filter query parameters, e.g.
                ``{"variationId": 5, "reasonGroup": 1, "itemId": 42,
                "createdAtFrom": "2026-01-01T00:00:00+00:00",
                "createdAtTo": "2026-01-31T23:59:59+00:00", "year": 2026,
                "processRowType": 1, "orderId": 123}``.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching movements.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Stock movement dicts, each with:

                - ``id`` (int): Stock movement ID.
                - ``itemId`` (int): Item ID.
                - ``variationId`` (int): Variation ID.
                - ``warehouseId`` (int): Warehouse ID.
                - ``warehouseName`` (str): Warehouse name.
                - ``reason`` (int): Numeric reason code for the movement.
                - ``reasonString`` (str): Human-readable reason.
                - ``attributeValues`` (str): Attribute values of the
                  variation.
                - ``processRowId`` (int): ID of the order or incoming-item
                  data set that triggered the movement.
                - ``processRowType`` (int): Type of the triggering record
                  (1=incoming item data set, 2=order, etc.).
                - ``quantity`` (int): Quantity moved.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``bestBeforeDate`` (str): Best-before date, if applicable.
                - ``batch`` (str): Batch identifier, if applicable.
                - ``storageLocationName`` (str): Storage location name.
                - ``purchasePrice`` (int): Purchase price of the variation.
                - ``userId`` (int): ID of the user who triggered the
                  movement, or ``None`` if system-triggered.
        """
        params = self._build_params(filters, page=page, itemsPerPage=items_per_page)
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/movements",
            params=params,
        )

    async def paginate_stock_movements(
        self,
        warehouse_id: int,
        filters: dict[str, Any] | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every stock movement for a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock_movements`).
            items_per_page: Results per page request (max 250).

        Yields:
            Individual stock movement dicts (see :meth:`list_stock_movements`).
        """
        page = 1
        while True:
            result = await self.list_stock_movements(
                warehouse_id, filters, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def list_stock_by_storage_location(
        self,
        warehouse_id: int,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """List stock levels per storage location within a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            filters: Optional dict of filter query parameters, e.g.
                ``{"updatedAtFrom": "2026-01-01T00:00:00+00:00",
                "updatedAtTo": "2026-01-31T23:59:59+00:00", "variationId": 5,
                "storageLocationId": 7}``.
            with_: Optional list of related data to embed.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching entries.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Storage location stock dicts, each
              with:

                - ``itemId`` (int): Item ID.
                - ``variationId`` (int): Variation ID.
                - ``storageLocationId`` (int): Storage location ID.
                - ``warehouseId`` (int): Warehouse ID.
                - ``quantity`` (float): Quantity stored at this location.
                - ``bestBeforeDate`` (str): Best-before date, if applicable.
                - ``batch`` (str): Batch identifier, if applicable.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        params = self._build_params(
            filters, with_=with_, page=page, itemsPerPage=items_per_page
        )
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/storageLocations",
            params=params,
        )

    async def list_stock_by_storage_location_pim(
        self,
        warehouse_id: int,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """List stock levels per storage location within a warehouse, with
        the linked PIM entry embedded.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock_by_storage_location`).
            with_: Optional list of related data to embed.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the same shape as
            :meth:`list_stock_by_storage_location`.
        """
        params = self._build_params(
            filters, with_=with_, page=page, itemsPerPage=items_per_page
        )
        return await self._session.get(
            f"/rest/stockmanagement/warehouses/{warehouse_id}/stock/storageLocationsPim",
            params=params,
        )

    async def paginate_stock_by_storage_location(
        self,
        warehouse_id: int,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every storage-location stock entry
        for a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock_by_storage_location`).
            with_: Optional list of related data to embed.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual storage location stock dicts (see
            :meth:`list_stock_by_storage_location`).
        """
        page = 1
        while True:
            result = await self.list_stock_by_storage_location(
                warehouse_id, filters, with_=with_, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def paginate_stock_by_storage_location_pim(
        self,
        warehouse_id: int,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every storage-location stock entry
        (with the linked PIM entry embedded) for a warehouse.

        Args:
            warehouse_id: The PlentyMarkets warehouse ID.
            filters: Optional dict of filter query parameters (see
                :meth:`list_stock_by_storage_location`).
            with_: Optional list of related data to embed.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual storage location stock dicts (see
            :meth:`list_stock_by_storage_location`).
        """
        page = 1
        while True:
            result = await self.list_stock_by_storage_location_pim(
                warehouse_id, filters, with_=with_, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
