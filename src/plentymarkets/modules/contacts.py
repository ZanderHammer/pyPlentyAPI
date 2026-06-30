from __future__ import annotations

from typing import AsyncIterator

from .._session import _Session


class ContactsModule:
    """Wraps the PlentyMarkets ``/rest/accounts/contacts`` endpoints.

    Note: PlentyMarkets groups contacts under the ``Account`` API tag.
    The root path is ``/rest/accounts/contacts``, not ``/rest/contacts``.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, contact_id: int) -> dict:
        """Get a single contact by ID.

        Args:
            contact_id: The PlentyMarkets contact ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The contact ID.
            - ``number`` (str): External contact number.
            - ``externalId`` (str): External system ID.
            - ``typeId`` (int): Contact type (1=customer, 2=interested party,
              3=sales rep, 4=supplier, 5=manufacturer, 6=partner).
            - ``firstName`` (str): First name.
            - ``lastName`` (str): Last name.
            - ``fullName`` (str): Formatted full name.
            - ``email`` (str): Primary e-mail address.
            - ``phone`` (str): Primary phone number.
            - ``gender`` (str): Gender (``"male"``, ``"female"``, ``"diverse"``).
            - ``lang`` (str): Preferred language code (e.g. ``"de"``, ``"en"``).
            - ``referrerId`` (float): Sales referrer ID.
            - ``plentyId`` (int): Client (store) ID.
            - ``userId`` (int): Assigned back-end user ID.
            - ``classId`` (int): Customer class ID.
            - ``blocked`` (int): ``0`` = active, ``1`` = blocked.
            - ``rating`` (int): Internal rating (1–5).
            - ``countryId`` (int): Country ID.
            - ``vatNumber`` (str): VAT registration number.
            - ``parentAccountId`` (int): Parent account/company ID.
            - ``createdAt`` (str): ISO 8601 creation timestamp.
            - ``updatedAt`` (str): ISO 8601 last-update timestamp.
        """
        return await self._session.get(f"/rest/accounts/contacts/{contact_id}")

    async def list(self, page: int = 1, items_per_page: int = 50) -> dict:
        """List contacts with pagination.

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page (max 250).

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching contacts.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Contact dicts; same keys as ``get()``.
        """
        return await self._session.get(
            "/rest/accounts/contacts",
            params={"page": page, "itemsPerPage": items_per_page},
        )

    async def create(self, data: dict) -> dict:
        """Create a new contact.

        Args:
            data: Contact payload dict. Common keys: ``firstName``,
                ``lastName``, ``email``, ``typeId``, ``plentyId``.

        Returns:
            The created contact dict; same keys as ``get()``.
        """
        return await self._session.post("/rest/accounts/contacts", json=data)

    async def update(self, contact_id: int, data: dict) -> dict:
        """Update an existing contact.

        Args:
            contact_id: The PlentyMarkets contact ID.
            data: Fields to update (partial update supported).

        Returns:
            The updated contact dict; same keys as ``get()``.
        """
        return await self._session.put(
            f"/rest/accounts/contacts/{contact_id}", json=data
        )

    async def paginate_contacts(
        self, items_per_page: int = 50
    ) -> AsyncIterator[dict]:
        """Async generator that yields every contact across all pages.

        Args:
            items_per_page: Results per page request (max 250).

        Yields:
            Individual contact dicts; same keys as ``get()``.
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
