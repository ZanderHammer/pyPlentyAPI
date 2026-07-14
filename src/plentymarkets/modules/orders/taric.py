from __future__ import annotations

from typing import Any, AsyncIterator

from ._base import OrdersBase


class TaricMixin(OrdersBase):
    """TARIC VAT assignment configuration (`/rest/system/settings/taric_vat_assignment`).

    Tagged ``Order`` in PlentyMarkets' OpenAPI spec, but this is genuinely
    tax/system configuration (mapping TARIC customs codes to VAT rates per
    country), not order data.
    """

    async def list_taric_vat_assignments(
        self,
        page: int = 1,
        items_per_page: int = 50,
        country_id: int | None = None,
        taric_code: str | None = None,
    ) -> dict[str, Any]:
        """List TARIC VAT assignments, with pagination and filters.

        Note:
            The spec types ``taricCode`` as ``integer`` for this filter,
            inconsistent with the ``string`` path-param type used on the
            single-resource endpoints below — treated as ``str`` here
            uniformly (TARIC codes match ``^[0-9a-z]{1,14}$``).

        Args:
            page: Page number (1-indexed).
            items_per_page: Results per page.
            country_id: Filter by country ID.
            taric_code: Filter by TARIC code.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of matching assignments.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Assignment dicts (see
              :meth:`get_taric_vat_assignment` for the field reference).
        """
        params = self._build_params(
            None,
            page=page,
            itemsPerPage=items_per_page,
            countryId=country_id,
            taricCode=taric_code,
        )
        return await self._session.get(
            "/rest/system/settings/taric_vat_assignment", params=params
        )

    async def paginate_taric_vat_assignments(
        self,
        country_id: int | None = None,
        taric_code: str | None = None,
        items_per_page: int = 50,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every TARIC VAT assignment across all
        pages.

        Args:
            country_id: Filter by country ID.
            taric_code: Filter by TARIC code.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual assignment dicts (see
            :meth:`get_taric_vat_assignment` for the field reference).
        """
        page = 1
        while True:
            result = await self.list_taric_vat_assignments(
                page=page,
                items_per_page=items_per_page,
                country_id=country_id,
                taric_code=taric_code,
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def delete_taric_vat_assignment(
        self, taric_code: str, country_id: int
    ) -> dict[str, Any]:
        """Delete a TARIC VAT assignment.

        Note:
            The spec declares a requestBody for this DELETE operation that
            just redeclares ``taricCode``/``countryId`` — both already
            supplied as path parameters and nothing new. No body is sent,
            matching how :meth:`delete_status_definition`/
            :meth:`delete_order_item` never resend path-supplied fields.

        Args:
            taric_code: The TARIC customs code.
            country_id: The country ID.

        Returns:
            Empty dict on success (the API returns no body).
        """
        return await self._session.delete(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}"
        )

    async def get_taric_vat_assignment(
        self, taric_code: str, country_id: int
    ) -> dict[str, Any]:
        """Get a single TARIC VAT assignment.

        Args:
            taric_code: The TARIC customs code.
            country_id: The country ID.

        Returns:
            A dict with the following keys:

            - ``id`` (int): The assignment record ID.
            - ``taricCode`` (str): The TARIC customs code.
            - ``countryId`` (int): The country ID.
            - ``vatField`` (str): The VAT rate ID for this TARIC
              code/country combination.
        """
        return await self._session.get(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}"
        )

    async def create_taric_vat_assignment(
        self, taric_code: str, country_id: int, vat_field: str
    ) -> dict[str, Any]:
        """Create a TARIC VAT assignment.

        Args:
            taric_code: The TARIC customs code, matching
                ``^[0-9a-z]{1,14}$``.
            country_id: The country ID this configuration belongs to.
            vat_field: The VAT rate ID for this TARIC code/country
                combination.

        Returns:
            The created assignment dict (see
            :meth:`get_taric_vat_assignment` for the field reference).
        """
        return await self._session.post(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}",
            json={
                "taricCode": taric_code,
                "countryId": country_id,
                "vatField": vat_field,
            },
        )

    async def update_taric_vat_assignment(
        self, taric_code: str, country_id: int, vat_field: str
    ) -> dict[str, Any]:
        """Update a TARIC VAT assignment.

        Args:
            taric_code: The TARIC customs code.
            country_id: The country ID.
            vat_field: The new VAT rate ID for this TARIC code/country
                combination.

        Returns:
            The updated assignment dict (see
            :meth:`get_taric_vat_assignment` for the field reference).
        """
        return await self._session.put(
            f"/rest/system/settings/taric_vat_assignment/{taric_code}/{country_id}",
            json={
                "taricCode": taric_code,
                "countryId": country_id,
                "vatField": vat_field,
            },
        )
