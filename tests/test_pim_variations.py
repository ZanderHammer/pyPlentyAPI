import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.pim import PimModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
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
