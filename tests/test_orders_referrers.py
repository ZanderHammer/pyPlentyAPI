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


async def test_list_referrers_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers",
        json=[{"id": 1, "name": "Google", "isEditable": True}],
    )
    result = await orders.list_referrers()
    assert result[0]["name"] == "Google"


async def test_list_referrers_sends_columns(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers?columns=id%2Cname",
        json=[],
    )
    await orders.list_referrers(columns=["id", "name"])


async def test_get_next_free_referrer_id_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/next_free_main",
        json={"data": 5},
    )
    result = await orders.get_next_free_referrer_id()
    assert result["data"] == 5


async def test_search_referrers_defaults_to_page_1_and_20(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/search?page=1&itemsPerPage=20",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search_referrers()
    assert result["page"] == 1


async def test_paginate_referrers_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/search?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/search?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [r async for r in orders.paginate_referrers(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_create_referrer_sends_data_values(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/referrers/1?data=name%3AGoogle%2CisFilterable%3Atrue",
        json={"id": 2, "name": "Google"},
    )
    result = await orders.create_referrer(
        1, values=["name:Google", "isFilterable:true"]
    )
    assert result["id"] == 2


async def test_delete_referrer_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/referrers/2",
        json={},
    )
    result = await orders.delete_referrer(2)
    assert result == {}


async def test_get_referrer_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/referrers/2",
        json={"id": 2, "name": "Google"},
    )
    result = await orders.get_referrer(2)
    assert result["name"] == "Google"


async def test_update_referrer_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/referrers/2",
        json={"id": 2, "name": "Google Ads"},
    )
    result = await orders.update_referrer(2, {"name": "Google Ads"})
    assert result["name"] == "Google Ads"
