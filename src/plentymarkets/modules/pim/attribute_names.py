from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        AttributeNamePayload,
    )

from ._base import PimBase


class AttributeNamesMixin(PimBase):
    """Translated names of attributes."""

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
