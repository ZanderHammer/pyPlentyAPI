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


async def test_update_variation_additional_skus_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/additional_skus",
        json={"updated": 1},
    )
    result = await pim.update_variation_additional_skus(
        [{"variationId": 7, "referrerId": 1, "sku": "ABC-1"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_additional_skus_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/additional_skus",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_additional_skus([10])
    assert result["deleted"] == 1


async def test_update_variation_barcodes_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/barcodes",
        json={"updated": 1},
    )
    result = await pim.update_variation_barcodes([{"variationId": 7, "barcodeId": 3}])
    assert result["updated"] == 1


async def test_delete_variation_barcodes_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/barcodes",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_barcodes([3])
    assert result["deleted"] == 1


async def test_update_variation_bundle_components_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/bundle_components",
        json={"updated": 1},
    )
    result = await pim.update_variation_bundle_components(
        [{"variationId": 7, "componentVariationId": 8, "componentQuantity": 2}]
    )
    assert result["updated"] == 1


async def test_delete_variation_bundle_components_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/bundle_components",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_bundle_components([8])
    assert result["deleted"] == 1


async def test_update_variation_market_ident_numbers_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/market_ident_numbers",
        json={"updated": 1},
    )
    result = await pim.update_variation_market_ident_numbers(
        [{"variationId": 7, "marketIdentNumberType": "ean", "marketIdentNumber": "4006381333931"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_market_ident_numbers_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/market_ident_numbers",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_market_ident_numbers([4])
    assert result["deleted"] == 1


async def test_update_variation_skus_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/skus",
        json={"updated": 1},
    )
    result = await pim.update_variation_skus(
        [{"variationId": 7, "marketId": 2, "sku": "MKT-SKU-1"}]
    )
    assert result["updated"] == 1


async def test_delete_variation_skus_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations/skus",
        json={"deleted": 1},
    )
    result = await pim.delete_variation_skus([6])
    assert result["deleted"] == 1
