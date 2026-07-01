from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import (
        AttributeCreatePayload,
        AttributeNamePayload,
        AttributeUpdatePayload,
        AttributeValuePayload,
        AttributeValueNamePayload,
        BarcodeCreatePayload,
        BarcodeUpdatePayload,
        ItemSerialNumberPayload,
        SalesPriceCreatePayload,
        SalesPriceUpdatePayload,
        VariationAdditionalSkuPayload,
        VariationBaseUpdatePayload,
        VariationBarcodePayload,
        VariationBundleComponentPayload,
        VariationCategoryPayload,
        VariationClientPayload,
        VariationCommentPayload,
        VariationCreatePayload,
        VariationDefaultCategoryPayload,
        VariationImagePayload,
        VariationMarketIdentNumberPayload,
        VariationMarketPayload,
        VariationPropertyPayload,
        VariationSalesPricePayload,
        VariationSkuPayload,
        VariationSupplierPayload,
        VariationTagPayload,
        VariationWarehousePayload,
    )

from .._session import _Session


class PimModule:
    """Wraps the PlentyMarkets ``/rest/pim`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<PimModule /rest/pim>"

    @staticmethod
    def _build_params(
        filters: dict[str, Any] | None,
        with_: list[str] | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if filters:
            params.update(filters)
        if with_:
            params["with"] = ",".join(with_)
        return params

    async def list_variations(
        self,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search and filter variations.

        Args:
            filters: Optional dict of filter/sort query parameters. Any of the
                70+ parameters supported by ``GET /rest/pim/variations`` may be
                passed here (e.g. ``{"isActive": "true", "itemId": 42}``).
            with_: Optional list of related data to include inline. Accepted
                values include ``"base"``, ``"base.item"``, ``"base.texts"``,
                ``"base.images"``, ``"base.stock"``, ``"barcodes"``,
                ``"categories"``, ``"clients"``, ``"salesPrices"``,
                ``"warehouses"``, ``"tags"``, ``"properties"``, ``"images"``,
                ``"attributeValues"``, ``"skus"``, ``"markets"``,
                ``"defaultCategories"``, ``"supplier"``, ``"unit"``,
                ``"timestamps"``, ``"bundleComponents"``, ``"comments"``.
                Dotted sub-includes (e.g. ``"base.item"``) pull nested records.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched variation records. Each dict
              contains the fields requested via ``with_`` plus variation ID.
            - ``totalsCount`` (int): Total number of matching variations.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        params = self._build_params(filters, with_)
        return await self._session.get("/rest/pim/variations", params=params or None)

    async def paginate_variations(
        self,
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every variation via cursor-based scroll.

        Uses ``GET /rest/pim/variations/scroll``. Prefer this over
        :meth:`list_variations` when iterating the full catalogue; the scroll
        API is optimised for large result sets and does not require page-count
        arithmetic.

        Args:
            filters: Optional dict of filter query parameters (same set as
                :meth:`list_variations`, excluding pagination params).
            with_: Optional list of related data to include inline (same values
                as :meth:`list_variations`).

        Yields:
            Individual variation dicts. Each dict contains at minimum ``id``;
            additional keys depend on the ``with_`` includes requested.
        """
        params = self._build_params(filters, with_)
        cursor: str | None = None

        while True:
            call_params = dict(params)
            if cursor:
                call_params["cursor"] = cursor
            result = await self._session.get(
                "/rest/pim/variations/scroll",
                params=call_params or None,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            cursor = result.get("cursor") or None
            if not cursor:
                break

    async def update_variation_bases(
        self,
        data: list[VariationBaseUpdatePayload],
    ) -> dict[str, Any]:
        """Bulk create or update variation base data.

        Args:
            data: List of variation update payloads. Each entry must contain
                ``id`` (the variation ID to update). Use
                :class:`~plentymarkets._types.VariationBaseUpdatePayload` for
                IDE autocomplete. Only provided keys are changed.

        Returns:
            A dict with the following keys (based on the standard bulk-endpoint
            pattern — verify against a live system before relying on these):

            - ``updated`` (int): Number of variations successfully updated.
            - ``invalid`` (list[dict]): Entries that failed validation, each
              with ``id`` and ``reason``.
        """
        return await self._session.put("/rest/pim/variations/bases", json=data)

    async def create_variations(
        self,
        data: list[VariationCreatePayload],
    ) -> dict[str, Any]:
        """Bulk create or fully update variations and their related data.

        Args:
            data: List of variation payloads. Use
                :class:`~plentymarkets._types.VariationCreatePayload` for IDE
                autocomplete. Omit ``id`` to create a new variation; include it
                to update an existing one.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; based on the
            bulk-endpoint pattern used elsewhere in the API, expect:

            - ``created`` (int): Number of variations successfully created or
              updated.
            - ``invalid`` (list[dict]): Entries that failed validation, each
              with ``id`` and ``reason``.

            Verify against a live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations", json=data)

    async def delete_variations(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variations by ID.

        Args:
            ids: List of variation IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int): number of variations removed. Verify against a
            live system before relying on this key.
        """
        return await self._session.delete("/rest/pim/variations", json=ids)

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

    async def update_variation_categories(
        self,
        data: list[VariationCategoryPayload],
    ) -> dict[str, Any]:
        """Bulk create or update category links on variations.

        Args:
            data: List of category link payloads. Use
                :class:`~plentymarkets._types.VariationCategoryPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/categories", json=data)

    async def delete_variation_categories(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation category links by ID.

        Args:
            ids: List of variation-category link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/categories", json=ids)

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

    async def update_variation_comments(
        self,
        data: list[VariationCommentPayload],
    ) -> dict[str, Any]:
        """Bulk create or update variation comments.

        Args:
            data: List of comment payloads. Use
                :class:`~plentymarkets._types.VariationCommentPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/comments", json=data)

    async def delete_variation_comments(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation comments by ID.

        Args:
            ids: List of comment record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/comments", json=ids)

    async def update_variation_default_categories(
        self,
        data: list[VariationDefaultCategoryPayload],
    ) -> dict[str, Any]:
        """Bulk create or update the default category per client on variations.

        Args:
            data: List of default-category payloads. Use
                :class:`~plentymarkets._types.VariationDefaultCategoryPayload`
                for IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put(
            "/rest/pim/variations/default_categories", json=data
        )

    async def delete_variation_default_categories(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation default-category links by ID.

        Args:
            ids: List of default-category record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete(
            "/rest/pim/variations/default_categories", json=ids
        )

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

    async def update_variation_properties(
        self,
        data: list[VariationPropertyPayload],
    ) -> dict[str, Any]:
        """Bulk create or update item properties on variations.

        Args:
            data: List of property payloads. Use
                :class:`~plentymarkets._types.VariationPropertyPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/properties", json=data)

    async def delete_variation_properties(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation properties by ID.

        Args:
            ids: List of variation-property record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/properties", json=ids)

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

    async def update_variation_tags(
        self,
        data: list[VariationTagPayload],
    ) -> dict[str, Any]:
        """Bulk create tags on variations.

        Args:
            data: List of tag payloads. Use
                :class:`~plentymarkets._types.VariationTagPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/variations/tags", json=data)

    async def delete_variation_tags(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete variation tags by ID.

        Args:
            ids: List of variation-tag link IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/variations/tags", json=ids)

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

    # -- Attributes -------------------------------------------------------------

    async def create_attributes(
        self,
        data: list[AttributeCreatePayload],
    ) -> dict[str, Any]:
        """Bulk create attributes (variation axes such as colour or size).

        Args:
            data: List of attribute payloads. Use
                :class:`~plentymarkets._types.AttributeCreatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/attributes", json=data)

    async def update_attributes(
        self,
        data: list[AttributeUpdatePayload],
    ) -> dict[str, Any]:
        """Bulk update attributes.

        Args:
            data: List of attribute update payloads. Use
                :class:`~plentymarkets._types.AttributeUpdatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/attributes", json=data)

    async def delete_attributes(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete attributes by ID.

        Args:
            ids: List of attribute IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/attributes", json=ids)

    async def list_attribute_names(
        self,
        attribute_id: int | None = None,
        lang: str | None = None,
        name: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search multilingual attribute display names.

        Args:
            attribute_id: Restrict results to names belonging to this
                attribute ID.
            lang: Restrict results to this two-letter language code.
            name: Restrict results to names containing this string.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched name records, each with
              ``attributeId``, ``lang``, and ``name``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if attribute_id is not None:
            filters["attributeId"] = attribute_id
        if lang is not None:
            filters["lang"] = lang
        if name is not None:
            filters["name"] = name
        params = self._build_params(filters or None, with_)
        return await self._session.get("/rest/pim/attributes/names", params=params or None)

    async def create_attribute_names(
        self,
        data: list[AttributeNamePayload],
    ) -> dict[str, Any]:
        """Bulk create multilingual attribute display names.

        Args:
            data: List of name payloads. Use
                :class:`~plentymarkets._types.AttributeNamePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/attributes/names", json=data)

    async def update_attribute_names(
        self,
        data: list[AttributeNamePayload],
    ) -> dict[str, Any]:
        """Bulk update multilingual attribute display names.

        Args:
            data: List of name payloads. Use
                :class:`~plentymarkets._types.AttributeNamePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/attributes/names", json=data)

    async def delete_attribute_names(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete attribute names by ID.

        Args:
            ids: List of attribute-name record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/attributes/names", json=ids)

    async def list_attribute_values(
        self,
        ids: list[int] | None = None,
        attribute_id: int | None = None,
        backend_name: str | None = None,
        name: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search attribute values (e.g. "Red", "Blue" for a colour attribute).

        Args:
            ids: Restrict results to attribute values with these IDs.
            attribute_id: Restrict results to values belonging to this
                attribute ID.
            backend_name: Restrict results to this exact back-end name.
            name: Restrict results to values whose display name contains this
                string.
            with_: Optional list of related data to embed. Accepted values:
                ``"names"`` (multilingual display names).

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched value records, each with at
              minimum ``id``, ``attributeId``, and ``backendName``.
            - ``totalsCount`` (int): Total number of matching values.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if ids is not None:
            filters["ids"] = ",".join(str(i) for i in ids)
        if attribute_id is not None:
            filters["attributeId"] = attribute_id
        if backend_name is not None:
            filters["backendName"] = backend_name
        if name is not None:
            filters["name"] = name
        params = self._build_params(filters or None, with_)
        return await self._session.get("/rest/pim/attributes/values", params=params or None)

    async def create_attribute_values(
        self,
        data: list[AttributeValuePayload],
    ) -> dict[str, Any]:
        """Bulk create attribute values.

        Args:
            data: List of attribute value payloads. Use
                :class:`~plentymarkets._types.AttributeValuePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/attributes/values", json=data)

    async def update_attribute_values(
        self,
        data: list[AttributeValuePayload],
    ) -> dict[str, Any]:
        """Bulk update attribute values.

        Args:
            data: List of attribute value payloads. Use
                :class:`~plentymarkets._types.AttributeValuePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/attributes/values", json=data)

    async def delete_attribute_values(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete attribute values by ID.

        Args:
            ids: List of attribute value IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/attributes/values", json=ids)

    async def get_attribute_value(self, value_id: int) -> dict[str, Any]:
        """Get a single attribute value by ID.

        Args:
            value_id: The PlentyMarkets attribute value ID.

        Returns:
            A dict with the following keys (based on the fields exposed by
            :meth:`list_attribute_values`; PlentyMarkets does not publish a
            fixed schema for this endpoint — verify against a live system):

            - ``id`` (int): The attribute value ID.
            - ``attributeId`` (int): The parent attribute ID.
            - ``backendName`` (str): Internal back-end name for this value.
            - ``position`` (int): Display sort position among the attribute's
              values.
            - ``image`` (str | None): Linked image path or URL, if any.
        """
        return await self._session.get(f"/rest/pim/attributes/values/{value_id}")

    async def list_attribute_value_names(
        self,
        value_id: int | None = None,
        lang: str | None = None,
        name: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search multilingual display names for attribute values.

        Args:
            value_id: Restrict results to names belonging to this attribute
                value ID.
            lang: Restrict results to this two-letter language code.
            name: Restrict results to names containing this string.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched name records, each with
              ``valueId``, ``lang``, and ``name``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if value_id is not None:
            filters["valueId"] = value_id
        if lang is not None:
            filters["lang"] = lang
        if name is not None:
            filters["name"] = name
        params = self._build_params(filters or None, with_)
        return await self._session.get(
            "/rest/pim/attributes/values/names", params=params or None
        )

    async def create_attribute_value_names(
        self,
        data: list[AttributeValueNamePayload],
    ) -> dict[str, Any]:
        """Bulk create multilingual display names for attribute values.

        Args:
            data: List of name payloads. Use
                :class:`~plentymarkets._types.AttributeValueNamePayload` for
                IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/attributes/values/names", json=data)

    async def update_attribute_value_names(
        self,
        data: list[AttributeValueNamePayload],
    ) -> dict[str, Any]:
        """Bulk update multilingual display names for attribute values.

        Args:
            data: List of name payloads. Use
                :class:`~plentymarkets._types.AttributeValueNamePayload` for
                IDE autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/attributes/values/names", json=data)

    async def delete_attribute_value_names(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete attribute value names by ID.

        Args:
            ids: List of attribute-value-name record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete(
            "/rest/pim/attributes/values/names", json=ids
        )

    async def list_categories(
        self,
        ids: list[int] | None = None,
        type_: str | None = None,
        level: int | None = None,
        name: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search categories.

        Args:
            ids: Restrict results to categories with these IDs.
            type_: Restrict results to categories of this type. Common values:
                ``"item"`` (product categories), ``"content"`` (CMS pages),
                ``"container"``, ``"blog"``.
            level: Restrict results to categories at this tree depth (1=root).
            name: Restrict results to categories whose name contains this string.
            with_: Optional list of related data to embed. Accepted values:
                ``"details"`` (multilingual name, description, meta data),
                ``"clients"`` (which stores have the category active),
                ``"branch"`` (full ancestor path).

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched category records. Each dict
              contains at minimum ``id`` and ``type``; additional keys depend
              on the ``with_`` includes requested.
            - ``totalsCount`` (int): Total number of matching categories.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if ids is not None:
            filters["ids"] = ",".join(str(i) for i in ids)
        if type_ is not None:
            filters["type"] = type_
        if level is not None:
            filters["level"] = level
        if name is not None:
            filters["name"] = name
        params = self._build_params(filters or None, with_)
        return await self._session.get("/rest/pim/categories", params=params or None)

    async def get_category(
        self,
        category_id: int,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a single category by ID.

        Args:
            category_id: The PlentyMarkets category ID.
            with_: Optional list of related data to embed (same values as
                :meth:`list_categories`).

        Returns:
            A dict with the following keys:

            - ``id`` (int): The category ID.
            - ``type`` (str): Category type (e.g. ``"item"``, ``"content"``).
            - ``parentCategoryId`` (int | None): Parent category ID, or
              ``None`` for root categories.
            - ``level`` (int): Tree depth (1=root).
            - ``right`` (str): Visibility. ``"all"`` or ``"customer"``.
            - ``sitemap`` (str): Whether included in sitemap (``"Y"``/``"N"``).
            - ``linklist`` (str): Whether shown in link list (``"Y"``/``"N"``).
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        params = self._build_params(None, with_)
        return await self._session.get(
            f"/rest/pim/categories/{category_id}",
            params=params or None,
        )

    async def list_category_branches(
        self,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search category branches (full path from root to leaf).

        Args:
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched branch records, each with at
              minimum ``categoryId`` and ``branch`` (list[int] of ancestor
              category IDs from root to the category itself).
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        params = self._build_params(None, with_)
        return await self._session.get(
            "/rest/pim/categories/branches", params=params or None
        )

    async def list_category_clients(
        self,
        category_id: int | None = None,
        plenty_id: int | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search which clients (stores) have each category active.

        Args:
            category_id: Restrict results to this category ID.
            plenty_id: Restrict results to this client (store) ID.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched records, each with
              ``categoryId`` and ``plentyId``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if category_id is not None:
            filters["categoryId"] = category_id
        if plenty_id is not None:
            filters["plentyId"] = plenty_id
        params = self._build_params(filters or None, with_)
        return await self._session.get(
            "/rest/pim/categories/clients", params=params or None
        )

    async def list_category_details(
        self,
        category_id: int | None = None,
        plenty_id: int | None = None,
        lang: str | None = None,
        name: str | None = None,
        name_url: str | None = None,
        meta_keywords: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search category detail records (multilingual names, descriptions, meta data).

        Args:
            category_id: Restrict results to this category ID.
            plenty_id: Restrict results to this client (store) ID.
            lang: Restrict results to this two-letter language code.
            name: Restrict results to details whose name contains this string.
            name_url: Restrict results to details whose URL slug contains this
                string.
            meta_keywords: Restrict results to details whose meta keywords
                contain this string.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched detail records, each with at
              minimum ``categoryId``, ``lang``, and ``name``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if category_id is not None:
            filters["categoryId"] = category_id
        if plenty_id is not None:
            filters["plentyId"] = plenty_id
        if lang is not None:
            filters["lang"] = lang
        if name is not None:
            filters["name"] = name
        if name_url is not None:
            filters["nameUrl"] = name_url
        if meta_keywords is not None:
            filters["metaKeywords"] = meta_keywords
        params = self._build_params(filters or None, with_)
        return await self._session.get(
            "/rest/pim/categories/details", params=params or None
        )

    async def list_category_properties(
        self,
        category_id: int | None = None,
        plenty_id: int | None = None,
        value: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search category property links.

        Args:
            category_id: Restrict results to this category ID.
            plenty_id: Restrict results to this client (store) ID.
            value: Restrict results to properties with this value.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched property link records, each
              with at minimum ``categoryId`` and ``value``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if category_id is not None:
            filters["categoryId"] = category_id
        if plenty_id is not None:
            filters["plentyId"] = plenty_id
        if value is not None:
            filters["value"] = value
        params = self._build_params(filters or None, with_)
        return await self._session.get(
            "/rest/pim/categories/properties", params=params or None
        )

    async def list_attributes(
        self,
        ids: list[int] | None = None,
        backend_name: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search attributes (variation axes such as colour or size).

        Args:
            ids: Restrict results to attributes with these IDs.
            backend_name: Restrict results to the attribute with this exact
                back-end name (case-sensitive).
            with_: Optional list of related data to embed. Accepted values:
                ``"names"`` (multilingual display names),
                ``"values"`` (all attribute values),
                ``"values.names"`` (multilingual names for each value),
                ``"maps"`` (marketplace attribute mappings).

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched attribute records. Each dict
              contains at minimum ``id`` and ``backendName``; additional keys
              depend on the ``with_`` includes requested.
            - ``totalsCount`` (int): Total number of matching attributes.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if ids is not None:
            filters["ids"] = ",".join(str(i) for i in ids)
        if backend_name is not None:
            filters["backendName"] = backend_name
        params = self._build_params(filters or None, with_)
        return await self._session.get("/rest/pim/attributes", params=params or None)

    async def get_attribute(self, attribute_id: int) -> dict[str, Any]:
        """Get a single attribute by ID.

        Args:
            attribute_id: The PlentyMarkets attribute ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The attribute ID.
            - ``backendName`` (str): Internal back-end name (unique, no commas,
              colons, semicolons, or quotes).
            - ``position`` (int): Display sort position in the attribute list.
            - ``isSurchargePercental`` (bool): Whether value surcharges are
              treated as a percentage.
            - ``isLinkableToImage`` (bool): Whether images can be linked to
              attribute values.
            - ``amazonAttribute`` (str | None): Linked Amazon attribute name.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.get(f"/rest/pim/attributes/{attribute_id}")

    async def list_sales_prices(
        self,
        ids: list[int] | None = None,
        type_: str | None = None,
        currency: str | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search sales price configurations.

        Sales price configurations define the *type* of price (default, RRP,
        special offer, etc.) and which clients, customer classes, countries, and
        referrers the price applies to. Actual price *values* are stored on the
        variation via ``/rest/pim/variations/sales_prices``.

        Args:
            ids: Restrict results to sales prices with these IDs.
            type_: Restrict results to prices of this type. Common values:
                ``"default"``, ``"rrp"``, ``"specialOffer"``, ``"setPrice"``.
            currency: Restrict results to prices in this ISO 4217 currency code
                (e.g. ``"EUR"``, ``"GBP"``).
            with_: Optional list of related data to embed. Accepted values:
                ``"names"`` (multilingual display names),
                ``"accounts"`` (linked client/referrer/country rules).

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched sales price configuration records.
              Each dict contains at minimum ``id``, ``type``, and ``currency``;
              additional keys depend on the ``with_`` includes requested.
            - ``totalsCount`` (int): Total number of matching price configurations.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if ids is not None:
            filters["ids"] = ",".join(str(i) for i in ids)
        if type_ is not None:
            filters["type"] = type_
        if currency is not None:
            filters["currency"] = currency
        params = self._build_params(filters or None, with_)
        return await self._session.get("/rest/pim/sales_prices", params=params or None)

    async def get_sales_price(self, price_id: int) -> dict[str, Any]:
        """Get a single sales price configuration by ID.

        Args:
            price_id: The PlentyMarkets sales price ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The sales price ID.
            - ``type`` (str): Price type (e.g. ``"default"``, ``"rrp"``).
            - ``currency`` (str): ISO 4217 currency code (e.g. ``"EUR"``).
            - ``position`` (int): Display sort position.
            - ``isLiveConversion`` (bool): Whether to apply live FX conversion.
            - ``minimumOrderQuantity`` (float): Minimum quantity for this price
              to apply.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.get(f"/rest/pim/sales_prices/{price_id}")

    async def create_sales_prices(
        self,
        data: list[SalesPriceCreatePayload],
    ) -> dict[str, Any]:
        """Bulk create sales price configurations.

        Args:
            data: List of sales price payloads. Use
                :class:`~plentymarkets._types.SalesPriceCreatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/sales_prices", json=data)

    async def update_sales_prices(
        self,
        data: list[SalesPriceUpdatePayload],
    ) -> dict[str, Any]:
        """Bulk update sales price configurations.

        Args:
            data: List of sales price update payloads. Use
                :class:`~plentymarkets._types.SalesPriceUpdatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/sales_prices", json=data)

    async def delete_sales_prices(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete sales price configurations by ID.

        Args:
            ids: List of sales price configuration IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/sales_prices", json=ids)

    # -- Barcodes -----------------------------------------------------------

    async def list_barcodes(
        self,
        ids: list[int] | None = None,
        code: str | None = None,
        type_: str | None = None,
        referrer_ids: list[int] | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search barcode type configurations.

        Args:
            ids: Restrict results to barcode configurations with these IDs.
            code: Restrict results to this exact barcode code value.
            type_: Restrict results to this barcode symbology/type, e.g.
                ``"EAN13"``.
            referrer_ids: Restrict results to configurations linked to any of
                these referrer IDs.
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched barcode configuration records,
              each with at minimum ``id``, ``name``, and ``type``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        filters: dict[str, Any] = {}
        if ids is not None:
            filters["ids"] = ",".join(str(i) for i in ids)
        if code is not None:
            filters["code"] = code
        if type_ is not None:
            filters["type"] = type_
        if referrer_ids is not None:
            filters["referrerIds"] = ",".join(str(i) for i in referrer_ids)
        params = self._build_params(filters or None, with_)
        return await self._session.get("/rest/pim/barcodes", params=params or None)

    async def create_barcodes(
        self,
        data: list[BarcodeCreatePayload],
    ) -> dict[str, Any]:
        """Bulk create barcode type configurations.

        Args:
            data: List of barcode payloads. Use
                :class:`~plentymarkets._types.BarcodeCreatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/barcodes", json=data)

    async def update_barcodes(
        self,
        data: list[BarcodeUpdatePayload],
    ) -> dict[str, Any]:
        """Bulk update barcode type configurations.

        Args:
            data: List of barcode update payloads. Use
                :class:`~plentymarkets._types.BarcodeUpdatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/barcodes", json=data)

    async def delete_barcodes(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete barcode type configurations by ID.

        Args:
            ids: List of barcode configuration IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/barcodes", json=ids)

    async def list_barcode_duplicates(self) -> dict[str, Any]:
        """List all variations that share a duplicate barcode value.

        Returns:
            A dict with the following keys (PlentyMarkets does not publish a
            fixed schema for this endpoint; verify against a live system):

            - ``entries``: Duplicate groups, keyed by barcode value, each
              mapping to a list of variation IDs sharing that value.
        """
        return await self._session.get("/rest/pim/barcodes/duplicates")

    async def count_barcode_duplicates(self) -> dict[str, Any]:
        """Count of duplicate barcodes across the catalogue.

        Returns:
            A dict with the following keys (PlentyMarkets does not publish a
            fixed schema for this endpoint; verify against a live system):

            - ``count`` (int): Number of barcode values that appear on more
              than one variation.
        """
        return await self._session.get("/rest/pim/barcodes/duplicates/count")

    async def get_barcode_duplicate_settings(self) -> dict[str, Any]:
        """Get settings controlling barcode duplicate detection behaviour.

        Returns:
            The raw response as returned by the API. The OpenAPI spec
            documents this endpoint's response as a JSON array (not the usual
            ``entries``-wrapped envelope), so despite the ``dict`` type hint
            shared by every method on this class, callers should expect a
            ``list[dict]`` at runtime — each dict describing one barcode
            type's duplicate-detection configuration (e.g. ``barcodeType`` and
            ``checkForDuplicates``). Verify against a live system.
        """
        return await self._session.get("/rest/pim/barcodes/duplicates/settings")

    # -- Item serial numbers --------------------------------------------------

    async def list_item_serial_numbers(
        self,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search serial numbers assigned to item variations.

        Args:
            with_: Optional list of related data to embed.

        Returns:
            A dict with the following keys:

            - ``entries`` (list[dict]): Matched serial number records, each
              with at minimum ``id``, ``itemId``, and ``serialNumber``.
            - ``totalsCount`` (int): Total number of matching records.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``page`` (int): Current page number.
        """
        params = self._build_params(None, with_)
        return await self._session.get(
            "/rest/pim/item-serial-numbers", params=params or None
        )

    async def create_item_serial_numbers(
        self,
        data: list[ItemSerialNumberPayload],
    ) -> dict[str, Any]:
        """Bulk create item serial numbers.

        Args:
            data: List of serial number payloads. Use
                :class:`~plentymarkets._types.ItemSerialNumberPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/item-serial-numbers", json=data)

    async def update_item_serial_numbers(
        self,
        data: list[ItemSerialNumberPayload],
    ) -> dict[str, Any]:
        """Bulk update item serial numbers.

        Args:
            data: List of serial number payloads. Use
                :class:`~plentymarkets._types.ItemSerialNumberPayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/item-serial-numbers", json=data)

    async def delete_item_serial_numbers(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete item serial numbers by ID.

        Args:
            ids: List of serial number record IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/item-serial-numbers", json=ids)

    # -- Item lookups -----------------------------------------------------------

    async def get_item_attributes(self, item_id: int) -> dict[str, Any]:
        """Get all attributes linked to a given item.

        Args:
            item_id: The PlentyMarkets item ID.

        Returns:
            The raw response as returned by the API. The OpenAPI spec
            documents this endpoint's response as a JSON array (not the usual
            ``entries``-wrapped envelope), so despite the ``dict`` type hint
            shared by every method on this class, callers should expect a
            ``list[dict]`` at runtime — each dict describing one linked
            attribute, with at minimum ``attributeId`` and ``backendName``.
            Verify against a live system.
        """
        return await self._session.get(f"/rest/pim/items/{item_id}/attributes")

    async def get_item_combinations(self, item_id: int) -> dict[str, Any]:
        """Get all valid variation combinations (attribute value sets) for an item.

        Args:
            item_id: The PlentyMarkets item ID.

        Returns:
            The raw response as returned by the API. The OpenAPI spec
            documents this endpoint's response as a JSON array (not the usual
            ``entries``-wrapped envelope), so despite the ``dict`` type hint
            shared by every method on this class, callers should expect a
            ``list[dict]`` at runtime — each dict describing one valid
            combination, with at minimum ``attributeValueSetIds``
            (list[int]). Verify against a live system.
        """
        return await self._session.get(f"/rest/pim/items/{item_id}/combinations")
