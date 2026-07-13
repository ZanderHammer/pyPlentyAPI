from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        VariationCategoryPayload,
        VariationDefaultCategoryPayload,
        VariationTagPayload,
        VariationPropertyPayload,
        VariationCommentPayload,
    )

from ._base import PimBase


class VariationTaxonomyMixin(PimBase):
    """Bulk update/delete of a variation's categorization and annotations (categories, tags, properties, comments)."""

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
