import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_list_currencies_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies",
        json=[{"currency": "EUR", "isActive": True}],
    )
    result = await orders.list_currencies()
    assert result[0]["currency"] == "EUR"


async def test_get_currency_for_country_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/countries/1",
        json={"currency": "EUR", "isActive": True},
    )
    result = await orders.get_currency_for_country(1)
    assert result["currency"] == "EUR"


async def test_list_exchange_rates_from_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/exchange_rates/from/EUR",
        json=[{"to": "USD", "rate": 1.1}],
    )
    result = await orders.list_exchange_rates_from("EUR")
    assert result == [{"to": "USD", "rate": 1.1}]


async def test_list_exchange_rates_to_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/exchange_rates/to/EUR",
        json=[{"from": "USD", "rate": 0.9}],
    )
    result = await orders.list_exchange_rates_to("EUR")
    assert result == [{"from": "USD", "rate": 0.9}]


async def test_get_currency_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/EUR",
        json={"currency": "EUR", "isActive": True},
    )
    result = await orders.get_currency("EUR")
    assert result["currency"] == "EUR"


async def test_list_currency_countries_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/EUR/countries",
        json=[{"id": 1, "name": "Germany", "isoCode2": "DE"}],
    )
    result = await orders.list_currency_countries("EUR")
    assert result[0]["isoCode2"] == "DE"


async def test_get_currency_exchange_rate_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/currencies/EUR/exchangeRate",
        json={"exchangeRate": 1.0},
    )
    result = await orders.get_currency_exchange_rate("EUR")
    assert result["exchangeRate"] == 1.0
