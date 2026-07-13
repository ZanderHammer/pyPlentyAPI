from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        AttributeValuePayload,
        AttributeValueNamePayload,
    )

from ._base import PimBase


class AttributeValuesMixin(PimBase):
    """Attribute values and their translated names."""

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
