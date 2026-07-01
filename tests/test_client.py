import pytest
import httpx
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

from plentymarkets import PlentyClient
from plentymarkets.modules.orders import OrdersModule
from plentymarkets.modules.items import ItemsModule
from plentymarkets.modules.stock import StockModule
from plentymarkets.modules.contacts import ContactsModule
from plentymarkets.modules.pim import PimModule

BASE_URL = "https://shop.example.com"


async def test_context_manager_logs_in_and_out(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/login",
        json={"accessToken": "tok", "expiresIn": 86400},
    )
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/login",
        status_code=200,
    )

    async with PlentyClient(BASE_URL, "user", "pass"):
        pass

    requests = httpx_mock.get_requests()
    assert requests[0].method == "POST"
    assert requests[1].method == "DELETE"


async def test_orders_property_returns_orders_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.orders, OrdersModule)


async def test_items_property_returns_items_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.items, ItemsModule)


async def test_stock_property_returns_stock_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.stock, StockModule)


async def test_contacts_property_returns_contacts_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.contacts, ContactsModule)


async def test_pim_property_returns_pim_module(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert isinstance(client.pim, PimModule)


async def test_module_properties_are_lazily_cached(httpx_mock):
    client = PlentyClient(BASE_URL, "user", "pass")
    assert client.orders is client.orders
    assert client.items is client.items
