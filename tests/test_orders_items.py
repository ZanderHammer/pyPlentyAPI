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


async def test_list_order_items_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/items?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_order_items(42)
    assert result["page"] == 1


async def test_list_order_items_sends_with_and_sort_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/42/items?with=variation%2CserialNumbers"
            "&sortBy=createdAt&sortOrder=desc&page=1&itemsPerPage=50"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_order_items(
        42,
        with_=["variation", "serialNumbers"],
        sort_by="createdAt",
        sort_order="desc",
    )
    assert result["page"] == 1


async def test_paginate_order_items_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/items?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/items?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [i async for i in orders.paginate_order_items(42, items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_order_items_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/items?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [i async for i in orders.paginate_order_items(42)]
    assert results == []


async def test_delete_order_item_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/42/items/77",
        json={},
    )
    result = await orders.delete_order_item(42, 77)
    assert result == {}


async def test_list_order_serial_numbers_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/items/serialNumbers",
        json=[{"serialNumberId": 1, "orderId": 42, "orderItemId": 77, "serialNumber": "SN-1"}],
    )
    result = await orders.list_order_serial_numbers(42)
    assert result[0]["serialNumber"] == "SN-1"


async def test_list_order_item_serial_numbers_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/items/77/serialNumbers",
        json=[{"serialNumberId": 1, "orderId": 42, "orderItemId": 77, "serialNumber": "SN-1"}],
    )
    result = await orders.list_order_item_serial_numbers(42, 77)
    assert result[0]["orderItemId"] == 77


async def test_create_order_item_serial_number_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/items/77/serialNumbers",
        json={"serialNumberId": 1, "orderId": 42, "orderItemId": 77, "serialNumber": "SN-99"},
    )
    result = await orders.create_order_item_serial_number(
        42, 77, {"serialNumber": "SN-99"}
    )
    assert result["serialNumber"] == "SN-99"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"serialNumber": "SN-99"}


async def test_list_order_package_numbers_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/packagenumbers",
        json=["PKG-1", "PKG-2"],
    )
    result = await orders.list_order_package_numbers(42)
    assert result == ["PKG-1", "PKG-2"]
