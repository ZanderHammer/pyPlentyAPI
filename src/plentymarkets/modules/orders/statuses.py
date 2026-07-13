from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from ..._types import OrderStatusNamePayload

from ._base import OrdersBase


class StatusMixin(OrdersBase):
    """Order status *definition* management (color, visibility, names).

    These methods manage order status entities themselves via
    `/rest/orders/statuses/*`. This is unrelated to
    :meth:`~plentymarkets.modules.orders.core.CoreMixin.update_status`,
    which sets the `statusId` field *on an order*.
    """

    async def list_status_definitions(
        self,
        status_id_from: float | None = None,
        status_id_to: float | None = None,
        language: str | None = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> dict[str, Any]:
        """Search order status definitions.

        Args:
            status_id_from: Lower bound (inclusive) of status ID to search from.
            status_id_to: Upper bound (inclusive) of status ID to search to.
            language: Two-letter ISO 639-1 language code to filter/localize
                status names by.
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching statuses.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Status definition dicts, each with:

                - ``statusId`` (float): The status ID.
                - ``isErasable`` (bool): Whether the status can be deleted.
                - ``createdAt`` (str): ISO 8601 creation timestamp.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
                - ``isFrontendVisible`` (bool): Visibility in the online store.
                - ``isReorderVisible`` (bool): Visibility for reorders.
                - ``isRedistributionVisible`` (bool): Visibility for
                  redistributions.
                - ``color`` (str): Hex color code of the status.
        """
        params = self._build_params(
            None,
            statusIdFrom=status_id_from,
            statusIdTo=status_id_to,
            language=language,
            page=page,
            itemsPerPage=items_per_page,
        )
        return await self._session.get("/rest/orders/statuses", params=params)

    async def paginate_status_definitions(
        self,
        status_id_from: float | None = None,
        status_id_to: float | None = None,
        language: str | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every order status definition across all pages.

        Args:
            status_id_from: Lower bound (inclusive) of status ID to search from.
            status_id_to: Upper bound (inclusive) of status ID to search to.
            language: Two-letter ISO 639-1 language code to filter/localize
                status names by.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual status definition dicts (see
            :meth:`list_status_definitions`).
        """
        page = 1
        while True:
            result = await self.list_status_definitions(
                status_id_from=status_id_from,
                status_id_to=status_id_to,
                language=language,
                page=page,
                items_per_page=items_per_page,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def list_all_status_definitions(self) -> list[dict[str, Any]]:
        """List every order status definition, unpaginated.

        Note:
            PlentyMarkets' published OpenAPI spec declares this endpoint's
            response as a generic ``Collection`` (empty schema) rather than a
            typed list. Based on the endpoint's name and its sibling
            :meth:`list_status_definitions`, this is inferred to return a
            bare array of status definition dicts. Verify against a live
            system before relying on it.

        Returns:
            A list of status definition dicts (see
            :meth:`list_status_definitions` for the field reference).
        """
        return await self._session.get("/rest/orders/statuses/all")  # type: ignore[return-value]

    async def create_status_definition(
        self, status_id: float, names: list[OrderStatusNamePayload]
    ) -> dict[str, Any]:
        """Create a new order status definition.

        Args:
            status_id: The ID to assign to the new status.
            names: List of translated name dicts. Use
                :class:`~plentymarkets._types.OrderStatusNamePayload` for IDE
                autocomplete.

        Returns:
            The created status definition dict (see
            :meth:`list_status_definitions` for the field reference).
        """
        return await self._session.post(
            "/rest/orders/statuses",
            json={"statusId": status_id, "names": names},
        )

    async def get_status_definition(self, status_id: float) -> dict[str, Any]:
        """Get a single order status definition by ID.

        Args:
            status_id: The order status ID.

        Returns:
            A status definition dict (see :meth:`list_status_definitions`
            for the field reference).
        """
        return await self._session.get(f"/rest/orders/statuses/{status_id}")

    async def rename_status_definition(
        self, status_id: float, names: list[OrderStatusNamePayload]
    ) -> dict[str, Any]:
        """Update the translated names of an order status definition.

        Args:
            status_id: The order status ID.
            names: List of translated name dicts. Use
                :class:`~plentymarkets._types.OrderStatusNamePayload` for IDE
                autocomplete.

        Returns:
            The updated status definition dict (see
            :meth:`list_status_definitions` for the field reference).
        """
        return await self._session.put(
            f"/rest/orders/statuses/{status_id}", json={"names": names}
        )

    async def delete_status_definition(self, status_id: float) -> dict[str, Any]:
        """Delete an order status definition.

        Args:
            status_id: The order status ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(f"/rest/orders/statuses/{status_id}")

    async def update_status_definition_properties(
        self, status_ids: list[float], new_values: list[str]
    ) -> dict[str, Any]:
        """Bulk-update properties (color/visibility flags) across several
        order status definitions at once.

        Args:
            status_ids: Status IDs to apply the new values to.
            new_values: List of ``"key:value"`` strings, one per property to
                change. The status color must be a hex code (e.g.
                ``"color:#ff0000"``); all other properties
                (``isFrontendVisible``, ``isReorderVisible``,
                ``isRedistributionVisible``) take ``0`` (inactive) or ``1``
                (active), e.g. ``"isFrontendVisible:1"``.

        Returns:
            The API response dict on success, or ``{}`` if the response has
            no body.
        """
        params = {
            "newStatusValues": ",".join(new_values),
            "selectedStatusList": ",".join(str(s) for s in status_ids),
        }
        return await self._session.post(
            "/rest/orders/statuses/group_functions", params=params
        )
