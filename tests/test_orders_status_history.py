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


async def test_list_status_history_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/status-history?page=1&itemsPerPage=50",
        json={
            "page": 1,
            "totalsCount": 1,
            "isLastPage": True,
            "entries": [{"id": 1, "orderId": 42, "statusId": 5.0}],
        },
    )
    result = await orders.list_status_history()
    assert result["entries"][0]["orderId"] == 42


async def test_list_status_history_sends_filters(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/status-history"
            "?orderId=42&statusId=5.0&page=1&itemsPerPage=50"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_status_history(order_id=42, status_id=5.0)
    assert result["page"] == 1


async def test_paginate_status_history_yields_all_items(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/status-history?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/status-history?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [h async for h in orders.paginate_status_history(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_get_order_status_history_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/status-history",
        json=[{"id": 1, "orderId": 42, "statusId": 3.0}],
    )
    result = await orders.get_order_status_history(42)
    assert result[0]["statusId"] == 3.0
