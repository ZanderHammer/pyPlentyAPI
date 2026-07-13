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


async def test_list_barcodes_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"entries": [{"id": 1, "type": "EAN13"}], "totalsCount": 1},
    )
    result = await pim.list_barcodes()
    assert result["totalsCount"] == 1


async def test_list_barcodes_with_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes?type=EAN13",
        json={"entries": [{"id": 1, "type": "EAN13"}], "totalsCount": 1},
    )
    result = await pim.list_barcodes(type_="EAN13")
    assert result["entries"][0]["id"] == 1


async def test_create_barcodes_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"created": 1},
    )
    result = await pim.create_barcodes([{"name": "EAN-13", "type": "EAN13"}])
    assert result["created"] == 1


async def test_update_barcodes_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"updated": 1},
    )
    result = await pim.update_barcodes([{"id": 1, "name": "EAN-13 (updated)"}])
    assert result["updated"] == 1


async def test_delete_barcodes_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/barcodes",
        json={"deleted": 1},
    )
    result = await pim.delete_barcodes([1])
    assert result["deleted"] == 1


async def test_list_barcode_duplicates(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes/duplicates",
        json={"entries": {"4006381333931": [10, 11]}},
    )
    result = await pim.list_barcode_duplicates()
    assert "4006381333931" in result["entries"]


async def test_count_barcode_duplicates(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes/duplicates/count",
        json={"count": 2},
    )
    result = await pim.count_barcode_duplicates()
    assert result["count"] == 2


async def test_get_barcode_duplicate_settings(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/barcodes/duplicates/settings",
        json=[{"barcodeType": "EAN13", "checkForDuplicates": True}],
    )
    result = await pim.get_barcode_duplicate_settings()
    assert result[0]["barcodeType"] == "EAN13"
