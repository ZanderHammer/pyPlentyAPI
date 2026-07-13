from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        AttributeCreatePayload,
        AttributeUpdatePayload,
    )

from ._base import PimBase


class AttributesMixin(PimBase):
    """Attribute entity CRUD."""

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
