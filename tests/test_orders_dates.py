import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_list_date_types_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types",
        json=[{"id": 2, "isErasable": False, "position": 1}],
    )
    result = await orders.list_date_types()
    assert result[0]["id"] == 2


async def test_get_date_type_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types/7",
        json={"id": 7, "isErasable": True, "position": 3},
    )
    result = await orders.get_date_type(7)
    assert result["id"] == 7


async def test_list_date_type_names_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types/7/names",
        json=[{"id": 1, "typeId": 7, "lang": "en", "name": "Payment due date"}],
    )
    result = await orders.list_date_type_names(7)
    assert result[0]["lang"] == "en"


async def test_get_date_type_name_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types/7/names/de",
        json={"id": 1, "typeId": 7, "lang": "de", "name": "Zahlungsziel"},
    )
    result = await orders.get_date_type_name(7, "de")
    assert result["name"] == "Zahlungsziel"


async def test_list_order_dates_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/dates",
        json=[{"id": 1, "orderId": 42, "typeId": 2}],
    )
    result = await orders.list_order_dates(42)
    assert result[0]["orderId"] == 42


async def test_get_order_date_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/dates/7",
        json={"id": 1, "orderId": 42, "typeId": 7},
    )
    result = await orders.get_order_date(42, 7)
    assert result["typeId"] == 7
