from __future__ import annotations

from typing import Any

from ._base import PimBase


class CategoriesMixin(PimBase):
    """Category tree search and lookups."""

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
