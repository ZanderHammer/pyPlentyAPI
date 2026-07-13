from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import (
        SalesPriceCreatePayload,
        SalesPriceUpdatePayload,
    )

from ._base import PimBase


class SalesPricesMixin(PimBase):
    """Sales price definition CRUD."""

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

    async def create_sales_prices(
        self,
        data: list[SalesPriceCreatePayload],
    ) -> dict[str, Any]:
        """Bulk create sales price configurations.

        Args:
            data: List of sales price payloads. Use
                :class:`~plentymarkets._types.SalesPriceCreatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``created`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.post("/rest/pim/sales_prices", json=data)

    async def update_sales_prices(
        self,
        data: list[SalesPriceUpdatePayload],
    ) -> dict[str, Any]:
        """Bulk update sales price configurations.

        Args:
            data: List of sales price update payloads. Use
                :class:`~plentymarkets._types.SalesPriceUpdatePayload` for IDE
                autocomplete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``updated`` (int) and ``invalid`` (list[dict]). Verify against a
            live system before relying on these keys.
        """
        return await self._session.put("/rest/pim/sales_prices", json=data)

    async def delete_sales_prices(self, ids: list[int]) -> dict[str, Any]:
        """Bulk delete sales price configurations by ID.

        Args:
            ids: List of sales price configuration IDs to delete.

        Returns:
            A dict with the response body returned by the API. PlentyMarkets
            does not publish a fixed schema for this endpoint; expect
            ``deleted`` (int). Verify against a live system before relying on
            this key.
        """
        return await self._session.delete("/rest/pim/sales_prices", json=ids)

