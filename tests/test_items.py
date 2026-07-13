import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.items import ItemsModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def items(session):
    return ItemsModule(session)


async def test_get_calls_correct_url(httpx_mock, items):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items/10",
        json={"id": 10, "position": 0},
    )
    result = await items.get(10)
    assert result["id"] == 10


async def test_list_sends_pagination_params(httpx_mock, items):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items?page=3&itemsPerPage=10",
        json={"page": 3, "totalsCount": 30, "isLastPage": True, "entries": []},
    )
    result = await items.list(page=3, items_per_page=10)
    assert result["page"] == 3


async def test_create_posts_data(httpx_mock, items):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/items",
        json={"id": 55},
    )
    result = await items.create({"vatId": 0, "producingCountryId": 1})
    assert result["id"] == 55


async def test_update_puts_to_item_url(httpx_mock, items):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/items/10",
        json={"id": 10, "position": 1},
    )
    result = await items.update(10, {"position": 1})
    assert result["position"] == 1


async def test_paginate_items_yields_all_items(httpx_mock, items):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 10}, {"id": 11}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/items?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 12}],
        },
    )
    results = [i async for i in items.paginate_items(items_per_page=2)]
    assert [r["id"] for r in results] == [10, 11, 12]
