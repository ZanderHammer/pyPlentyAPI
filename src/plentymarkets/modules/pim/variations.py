from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from ..._types import (
        VariationBaseUpdatePayload,
        VariationCreatePayload,
    )

from ._base import PimBase


class VariationsMixin(PimBase):
    """Core variation search, creation, and deletion."""

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
