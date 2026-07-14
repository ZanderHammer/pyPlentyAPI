from __future__ import annotations

from typing import Any

from ._base import OrdersBase


class CurrenciesMixin(OrdersBase):
    """Currency and exchange-rate lookups (`/rest/orders/currencies`).

    All-read-only; PlentyMarkets exposes no create/update/delete endpoints
    for currencies.
    """

    async def list_currencies(
        self, columns: list[str] | None = None, with_: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List all currencies known to the system.

        Args:
            columns: Restrict the response to these currency attributes.
            with_: Related data to embed.

        Returns:
            A list of currency dicts, each with:

            - ``currency`` (str): The ISO 4217 currency code.
            - ``htmlCode`` (str): HTML entity code for the currency symbol.
            - ``unicodeSign`` (str): Unicode currency symbol, or the HTML
              code if no Unicode symbol exists.
            - ``isActive`` (bool): Whether the currency is active in the
              system (activated per sales price).
            - ``isErasable`` (bool): Whether this currency can be deleted.
            - ``exchangeRate`` (float): The current exchange rate.
        """
        params = self._build_params(
            None, with_=with_, columns=",".join(columns) if columns else None
        )
        return await self._session.get(  # type: ignore[return-value]
            "/rest/orders/currencies", params=params
        )

    async def get_currency_for_country(
        self,
        country_id: int,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get the currency configured for a country.

        Args:
            country_id: The country ID.
            columns: Restrict the response to these currency attributes.
            with_: Related data to embed.

        Returns:
            A currency dict (see :meth:`list_currencies` for the field
            reference).
        """
        params = self._build_params(
            None, with_=with_, columns=",".join(columns) if columns else None
        )
        return await self._session.get(
            f"/rest/orders/currencies/countries/{country_id}", params=params
        )

    async def list_exchange_rates_from(self, currency_iso: str) -> list[Any]:
        """List exchange rates *from* a currency to every other currency.

        Note:
            The spec types ``currencyIso`` as ``integer`` on this operation
            (and :meth:`list_exchange_rates_to`), inconsistent with the
            ``string`` type used everywhere else in this mixin — treated as
            ``str`` here uniformly. Response items are also declared as an
            untyped (``mixed``) schema. Verify against a live system before
            relying on this endpoint's shape.

        Args:
            currency_iso: ISO 4217 currency code to convert from.

        Returns:
            An unverified list of exchange-rate entries.
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/currencies/exchange_rates/from/{currency_iso}"
        )

    async def list_exchange_rates_to(self, currency_iso: str) -> list[Any]:
        """List exchange rates *to* a currency from every other currency.

        Note:
            See the Note on :meth:`list_exchange_rates_from` — the same
            ``currencyIso`` type inconsistency and untyped response items
            apply here.

        Args:
            currency_iso: ISO 4217 currency code to convert to.

        Returns:
            An unverified list of exchange-rate entries.
        """
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/currencies/exchange_rates/to/{currency_iso}"
        )

    async def get_currency(
        self,
        currency_iso: str,
        columns: list[str] | None = None,
        with_: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a single currency by its ISO 4217 code.

        Args:
            currency_iso: ISO 4217 currency code, e.g. ``"EUR"``.
            columns: Restrict the response to these currency attributes.
            with_: Related data to embed.

        Returns:
            A currency dict (see :meth:`list_currencies` for the field
            reference).
        """
        params = self._build_params(
            None, with_=with_, columns=",".join(columns) if columns else None
        )
        return await self._session.get(
            f"/rest/orders/currencies/{currency_iso}", params=params
        )

    async def list_currency_countries(
        self, currency_iso: str, columns: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """List countries that use a given currency.

        Args:
            currency_iso: ISO 4217 currency code, e.g. ``"EUR"``.
            columns: Restrict the response to these country attributes.

        Returns:
            A list of country dicts, each with:

            - ``id`` (int): The country ID.
            - ``name`` (str): The country name.
            - ``shippingDestinationId`` (int): Shipping destination group
              ID.
            - ``active`` (bool): Whether the country is active in the
              system.
            - ``storehouseId`` (int): Associated storehouse ID.
            - ``isoCode2`` (str): ISO 3166-1 alpha-2 code.
            - ``isoCode3`` (str): ISO 3166-1 alpha-3 code.
            - ``lang`` (str): The country's default language.
            - ``isCountryStateMandatory`` (bool): Whether a state/province
              is required for addresses in this country.
            - ``vatCodes`` (list): VAT code configurations for this
              country.
        """
        params = self._build_params(
            None, columns=",".join(columns) if columns else None
        )
        return await self._session.get(  # type: ignore[return-value]
            f"/rest/orders/currencies/{currency_iso}/countries", params=params
        )

    async def get_currency_exchange_rate(self, currency_iso: str) -> dict[str, Any]:
        """Get the current exchange rate for a currency.

        Note:
            The spec types ``currencyIso`` as ``integer`` on this
            operation, inconsistent with the ``string`` type used
            elsewhere in this mixin — treated as ``str`` here uniformly.

        Args:
            currency_iso: ISO 4217 currency code, e.g. ``"EUR"``.

        Returns:
            A dict with a single key:

            - ``exchangeRate`` (float): The current exchange rate.
        """
        return await self._session.get(
            f"/rest/orders/currencies/{currency_iso}/exchangeRate"
        )
