import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.pim import PimModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def pim(session):
    return PimModule(session)


async def test_pim_module_repr(pim):
    assert repr(pim) == "<PimModule /rest/pim>"


async def test_list_variations_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"entries": [{"id": 1}, {"id": 2}], "totalsCount": 2},
    )
    result = await pim.list_variations()
    assert result["totalsCount"] == 2


async def test_list_variations_with_filters_and_with(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations?isActive=true&with=base%2Cbarcodes",
        json={"entries": [{"id": 5}], "totalsCount": 1},
    )
    result = await pim.list_variations(
        filters={"isActive": "true"},
        with_=["base", "barcodes"],
    )
    assert result["entries"][0]["id"] == 5


async def test_paginate_variations_yields_all_across_cursors(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll",
        json={"entries": [{"id": 10}, {"id": 11}], "cursor": "abc123"},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?cursor=abc123",
        json={"entries": [{"id": 12}], "cursor": None},
    )
    results = [v async for v in pim.paginate_variations()]
    assert [r["id"] for r in results] == [10, 11, 12]


async def test_paginate_variations_stops_on_empty_entries(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll",
        json={"entries": [], "cursor": None},
    )
    results = [v async for v in pim.paginate_variations()]
    assert results == []


async def test_paginate_variations_preserves_filters_across_cursors(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?isActive=true&with=base",
        json={"entries": [{"id": 20}], "cursor": "tok99"},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?isActive=true&with=base&cursor=tok99",
        json={"entries": [{"id": 21}], "cursor": None},
    )
    results = [
        v async for v in pim.paginate_variations(
            filters={"isActive": "true"}, with_=["base"]
        )
    ]
    assert [r["id"] for r in results] == [20, 21]


async def test_update_variation_bases_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/bases",
        json={"updated": 1},
    )
    result = await pim.update_variation_bases([{"id": 7, "isActive": True}])
    assert result["updated"] == 1


async def test_list_categories_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories",
        json={"entries": [{"id": 1, "type": "item"}], "totalsCount": 1},
    )
    result = await pim.list_categories()
    assert result["totalsCount"] == 1


async def test_list_categories_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories?type=item&level=1",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_categories(type_="item", level=1)
    assert result["totalsCount"] == 0


async def test_get_category(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/99",
        json={"id": 99, "type": "item"},
    )
    result = await pim.get_category(99)
    assert result["id"] == 99


async def test_list_attributes_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"entries": [{"id": 3, "backendName": "Colour"}], "totalsCount": 1},
    )
    result = await pim.list_attributes()
    assert result["entries"][0]["backendName"] == "Colour"


async def test_list_attributes_with_backend_name(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes?backendName=Size",
        json={"entries": [{"id": 4}], "totalsCount": 1},
    )
    result = await pim.list_attributes(backend_name="Size")
    assert result["entries"][0]["id"] == 4


async def test_get_attribute(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/3",
        json={"id": 3, "backendName": "Colour"},
    )
    result = await pim.get_attribute(3)
    assert result["backendName"] == "Colour"


async def test_list_sales_prices_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"entries": [{"id": 1, "type": "default"}], "totalsCount": 1},
    )
    result = await pim.list_sales_prices()
    assert result["totalsCount"] == 1


async def test_get_sales_price(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/sales_prices/1",
        json={"id": 1, "type": "default", "currency": "EUR"},
    )
    result = await pim.get_sales_price(1)
    assert result["currency"] == "EUR"


async def test_create_variations_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"created": 1},
    )
    result = await pim.create_variations([{"id": 1, "base": {"itemId": 42}}])
    assert result["created"] == 1


async def test_delete_variations_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"deleted": 2},
    )
    result = await pim.delete_variations([1, 2])
    assert result["deleted"] == 2
