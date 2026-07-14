from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..._types import OrderCouponCodeCreatePayload

from ._base import OrdersBase


class CouponsMixin(OrdersBase):
    """Coupon campaign and coupon-code management (`/rest/orders/coupons/*`).

    None of these endpoints are deprecated.
    """

    async def list_campaigns(self) -> dict[str, Any]:
        """List all coupon campaigns.

        Note:
            The spec documents zero query parameters for this endpoint —
            despite the page-shaped response, there is no way to control
            ``page``/``itemsPerPage``, so no ``paginate_campaigns`` wrapper
            is possible. Verify against a live system whether pagination
            params are silently accepted anyway.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of campaigns.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Campaign dicts, each with:

                - ``id`` (int): The campaign ID.
                - ``name`` (str): The campaign name.
                - ``variable`` (str): Internal campaign variable name.
                - ``isPermittedForExternalReferrers`` (bool): Whether
                  external referrers may use this campaign.
                - ``includeShipping`` (bool): Whether the discount applies
                  to shipping costs.
                - ``unusedCodesCount`` (int): Number of unused codes.
                - ``usedCodesCount`` (int): Number of used codes.
                - ``startsAt`` (str): ISO 8601 campaign start date.
                - ``endsAt`` (str): ISO 8601 campaign end date.
                - ``minOrderValue`` (float): Minimum order value to qualify.
                - ``codeDurationWeeks`` (int): Code validity duration in
                  weeks.
                - ``discountType`` (str): Type of discount granted.
                - ``value`` (float): The discount value.
        """
        return await self._session.get("/rest/orders/coupons/campaigns")

    async def delete_coupon_code(
        self, code: str, without_used: int | None = None
    ) -> dict[str, Any]:
        """Delete a coupon code.

        Note:
            The spec types ``code`` as ``integer`` on this operation,
            inconsistent with the ``string`` type used on
            :meth:`get_coupon_code` — treated as ``str`` here uniformly
            (the coupon code format is alphanumeric,
            ``^[a-zA-Z0-9_-]{6,32}$``).

        Args:
            code: The coupon code.
            without_used: When set, restricts deletion behavior around
                already-used codes (exact semantics undocumented in the
                spec).

        Returns:
            The API's response dict.
        """
        params = self._build_params(None, withoutUsed=without_used)
        return await self._session.delete(
            f"/rest/orders/coupons/campaigns/codes/{code}", params=params
        )

    async def get_coupon_code(
        self, code: str, with_: str | None = None
    ) -> dict[str, Any]:
        """Get information about a coupon code.

        Note:
            The ``with`` query parameter is a plain string on this
            operation (not the usual ``array[string]`` used elsewhere in
            this module), so it bypasses ``_build_params``'s list-join
            convention.

        Args:
            code: The coupon code.
            with_: Related data to embed, as a single string (not a list).

        Returns:
            A dict with the following keys:

            - ``code`` (str): The coupon code.
            - ``campaignId`` (int): The campaign this code belongs to.
            - ``disable`` (bool): Whether the code is disabled.
            - ``consumed`` (bool): Whether the code has been used.
            - ``usedCount`` (int): Number of times the code has been used.
            - ``usedAmount`` (float): Total amount redeemed against this
              code.
            - ``value`` (float): The coupon's value.
        """
        params: dict[str, Any] = {}
        if with_ is not None:
            params["with"] = with_
        return await self._session.get(
            f"/rest/orders/coupons/campaigns/codes/{code}", params=params
        )

    async def set_coupon_code_disabled(
        self, code: str, is_disabled: int
    ) -> dict[str, Any]:
        """Enable or disable a coupon code.

        Note:
            The spec types both ``code`` and ``isDisabled`` as path
            segments of type ``integer``; ``code`` is treated as ``str``
            here uniformly with the rest of this mixin (see the Note on
            :meth:`delete_coupon_code`).

        Args:
            code: The coupon code.
            is_disabled: ``1`` to disable the code, ``0`` to enable it.

        Returns:
            The API's response dict.
        """
        return await self._session.put(
            f"/rest/orders/coupons/campaigns/codes/{code}/disabled/{is_disabled}"
        )

    async def get_campaign(self, campaign_id: int) -> dict[str, Any]:
        """Get a single coupon campaign by ID.

        Args:
            campaign_id: The campaign ID.

        Returns:
            A campaign dict (see :meth:`list_campaigns` for the field
            reference).
        """
        return await self._session.get(f"/rest/orders/coupons/campaigns/{campaign_id}")

    async def create_coupon_code(
        self, campaign_id: int, data: OrderCouponCodeCreatePayload | None = None
    ) -> dict[str, Any]:
        """Create a new coupon code under a campaign.

        Args:
            campaign_id: The campaign ID to create the code under.
            data: Optional code payload. Use
                :class:`~plentymarkets._types.OrderCouponCodeCreatePayload`
                for IDE autocomplete. ``campaignId`` is merged in
                automatically from ``campaign_id`` and must not be
                included.

        Returns:
            A dict with the following keys:

            - ``code`` (str): The (possibly auto-generated) coupon code.
            - ``campaignId`` (int): The campaign this code belongs to.
            - ``disable`` (bool): Whether the code is disabled.
            - ``consumed`` (bool): Whether the code has been used.
            - ``usedCount`` (int): Number of times the code has been used.
            - ``usedAmount`` (float): Total amount redeemed against this
              code.
            - ``value`` (float): The coupon's value.
        """
        return await self._session.post(
            f"/rest/orders/coupons/campaigns/{campaign_id}/codes",
            json={**(data or {}), "campaignId": campaign_id},
        )
