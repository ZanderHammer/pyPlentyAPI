from __future__ import annotations

import httpx

from ._session import _Session
from .modules.contacts import ContactsModule
from .modules.items import ItemsModule
from .modules.orders import OrdersModule
from .modules.pim import PimModule
from .modules.stock import StockModule


class PlentyClient:
    """Async client for the PlentyMarkets REST API.

    Use as an async context manager (recommended) or call ``login()``/``aclose()``
    manually.

    Args:
        base_url: Shop base URL, e.g. ``https://your-shop.plentymarkets.com``.
        username: PlentyMarkets back-end user e-mail.
        password: PlentyMarkets back-end user password.

    Example::

        async with PlentyClient(
            base_url="https://your-shop.plentymarkets.com",
            username="user@example.com",
            password="secret",
        ) as client:
            order = await client.orders.get(42)
    """

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self._httpx_client = httpx.AsyncClient()
        self._session = _Session(base_url, username, password, self._httpx_client)
        self._orders: OrdersModule | None = None
        self._items: ItemsModule | None = None
        self._stock: StockModule | None = None
        self._contacts: ContactsModule | None = None
        self._pim: PimModule | None = None

    def __repr__(self) -> str:
        authenticated = self._session._access_token is not None
        return (
            f"PlentyClient(base_url={self._session._base_url!r}, "
            f"authenticated={authenticated})"
        )

    async def __aenter__(self) -> PlentyClient:
        await self.login()
        return self

    async def __aexit__(self, *_: object) -> None:
        try:
            await self.logout()
        finally:
            await self.aclose()

    async def login(self) -> None:
        """Authenticate and acquire an access token."""
        await self._session.login()

    async def logout(self) -> None:
        """Invalidate the current token on the server and clear local state."""
        await self._session.logout()

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._httpx_client.aclose()

    @property
    def orders(self) -> OrdersModule:
        """Access the Orders module (``/rest/orders``)."""
        if self._orders is None:
            self._orders = OrdersModule(self._session)
        return self._orders

    @property
    def items(self) -> ItemsModule:
        """Access the Items module (``/rest/items``)."""
        if self._items is None:
            self._items = ItemsModule(self._session)
        return self._items

    @property
    def stock(self) -> StockModule:
        """Access the Stock module (``/rest/stock``)."""
        if self._stock is None:
            self._stock = StockModule(self._session)
        return self._stock

    @property
    def contacts(self) -> ContactsModule:
        """Access the Contacts module (``/rest/accounts/contacts``)."""
        if self._contacts is None:
            self._contacts = ContactsModule(self._session)
        return self._contacts

    @property
    def pim(self) -> PimModule:
        """Access the PIM module (``/rest/pim``)."""
        if self._pim is None:
            self._pim = PimModule(self._session)
        return self._pim
