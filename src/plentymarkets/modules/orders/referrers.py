from __future__ import annotations

from typing import Any, AsyncIterator

from ._base import OrdersBase


class ReferrersMixin(OrdersBase):
    """Order referrer management (`/rest/orders/referrers`)."""

    async def list_referrers(
        self, columns: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List all order referrers.

        Args:
            columns: Restrict the response to these referrer attributes.

        Returns:
            A list of referrer dicts, each with:

            - ``id`` (float): The referrer ID.
            - ``isEditable`` (bool): Whether this referrer can be edited or
              deleted.
            - ``backendName`` (str): The referrer's back-end name.
            - ``name`` (str): The referrer's public display name, e.g. on
              documents.
            - ``orderOwnerId`` (int): User ID that owns new orders from this
              referrer.
            - ``isFilterable`` (bool): Whether this referrer can be used as
              a filter.
            - ``origin`` (str): The referrer's origin.
            - ``showInLeads`` (bool): Whether this referrer is shown when
              creating a new lead.
        """
        params = self._build_params(
            None, columns=",".join(columns) if columns else None
        )
        return await self._session.get(  # type: ignore[return-value]
            "/rest/orders/referrers", params=params
        )

    async def get_next_free_referrer_id(self) -> dict[str, Any]:
        """Get the next free main referrer ID.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as ``SimpleRestResponse`` — a bare placeholder schema
            with no fields. Response shape is unverified. Verify against a
            live system before relying on it.

        Returns:
            The API's response dict.
        """
        return await self._session.get("/rest/orders/referrers/next_free_main")

    async def search_referrers(
        self,
        page: int = 1,
        items_per_page: int = 20,
        sort_by: str | None = None,
        sort_order: str | None = None,
        referrer_id: int | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        """Search order referrers with pagination and filters.

        Note:
            The spec documents this endpoint's default ``itemsPerPage`` as
            ``20``, not this module's usual default of ``50``.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page.
            sort_by: Field to sort by. Defaults to ``"id"``.
            sort_order: Sort direction, ``"asc"`` or ``"desc"``. Defaults to
                ``"asc"``.
            referrer_id: Filter by referrer ID.
            name: Filter by referrer name.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching referrers.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Referrer dicts (see
              :meth:`list_referrers` for the field reference).
        """
        params = self._build_params(
            None,
            page=page,
            itemsPerPage=items_per_page,
            sortBy=sort_by,
            sortOrder=sort_order,
            id=referrer_id,
            name=name,
        )
        return await self._session.get("/rest/orders/referrers/search", params=params)

    async def paginate_referrers(
        self,
        sort_by: str | None = None,
        sort_order: str | None = None,
        referrer_id: int | None = None,
        name: str | None = None,
        items_per_page: int = 20,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every matching referrer across all
        pages.

        Args:
            sort_by: Field to sort by (see :meth:`search_referrers`).
            sort_order: Sort direction, ``"asc"`` or ``"desc"``.
            referrer_id: Filter by referrer ID.
            name: Filter by referrer name.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual referrer dicts (see :meth:`list_referrers` for the
            field reference).
        """
        page = 1
        while True:
            result = await self.search_referrers(
                page=page,
                items_per_page=items_per_page,
                sort_by=sort_by,
                sort_order=sort_order,
                referrer_id=referrer_id,
                name=name,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def create_referrer(
        self, parent_referrer_id: int, values: list[str]
    ) -> dict[str, Any]:
        """Create a new order referrer, or a sub-referrer of an existing one.

        Note:
            The spec's path parameter is literally named
            ``{parentReferrerId?}`` — the trailing ``?`` suggests an
            optional segment — yet it is marked ``required: true``, and the
            endpoint's own description says a referrer ID is
            auto-assigned "if no ID is specified." This is a contradiction
            in the published spec; ``parent_referrer_id`` is implemented as
            required here. Verify against a live system whether calling
            ``POST /rest/orders/referrers`` (no segment) is also accepted
            for auto-assignment.

        Args:
            parent_referrer_id: ID of the parent referrer to create a
                sub-referrer under.
            values: List of ``"key:value"`` strings describing the new
                referrer's attributes (see :meth:`list_referrers` for the
                available keys), e.g. ``["name:Google",
                "isFilterable:true"]``.

        Returns:
            The created referrer dict (see :meth:`list_referrers` for the
            field reference).
        """
        params = self._build_params(None, data=",".join(values))
        return await self._session.post(
            f"/rest/orders/referrers/{parent_referrer_id}", params=params
        )

    async def delete_referrer(self, referrer_id: int) -> dict[str, Any]:
        """Delete an order referrer.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as ``SimpleRestResponse`` — a bare placeholder schema
            with no fields. Response shape is unverified. Verify against a
            live system before relying on it.

        Args:
            referrer_id: The referrer ID.

        Returns:
            The API's response dict.
        """
        return await self._session.delete(f"/rest/orders/referrers/{referrer_id}")

    async def get_referrer(self, referrer_id: int) -> dict[str, Any]:
        """Get a single order referrer by ID.

        Args:
            referrer_id: The referrer ID.

        Returns:
            A referrer dict (see :meth:`list_referrers` for the field
            reference).
        """
        return await self._session.get(f"/rest/orders/referrers/{referrer_id}")

    async def update_referrer(
        self, referrer_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an order referrer.

        Note:
            PlentyMarkets' published OpenAPI spec declares no request body
            schema for this endpoint at all. Based on :meth:`list_referrers`'
            field reference, ``data`` likely accepts ``name``,
            ``backendName``, ``orderOwnerId``, ``isFilterable``,
            ``showInLeads`` keys. Verify against a live system before
            relying on this shape.

        Args:
            referrer_id: The referrer ID.
            data: Referrer update payload — see the Note above.

        Returns:
            The updated referrer dict (see :meth:`list_referrers` for the
            field reference).
        """
        return await self._session.put(
            f"/rest/orders/referrers/{referrer_id}", json=data
        )
