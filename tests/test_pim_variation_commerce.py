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


async def test_update_variation_clients_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/clients",
        json={"updated": 1},
    )
    result = await pim.update_variation_clients([{"variationId": 7, "plentyId": 1}])
    assert result["updated"] == 1


async def test_delete_variation_clients_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/clients",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_clients([1])
    assert result["deleted"] == 1


async def test_update_variation_images_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/images",
        json={"updated": 1},
    )
    result = await pim.update_variation_images([{"variationId": 7, "imageId": 9}])
    assert result["updated"] == 1


async def test_delete_variation_images_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/images",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_images([9])
    assert result["deleted"] == 1


async def test_update_variation_markets_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/markets",
        json={"updated": 1},
    )
    result = await pim.update_variation_markets([{"variationId": 7, "marketId": 2}])
    assert result["updated"] == 1


async def test_delete_variation_markets_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/markets",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_markets([2])
    assert result["deleted"] == 1


async def test_update_variation_sales_prices_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/sales_prices",
        json={"updated": 1},
    )
    result = await pim.update_variation_sales_prices(
        [{"variationId": 7, "salesPriceId": 1, "price": 19.99}]
    )
    assert result["updated"] == 1


async def test_delete_variation_sales_prices_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/sales_prices",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_sales_prices([1])
    assert result["deleted"] == 1


async def test_update_variation_supplier_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/supplier",
        json={"updated": 1},
    )
    result = await pim.update_variation_supplier(
        [{"variationId": 7, "supplierId": 4, "supplierPartNumber": "SUP-9"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_supplier_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/supplier",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_supplier([4])
    assert result["deleted"] == 1


async def test_update_variation_warehouses_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/warehouses",
        json={"updated": 1},
    )
    result = await pim.update_variation_warehouses(
        [{"variationId": 7, "warehouseId": 1, "stockManagementActive": True}]
    )
    assert result["updated"] == 1


async def test_delete_variation_warehouses_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/warehouses",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_warehouses([1])
    assert result["deleted"] == 1
