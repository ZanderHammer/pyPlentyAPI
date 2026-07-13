from __future__ import annotations

from typing import Any

from ._base import PimBase


class LookupsMixin(PimBase):
    """Miscellaneous read-only item/Amazon reference lookups."""

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

    # -- Amazon product types ----------------------------------------------------

    async def list_amazon_product_types(self) -> dict[str, Any]:
        """List Amazon product type definitions available for attribute mapping.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; verify against
            a live system before relying on its keys.
        """
        return await self._session.get("/rest/pim/amazon-product-types")
