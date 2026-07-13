from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        ItemSerialNumberPayload,
    )

from ._base import PimBase


class ItemSerialNumbersMixin(PimBase):
    """Item serial number CRUD."""

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

