from __future__ import annotations

from typing import Any, AsyncIterator

from .._session import _Session


class ItemsModule:
    """Wraps the PlentyMarkets ``/rest/items`` endpoints.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, item_id: int) -> dict:
        """Get a single item by ID.

        Args:
            item_id: The PlentyMarkets item ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The item ID.
            - ``position`` (int): Item sort position.
            - ``manufacturerId`` (int): Manufacturer ID.
            - ``stockType`` (int): Stock type. 0=stocked, 1=production,
              2=colli, 3=special order.
            - ``vatId`` (int): VAT configuration ID.
            - ``producingCountryId`` (int): Country of origin ID.
            - ``condition`` (int): Item condition (0–5).
            - ``conditionApi`` (int): Condition exposed via API (0–5).
            - ``mainVariationId`` (int): ID of the main variation.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
            - ``itemProperties`` (list[dict]): Custom item properties.
            - ``texts`` (list[dict]): Multilingual name/description texts.
        """
        return await self._session.get(f"/rest/items/{item_id}")

    async def list(self, page: int = 1, items_per_page: int = 50) -> dict:
        """List items with pagination.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching items.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Item dicts; same keys as ``get()``.
        """
        return await self._session.get(
            "/rest/items",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def create(self, data: dict) -> dict:
        """Create a new item.

        Args:
            data: Item payload dict. Recommended keys: ``vatId``,
                ``producingCountryId``, ``stockType``.

        Returns:
            The created item dict; same keys as ``get()``.
        """
        return await self._session.post("/rest/items", json=data)

    async def update(self, item_id: int, data: dict) -> dict:
        """Update an existing item.

        Args:
            item_id: The PlentyMarkets item ID.
            data: Fields to update (partial update supported).

        Returns:
            The updated item dict; same keys as ``get()``.
        """
        return await self._session.put(f"/rest/items/{item_id}", json=data)

    async def paginate_items(
        self, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every item across all pages.

        Args:
            items_per_page: Results per page request (max 250).

        Yields:
            Individual item dicts; same keys as ``get()``.
        """
        page = 1
        while True:
            result = await self.list(page=page, items_per_page=items_per_page)
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1
