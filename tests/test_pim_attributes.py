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


async def test_create_attributes_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"created": 1},
    )
    result = await pim.create_attributes([{"backendName": "Material"}])
    assert result["created"] == 1


async def test_update_attributes_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"updated": 1},
    )
    result = await pim.update_attributes([{"id": 3, "position": 2}])
    assert result["updated"] == 1


async def test_delete_attributes_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes",
        json={"deleted": 1},
    )
    result = await pim.delete_attributes([3])
    assert result["deleted"] == 1
