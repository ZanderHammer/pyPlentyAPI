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


async def test_create_sales_prices_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"created": 1},
    )
    result = await pim.create_sales_prices(
        [{"type": "specialOffer", "position": 3, "isCustomerPrice": False}]
    )
    assert result["created"] == 1


async def test_update_sales_prices_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"updated": 1},
    )
    result = await pim.update_sales_prices([{"id": 1, "position": 2}])
    assert result["updated"] == 1


async def test_delete_sales_prices_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/sales_prices",
        json={"deleted": 1},
    )
    result = await pim.delete_sales_prices([1])
    assert result["deleted"] == 1
