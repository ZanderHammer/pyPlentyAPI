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


async def test_get_item_attributes(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/items/42/attributes",
        json=[{"attributeId": 3, "backendName": "Colour"}],
    )
    result = await pim.get_item_attributes(42)
    assert result[0]["attributeId"] == 3


async def test_get_item_combinations(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/items/42/combinations",
        json=[{"attributeValueSetIds": [10, 20]}],
    )
    result = await pim.get_item_combinations(42)
    assert result[0]["attributeValueSetIds"] == [10, 20]


async def test_list_amazon_product_types(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/amazon-product-types",
        json={"entries": [{"productType": "SHOES"}]},
    )
    result = await pim.list_amazon_product_types()
    assert result["entries"][0]["productType"] == "SHOES"
