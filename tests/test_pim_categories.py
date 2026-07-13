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


async def test_list_category_branches(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/branches",
        json={"entries": [{"categoryId": 5, "branch": [1, 2, 5]}], "totalsCount": 1},
    )
    result = await pim.list_category_branches()
    assert result["totalsCount"] == 1


async def test_list_category_clients(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/clients?categoryId=5&plentyId=1",
        json={"entries": [{"categoryId": 5, "plentyId": 1}], "totalsCount": 1},
    )
    result = await pim.list_category_clients(category_id=5, plenty_id=1)
    assert result["totalsCount"] == 1


async def test_list_category_details(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/details?categoryId=5&lang=en",
        json={"entries": [{"categoryId": 5, "lang": "en", "name": "Shoes"}], "totalsCount": 1},
    )
    result = await pim.list_category_details(category_id=5, lang="en")
    assert result["entries"][0]["name"] == "Shoes"


async def test_list_category_properties(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/categories/properties?categoryId=5",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_category_properties(category_id=5)
    assert result["totalsCount"] == 0
