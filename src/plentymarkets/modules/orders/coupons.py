from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from ..._types import OrderCouponCodeCreatePayload, OrderCouponValidatePayload

from ._base import OrdersBase


class CouponsMixin(OrdersBase):
    """Coupon campaign, coupon code, and redemption/validation management.

    Covers `/rest/orders/coupons/*` (campaigns and code management) and
    `/rest/orders/{orderId}/coupons/*` (redemption against a specific
    order). None of these endpoints are deprecated.
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

    async def validate_coupons(
        self,
        coupons: list[str],
        plenty_id: int,
        ship_to_country: int,
        data: OrderCouponValidatePayload,
        call_from_scheduler: bool | None = None,
        tax_id_number: str | None = None,
        contact_class: int | None = None,
        contact_type: int | None = None,
    ) -> list[dict[str, Any]]:
        """Validate multiple coupon codes at once, without redeeming them.

        Args:
            coupons: Coupon codes to validate.
            plenty_id: The client (store) ID.
            ship_to_country: Country ID of the delivery destination.
            data: Contact and basket payload. Use
                :class:`~plentymarkets._types.OrderCouponValidatePayload`
                for IDE autocomplete. Required keys: ``contactId``,
                ``items``.
            call_from_scheduler: Whether this validation is requested by a
                subscription-order scheduler run.
            tax_id_number: The contact's tax ID number.
            contact_class: The contact's class.
            contact_type: The contact's type.

        Returns:
            A list of validation result dicts, one per coupon, each with:

            - ``campaignId`` (int): The coupon's campaign ID.
            - ``validationType`` (str): The validation mode used.
            - ``contactId`` (int): The contact the coupon was validated
              for.
            - ``couponCode`` (str): The validated coupon code.
            - ``currency`` (str): Currency used for discount amounts.
            - ``exchangeRate`` (float): Exchange rate applied.
            - ``referrer`` (float): Referrer ID used.
            - ``salesDiscount`` (float): Total sales discount granted.
            - ``salesDiscountNet`` (float): Net sales discount granted.
            - ``itemDiscount`` (float): Total item-level discount granted.
            - ``shippingDiscount`` (float): Shipping discount granted.
            - ``restCouponAmount`` (float): Remaining unused coupon
              balance.
            - ``checkedItems`` (list): Basket items the coupon was checked
              against.
        """
        params = self._build_params(
            None,
            coupons=",".join(coupons),
            plentyId=plenty_id,
            shipToCountry=ship_to_country,
            callFromScheduler=call_from_scheduler,
            taxIdNumber=tax_id_number,
            contactClass=contact_class,
            contactType=contact_type,
        )
        return await self._session.post(  # type: ignore[return-value]
            "/rest/orders/coupons/codes", params=params, json=data
        )

    async def list_redeemed_coupon_codes(
        self, contact_id: int, page: int = 1, items_per_page: int = 50
    ) -> dict[str, Any]:
        """List coupon codes redeemed by a contact, with pagination.

        Args:
            contact_id: The contact ID.
            page: Page number (1-indexed).
            items_per_page: Results per page.

        Returns:
            A dict with the following keys:

            - ``page`` (int): Current page number.
            - ``totalsCount`` (int): Total number of redeemed codes.
            - ``isLastPage`` (bool): ``True`` when no further pages exist.
            - ``lastPageNumber`` (int): Number of the last page.
            - ``entries`` (list[dict]): Redeemed-code dicts, each with:

                - ``code`` (str): The coupon code.
                - ``contactId`` (int): The contact who redeemed it.
                - ``openAmount`` (float): Remaining unused balance.
                - ``redeemCount`` (int): Number of times redeemed.
                - ``updatedAt`` (str): ISO 8601 last-update timestamp.
                - ``campaignId`` (int): The code's campaign ID.
                - ``externalTransactionId`` (str): External transaction
                  reference, if any.
        """
        params = self._build_params(
            None, page=page, itemsPerPage=items_per_page
        )
        return await self._session.get(
            f"/rest/orders/coupons/codes/contacts/{contact_id}", params=params
        )

    async def paginate_redeemed_coupon_codes(
        self, contact_id: int, items_per_page: int = 50
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields every coupon code redeemed by a
        contact across all pages.

        Args:
            contact_id: The contact ID.
            items_per_page: Results per page request (max 250).

        Yields:
            Individual redeemed-code dicts (see
            :meth:`list_redeemed_coupon_codes` for the field reference).
        """
        page = 1
        while True:
            result = await self.list_redeemed_coupon_codes(
                contact_id, page=page, items_per_page=items_per_page
            )
            entries = result.get("entries", [])
            if not entries:
                break
            for entry in entries:
                yield entry
            if result.get("isLastPage", True):
                break
            page += 1

    async def validate_coupon(
        self,
        coupon: str,
        plenty_id: int,
        ship_to_country: int,
        data: OrderCouponValidatePayload,
        call_from_scheduler: bool | None = None,
        tax_id_number: str | None = None,
        contact_class: int | None = None,
        contact_type: int | None = None,
    ) -> dict[str, Any]:
        """Validate a single coupon code, without redeeming it.

        Args:
            coupon: The coupon code to validate.
            plenty_id: The client (store) ID.
            ship_to_country: Country ID of the delivery destination.
            data: Contact and basket payload (see :meth:`validate_coupons`).
            call_from_scheduler: Whether this validation is requested by a
                subscription-order scheduler run.
            tax_id_number: The contact's tax ID number.
            contact_class: The contact's class.
            contact_type: The contact's type.

        Returns:
            A single validation result dict (see :meth:`validate_coupons`
            for the field reference).
        """
        params = self._build_params(
            None,
            plentyId=plenty_id,
            shipToCountry=ship_to_country,
            callFromScheduler=call_from_scheduler,
            taxIdNumber=tax_id_number,
            contactClass=contact_class,
            contactType=contact_type,
        )
        return await self._session.post(
            f"/rest/orders/coupons/codes/{coupon}", params=params, json=data
        )

    async def redeem_coupon(self, order_id: int, coupon: str) -> dict[str, Any]:
        """Redeem a coupon code against an order.

        Args:
            order_id: The PlentyMarkets order ID to redeem the coupon on.
            coupon: The coupon code to redeem.

        Returns:
            A validation result dict describing the redemption (see
            :meth:`validate_coupons` for the field reference).
        """
        return await self._session.post(f"/rest/orders/{order_id}/coupons/{coupon}")

    async def validate_order_coupon(self, order_id: int, coupon: str) -> list[Any]:
        """Validate a coupon code against an existing order, without
        redeeming it.

        Note:
            The spec types both ``orderId`` and ``coupon`` as ``integer``
            path segments on this operation — inconsistent with
            :meth:`redeem_coupon`'s sibling endpoint, where ``coupon`` is
            typed ``string``. ``coupon`` is treated as ``str`` here
            uniformly. Response items are also declared as an untyped
            (``mixed``) schema; verify against a live system before relying
            on this endpoint's shape.

        Args:
            order_id: The PlentyMarkets order ID.
            coupon: The coupon code to validate.

        Returns:
            An unverified list of validation result entries.
        """
        return await self._session.post(  # type: ignore[return-value]
            f"/rest/orders/{order_id}/coupons/{coupon}/validate"
        )
