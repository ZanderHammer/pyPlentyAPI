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


async def test_list_attribute_names_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"entries": [{"attributeId": 3, "lang": "en", "name": "Colour"}], "totalsCount": 1},
    )
    result = await pim.list_attribute_names()
    assert result["totalsCount"] == 1


async def test_list_attribute_names_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/names?attributeId=3&lang=en",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_attribute_names(attribute_id=3, lang="en")
    assert result["totalsCount"] == 0


async def test_create_attribute_names_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"created": 1},
    )
    result = await pim.create_attribute_names(
        [{"attributeId": 3, "lang": "en", "name": "Colour"}]
    )
    assert result["created"] == 1


async def test_update_attribute_names_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"updated": 1},
    )
    result = await pim.update_attribute_names(
        [{"attributeId": 3, "lang": "en", "name": "Color"}]
    )
    assert result["updated"] == 1


async def test_delete_attribute_names_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes/names",
        json={"deleted": 1},
    )
    result = await pim.delete_attribute_names([9])
    assert result["deleted"] == 1
