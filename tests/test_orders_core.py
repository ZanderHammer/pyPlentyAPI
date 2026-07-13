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


async def test_get_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42, "statusId": 5.0},
    )
    result = await orders.get(42)
    assert result["id"] == 42


async def test_list_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=25",
        json={"page": 2, "totalsCount": 50, "isLastPage": True, "entries": []},
    )
    result = await orders.list(page=2, items_per_page=25)
    assert result["page"] == 2


async def test_list_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    await orders.list()
    request = httpx_mock.get_request()
    assert "page=1" in str(request.url)
    assert "itemsPerPage=50" in str(request.url)


async def test_create_posts_data(httpx_mock, orders):
    payload = {"typeId": 1, "plentyId": 12345}
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders",
        json={"id": 99, "typeId": 1},
    )
    result = await orders.create(payload)
    assert result["id"] == 99


async def test_update_status_puts_to_order_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42, "statusId": 8.0},
    )
    result = await orders.update_status(42, status_id=8.0)
    assert result["statusId"] == 8.0


async def test_paginate_orders_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [order async for order in orders.paginate_orders(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_orders_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_orders()]
    assert results == []


async def test_delete_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/42",
        json={},
    )
    result = await orders.delete(42)
    assert result == {}


async def test_cancel_puts_to_cancel_url_with_no_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/cancel",
        json={"id": 42, "statusId": 8.0},
    )
    result = await orders.cancel(42)
    assert result["statusId"] == 8.0
    request = httpx_mock.get_request()
    assert request.content == b"{}"


async def test_cancel_sends_status_id_and_message(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/cancel",
        json={"id": 42, "statusId": 8.0},
    )
    await orders.cancel(42, status_id=8.0, message="Cancelled by customer")
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "statusId": 8.0,
        "message": "Cancelled by customer",
    }


async def test_get_family_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/family",
        json={"originOrderId": 10, "mainSalesOrderId": 42},
    )
    result = await orders.get_family(42)
    assert result["originOrderId"] == 10


async def test_get_my_account_url_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/my_account_url",
        json=["https://shop.example.com/my-account/orders/42"],
    )
    result = await orders.get_my_account_url(42)
    assert result == ["https://shop.example.com/my-account/orders/42"]


async def test_search_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search()
    assert result["page"] == 1


async def test_search_sends_filters_with_and_sort_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/search?statusId=5.0&with=documents%2Caddress"
            "&page=1&itemsPerPage=50&sortBy=updatedAt&sortOrder=desc"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search(
        filters={"statusId": 5.0},
        with_=["documents", "address"],
        sort_by="updatedAt",
        sort_order="desc",
    )
    assert result["page"] == 1


async def test_search_use_post_hits_post_endpoint(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search(use_post=True)
    assert result["page"] == 1


async def test_paginate_search_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [o async for o in orders.paginate_search(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_search_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_search()]
    assert results == []
