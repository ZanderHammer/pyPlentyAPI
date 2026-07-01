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
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"variationId": 5}]},
    )
    result = await stock.get_by_warehouse(warehouse_id=1)
    assert result["entries"][0]["variationId"] == 5


async def test_get_by_warehouse_sends_pagination_params(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/2/stock?page=2&itemsPerPage=10",
        json={"page": 2, "totalsCount": 20, "isLastPage": True, "entries": []},
    )
    result = await stock.get_by_warehouse(warehouse_id=2, page=2, items_per_page=10)
    assert result["page"] == 2


async def test_correct_puts_to_correction_url(httpx_mock, stock):
    payload = {"variationId": 5, "quantity": 10, "reasonId": 301, "storageLocationId": 0}
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock/correction",
        json={"success": True},
    )
    result = await stock.correct(warehouse_id=1, data=payload)
    assert result == {"success": True}


async def test_correct_accepts_quantity_only_payload(httpx_mock, stock):
    """`quantity` is the only field the API requires; everything else is optional."""
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock/correction",
        json={"success": True},
    )
    result = await stock.correct(warehouse_id=1, data={"quantity": 10})
    assert result == {"success": True}


async def test_paginate_stock_yields_all_items(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"variationId": 1}, {"variationId": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/stock?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"variationId": 3}],
        },
    )
    results = [s async for s in stock.paginate_stock(warehouse_id=1, items_per_page=2)]
    assert [r["variationId"] for r in results] == [1, 2, 3]


# -- Stock (global) -----------------------------------------------------------


async def test_list_stock_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"variationId": 5}]},
    )
    result = await stock.list_stock()
    assert result["entries"][0]["variationId"] == 5


async def test_list_stock_sends_filters(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock?variationId=5&page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": []},
    )
    result = await stock.list_stock(filters={"variationId": 5})
    assert result["page"] == 1


async def test_paginate_all_stock_yields_all_items(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"variationId": 1}, {"variationId": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock?page=2&itemsPerPage=2",
        json={"page": 2, "totalsCount": 3, "isLastPage": True, "entries": [{"variationId": 3}]},
    )
    results = [s async for s in stock.paginate_all_stock(items_per_page=2)]
    assert [r["variationId"] for r in results] == [1, 2, 3]


async def test_list_stock_archive_years_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock/archives",
        json=[2024, 2025, 2026],
    )
    result = await stock.list_stock_archive_years()
    assert result == [2024, 2025, 2026]


async def test_list_stock_by_type_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock/types/sales?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"variationId": 5}]},
    )
    result = await stock.list_stock_by_type("sales")
    assert result["entries"][0]["variationId"] == 5


async def test_paginate_stock_by_type_yields_all_items(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock/types/sales?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 2,
            "isLastPage": False,
            "entries": [{"variationId": 1}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/stock/types/sales?page=2&itemsPerPage=2",
        json={"page": 2, "totalsCount": 2, "isLastPage": True, "entries": [{"variationId": 2}]},
    )
    results = [s async for s in stock.paginate_stock_by_type("sales", items_per_page=2)]
    assert [r["variationId"] for r in results] == [1, 2]


async def test_redistribute_stock_puts_to_redistribute_url(httpx_mock, stock):
    payload = {"currentWarehouseId": 1, "newWarehouseId": 2, "quantity": 5}
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/stockmanagement/stock/redistribute",
        json={"success": True},
    )
    result = await stock.redistribute_stock(data=payload)
    assert result == {"success": True}


# -- Warehouses -----------------------------------------------------------


async def test_list_warehouses_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses",
        json={"entries": [{"id": 1, "name": "Main"}]},
    )
    result = await stock.list_warehouses()
    assert result["entries"][0]["id"] == 1


async def test_create_warehouse_posts_payload(httpx_mock, stock):
    payload = {"name": "Main", "typeId": 0, "logisticsType": "own"}
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses",
        json={"id": 1, "name": "Main"},
    )
    result = await stock.create_warehouse(data=payload)
    assert result["id"] == 1


async def test_get_warehouse_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1",
        json={"id": 1, "name": "Main"},
    )
    result = await stock.get_warehouse(warehouse_id=1)
    assert result["id"] == 1


async def test_get_storage_location_calls_correct_url(httpx_mock, stock):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/stockmanagement/warehouses/1/management/storageLocations/7",
        json={"id": 7, "warehouseId": 1},
    )
    result = await stock.get_storage_location(warehouse_id=1, storage_location_id=7)
    assert result["id"] == 7

