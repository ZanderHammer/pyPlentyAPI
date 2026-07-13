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


async def test_search_item_transactions_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/transactions?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search_item_transactions()
    assert result["page"] == 1


async def test_search_item_transactions_sends_filters(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/items/transactions?with=orderItem"
            "&columns=quantity%2Cstatus&orderItemId=10&orderId=42"
            "&direction=out&status=in&isBooked=true&sortBy=createdAt"
            "&sortOrder=desc&page=1&itemsPerPage=50"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search_item_transactions(
        order_item_id=10,
        order_id=42,
        direction="out",
        status="in",
        is_booked=True,
        columns=["quantity", "status"],
        with_=["orderItem"],
        sort_by="createdAt",
        sort_order="desc",
    )
    assert result["page"] == 1


async def test_paginate_item_transactions_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/transactions?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/transactions?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [
        t async for t in orders.paginate_item_transactions(items_per_page=2)
    ]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_item_transactions_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/transactions?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [t async for t in orders.paginate_item_transactions()]
    assert results == []


async def test_update_item_transaction_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/items/transactions/501",
        json={"id": 501, "warehouseLocationId": 3},
    )
    result = await orders.update_item_transaction(
        501,
        warehouse_location_id=3,
        batch="B100",
        best_before_date="2026-12-31",
    )
    assert result["id"] == 501
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "warehouseLocationId": 3,
        "batch": "B100",
        "bestBeforeDate": "2026-12-31",
    }


async def test_update_item_transaction_puts_empty_body_when_no_fields(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/items/transactions/501",
        json={"id": 501},
    )
    await orders.update_item_transaction(501)
    request = httpx_mock.get_request()
    assert request.content == b"{}"


async def test_delete_item_transaction_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/items/transactions/501",
        json={},
    )
    result = await orders.delete_item_transaction(501)
    assert result == {}


async def test_book_item_transactions_sends_query_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=(
            f"{BASE_URL}/rest/orders/items/transactions/booking"
            "?transactionIds=1%2C2%2C3&deliveryNoteNumber=DN-1"
        ),
        json={},
    )
    result = await orders.book_item_transactions(
        [1, 2, 3], delivery_note_number="DN-1"
    )
    assert result == {}


async def test_list_item_transactions_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/items/77/transactions",
        json=[{"id": 1, "orderItemId": 77}],
    )
    result = await orders.list_item_transactions(77)
    assert result[0]["orderItemId"] == 77


async def test_create_item_transaction_posts_data_merges_order_item_id(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/items/77/transactions",
        json={"id": 900, "orderItemId": 77},
    )
    result = await orders.create_item_transaction(
        77, {"quantity": 5, "direction": "in", "status": "regular"}
    )
    assert result["id"] == 900
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "quantity": 5,
        "direction": "in",
        "status": "regular",
        "orderItemId": 77,
    }


async def test_book_item_in_sends_query_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/items/77/booking?deliveryNoteNumber=DN-9",
        json={},
    )
    result = await orders.book_item_in(77, delivery_note_number="DN-9")
    assert result == {}
