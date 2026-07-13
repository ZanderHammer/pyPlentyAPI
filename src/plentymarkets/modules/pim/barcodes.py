from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        BarcodeCreatePayload,
        BarcodeUpdatePayload,
    )

from ._base import PimBase


class BarcodesMixin(PimBase):
    """Barcode definition CRUD and duplicate detection."""

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

