from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        VariationAdditionalSkuPayload,
        VariationSkuPayload,
        VariationBarcodePayload,
        VariationMarketIdentNumberPayload,
        VariationBundleComponentPayload,
    )

from ._base import PimBase


class VariationIdentifiersMixin(PimBase):
    """Bulk update/delete of a variation's identifying codes and composition (SKUs, barcodes, market identification numbers, bundle components)."""

    async def update_variation_additional_skus(
        self,
        data: list[VariationAdditionalSkuPayload],
    ) -> dict[str, Any]:
        """Bulk create or update variation additional SKUs.

        Args:
            data: List of additional-SKU payloads. Use
                :class:`~plentymarkets._types.VariationAdditionalSkuPayload`
                for IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; based on the
            bulk-endpoint pattern used elsewhere in the API, expect
            ``updated`` (int) and ``invalid`` (list[dict], each with ``id``
            and ``reason``). Verify against a live system before relying on
            these keys.
        """
        return await self._session.put(
            "/rest/pim/variations/additional_skus", json=data
        )

    async def delete_variation_additional_skus(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation additional SKUs by ID.

        Args:
            ids: List of additional-SKU record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete(
            "/rest/pim/variations/additional_skus", json=ids
        )

    async def update_variation_skus(
        self,
        data: list[VariationSkuPayload],
    ) -> dict[str, Any]:
        """Bulk create or update marketplace SKUs on variations.

        Args:
            data: List of SKU payloads. Use
                :class:`~plentymarkets._types.VariationSkuPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/skus", json=data)

    async def delete_variation_skus(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation marketplace SKUs by ID.

        Args:
            ids: List of variation-SKU record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/skus", json=ids)

    async def update_variation_barcodes(
        self,
        data: list[VariationBarcodePayload],
    ) -> dict[str, Any]:
        """Bulk create or update variation barcode links.

        Args:
            data: List of barcode link payloads. Use
                :class:`~plentymarkets._types.VariationBarcodePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/barcodes", json=data)

    async def delete_variation_barcodes(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation barcode links by ID.

        Args:
            ids: List of variation-barcode link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/barcodes", json=ids)

    async def update_variation_market_ident_numbers(
        self,
        data: list[VariationMarketIdentNumberPayload],
    ) -> dict[str, Any]:
        """Bulk create or update market identifier numbers (MINs) on variations.

        Args:
            data: List of MIN payloads. Use
                :class:`~plentymarkets._types.VariationMarketIdentNumberPayload`
                for IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put(
            "/rest/pim/variations/market_ident_numbers", json=data
        )

    async def delete_variation_market_ident_numbers(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation market identifier numbers by ID.

        Args:
            ids: List of MIN record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete(
            "/rest/pim/variations/market_ident_numbers", json=ids
        )

    async def update_variation_bundle_components(
        self,
        data: list[VariationBundleComponentPayload],
    ) -> dict[str, Any]:
        """Bulk create or update bundle components on a variation.

        Args:
            data: List of bundle component payloads. Use
                :class:`~plentymarkets._types.VariationBundleComponentPayload`
                for IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put(
            "/rest/pim/variations/bundle_components", json=data
        )

    async def delete_variation_bundle_components(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete bundle components by ID.

        Args:
            ids: List of bundle component record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete(
            "/rest/pim/variations/bundle_components", json=ids
        )
