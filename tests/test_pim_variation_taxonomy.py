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


async def test_update_variation_categories_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/categories",
        json={"updated": 1},
    )
    result = await pim.update_variation_categories([{"variationId": 7, "categoryId": 5}])
    assert result["updated"] == 1


async def test_delete_variation_categories_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/categories",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_categories([5])
    assert result["deleted"] == 1


async def test_update_variation_comments_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/comments",
        json={"updated": 1},
    )
    result = await pim.update_variation_comments(
        [{"variationId": 7, "text": "Check supplier lead time"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_comments_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/comments",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_comments([12])
    assert result["deleted"] == 1


async def test_update_variation_default_categories_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/default_categories",
        json={"updated": 1},
    )
    result = await pim.update_variation_default_categories(
        [{"variationId": 7, "categoryId": 5, "plentyId": 1}]
    )
    assert result["updated"] == 1


async def test_delete_variation_default_categories_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/default_categories",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_default_categories([5])
    assert result["deleted"] == 1


async def test_update_variation_properties_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/properties",
        json={"updated": 1},
    )
    result = await pim.update_variation_properties(
        [{"variationId": 7, "propertyId": 3, "propertyValue": "Cotton"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_properties_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/properties",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_properties([3])
    assert result["deleted"] == 1


async def test_update_variation_tags_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/tags",
        json={"updated": 1},
    )
    result = await pim.update_variation_tags([{"variationId": 7, "tagId": 11}])
    assert result["updated"] == 1


async def test_delete_variation_tags_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/tags",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_tags([11])
    assert result["deleted"] == 1
