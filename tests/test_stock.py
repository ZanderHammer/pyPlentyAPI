import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.stock import StockModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def stock(session):
    return StockModule(session)


async def test_get_by_warehouse_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/1/items?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"variationId": 5}]},
    )
    result = await stock.get_by_warehouse(warehouse_id=1)
    assert result["entries"][0]["variationId"] == 5


async def test_get_by_warehouse_sends_pagination_params(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/2/items?page=2&itemsPerPage=10",
        json={"page": 2, "totalsCount": 20, "isLastPage": True, "entries": []},
    )
    result = await stock.get_by_warehouse(warehouse_id=2, page=2, items_per_page=10)
    assert result["page"] == 2


async def test_correct_puts_to_correction_url(httpx_mock, stock):
    payload = {"variationId": 5, "quantity": 10, "reasonId": 301, "warehouseLocationId": 0}
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/stock/warehouses/1/stock/correction",
        json={"success": True},
    )
    result = await stock.correct(warehouse_id=1, data=payload)
    assert result == {"success": True}


async def test_paginate_stock_yields_all_items(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/1/items?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"variationId": 1}, {"variationId": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stock/warehouses/1/items?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"variationId": 3}],
        },
    )
    results = [s async for s in stock.paginate_stock(warehouse_id=1, items_per_page=2)]
    assert [r["variationId"] for r in results] == [1, 2, 3]
