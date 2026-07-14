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


async def test_get_orders_batch_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/batch?orderIds=1%2C2&addOrderItems=true",
        json=[{"id": 1}, {"id": 2}],
    )
    result = await orders.get_orders_batch([1, 2], add_order_items=True)
    assert result == [{"id": 1}, {"id": 2}]


async def test_list_contact_orders_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_contact_orders(7)
    assert result["page"] == 1


async def test_paginate_contact_orders_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [
        o async for o in orders.paginate_contact_orders(7, items_per_page=2)
    ]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_contact_orders_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/contacts/7?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_contact_orders(7)]
    assert results == []


async def test_create_multi_order_posts_to_contact_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/contacts/7/multi_order",
        json={"id": 99, "typeId": 9},
    )
    result = await orders.create_multi_order(7)
    assert result["typeId"] == 9
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_list_accounting_summaries_defaults_to_page_1_and_10(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/documents/accounting_summary?page=1&itemsPerPage=10",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_accounting_summaries()
    assert result["page"] == 1


async def test_list_accounting_summaries_sends_filters(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/documents/accounting_summary?orderId=42"
            "&documentType=reversal_document&createdAtFrom=2026-01-01"
            "&createdAtTo=2026-02-01&page=1&itemsPerPage=10"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_accounting_summaries(
        order_id=42,
        document_type="reversal_document",
        created_at_from="2026-01-01",
        created_at_to="2026-02-01",
    )
    assert result["page"] == 1


async def test_paginate_accounting_summaries_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/documents/accounting_summary?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"key": "a"}, {"key": "b"}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/documents/accounting_summary?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"key": "c"}],
        },
    )
    results = [
        s async for s in orders.paginate_accounting_summaries(items_per_page=2)
    ]
    assert [r["key"] for r in results] == ["a", "b", "c"]


async def test_book_order_in_posts_to_booking_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/booking",
        json={},
    )
    result = await orders.book_order_in(42)
    assert result == {}
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_book_order_in_sends_delivery_note_number(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/booking?deliveryNoteNumber=DN-1",
        json={},
    )
    await orders.book_order_in(42, delivery_note_number="DN-1")
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_get_contact_wish_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/contactWish",
        json={"text": "Please gift-wrap"},
    )
    result = await orders.get_contact_wish(42)
    assert result["text"] == "Please gift-wrap"


async def test_update_order_currency_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/currency",
        json={"id": 42, "statusId": 5.0},
    )
    result = await orders.update_order_currency(
        42, {"currency": "EUR", "exchangeRate": 1.0}
    )
    assert result["id"] == 42

