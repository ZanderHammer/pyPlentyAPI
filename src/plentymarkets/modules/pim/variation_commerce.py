from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        VariationClientPayload,
        VariationMarketPayload,
        VariationSalesPricePayload,
        VariationSupplierPayload,
        VariationWarehousePayload,
        VariationImagePayload,
    )

from ._base import PimBase


class VariationCommerceMixin(PimBase):
    """Bulk update/delete of a variation's business assignments and media (clients, markets, sales prices, supplier, warehouses, images)."""

    async def update_variation_clients(
        self,
        data: list[VariationClientPayload],
    ) -> dict[str, Any]:
        """Bulk create client (store) visibility links on variations.

        Args:
            data: List of client visibility payloads. Use
                :class:`~plentymarkets._types.VariationClientPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/clients", json=data)

    async def delete_variation_clients(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation client visibility links by ID.

        Args:
            ids: List of variation-client link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/clients", json=ids)

    async def update_variation_markets(
        self,
        data: list[VariationMarketPayload],
    ) -> dict[str, Any]:
        """Bulk create market availability links on variations.

        Args:
            data: List of market availability payloads. Use
                :class:`~plentymarkets._types.VariationMarketPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/markets", json=data)

    async def delete_variation_markets(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation market availability links by ID.

        Args:
            ids: List of variation-market link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/markets", json=ids)

    async def update_variation_sales_prices(
        self,
        data: list[VariationSalesPricePayload],
    ) -> dict[str, Any]:
        """Bulk create or update sales price values on variations.

        Args:
            data: List of variation sales price payloads. Use
                :class:`~plentymarkets._types.VariationSalesPricePayload` for
                IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/sales_prices", json=data)

    async def delete_variation_sales_prices(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation sales price links by ID.

        Args:
            ids: List of variation-sales-price link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/sales_prices", json=ids)

    async def update_variation_supplier(
        self,
        data: list[VariationSupplierPayload],
    ) -> dict[str, Any]:
        """Bulk create or update supplier links on variations.

        Args:
            data: List of supplier link payloads. Use
                :class:`~plentymarkets._types.VariationSupplierPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/supplier", json=data)

    async def delete_variation_supplier(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation supplier links by ID.

        Args:
            ids: List of variation-supplier link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/supplier", json=ids)

    async def update_variation_warehouses(
        self,
        data: list[VariationWarehousePayload],
    ) -> dict[str, Any]:
        """Bulk create or update warehouse stock links on variations.

        Args:
            data: List of warehouse link payloads. Use
                :class:`~plentymarkets._types.VariationWarehousePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/warehouses", json=data)

    async def delete_variation_warehouses(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation warehouse stock links by ID.

        Args:
            ids: List of variation-warehouse link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/warehouses", json=ids)

    async def update_variation_images(
        self,
        data: list[VariationImagePayload],
    ) -> dict[str, Any]:
        """Bulk create image links on variations.

        Args:
            data: List of image link payloads. Use
                :class:`~plentymarkets._types.VariationImagePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/images", json=data)

    async def delete_variation_images(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation image links by ID.

        Args:
            ids: List of variation-image link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/images", json=ids)
