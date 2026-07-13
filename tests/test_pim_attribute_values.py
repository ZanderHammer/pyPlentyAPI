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


async def test_list_attribute_values_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"entries": [{"id": 10, "attributeId": 3, "backendName": "Red"}], "totalsCount": 1},
    )
    result = await pim.list_attribute_values()
    assert result["totalsCount"] == 1


async def test_list_attribute_values_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values?attributeId=3",
        json={"entries": [{"id": 10}], "totalsCount": 1},
    )
    result = await pim.list_attribute_values(attribute_id=3)
    assert result["entries"][0]["id"] == 10


async def test_create_attribute_values_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"created": 1},
    )
    result = await pim.create_attribute_values(
        [{"attributeId": 3, "backendName": "Red", "position": 1}]
    )
    assert result["created"] == 1


async def test_update_attribute_values_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"updated": 1},
    )
    result = await pim.update_attribute_values([{"id": 10, "position": 2}])
    assert result["updated"] == 1


async def test_delete_attribute_values_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes/values",
        json={"deleted": 1},
    )
    result = await pim.delete_attribute_values([10])
    assert result["deleted"] == 1


async def test_get_attribute_value(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values/10",
        json={"id": 10, "attributeId": 3, "backendName": "Red"},
    )
    result = await pim.get_attribute_value(10)
    assert result["backendName"] == "Red"


async def test_list_attribute_value_names_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"entries": [{"valueId": 10, "lang": "en", "name": "Red"}], "totalsCount": 1},
    )
    result = await pim.list_attribute_value_names()
    assert result["totalsCount"] == 1


async def test_list_attribute_value_names_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/attributes/values/names?valueId=10&lang=en",
        json={"entries": [], "totalsCount": 0},
    )
    result = await pim.list_attribute_value_names(value_id=10, lang="en")
    assert result["totalsCount"] == 0


async def test_create_attribute_value_names_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"created": 1},
    )
    result = await pim.create_attribute_value_names(
        [{"valueId": 10, "lang": "en", "name": "Red"}]
    )
    assert result["created"] == 1


async def test_update_attribute_value_names_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"updated": 1},
    )
    result = await pim.update_attribute_value_names(
        [{"valueId": 10, "lang": "en", "name": "Crimson"}]
    )
    assert result["updated"] == 1


async def test_delete_attribute_value_names_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/attributes/values/names",
        json={"deleted": 1},
    )
    result = await pim.delete_attribute_value_names([21])
    assert result["deleted"] == 1
