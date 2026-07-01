from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from .._types import VariationBaseUpdatePayload

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
