import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.pim import PimModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def pim(session):
    return PimModule(session)


async def test_pim_module_repr(pim):
    assert repr(pim) == "<PimModule /rest/pim>"


async def test_list_variations_no_filters(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"entries": [{"id": 1}, {"id": 2}], "totalsCount": 2},
    )
    result = await pim.list_variations()
    assert result["totalsCount"] == 2


async def test_list_variations_with_filters_and_with(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations?isActive=true&with=base%2Cbarcodes",
        json={"entries": [{"id": 5}], "totalsCount": 1},
    )
    result = await pim.list_variations(
        filters={"isActive": "true"},
        with_=["base", "barcodes"],
    )
    assert result["entries"][0]["id"] == 5


async def test_paginate_variations_yields_all_across_cursors(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll",
        json={"entries": [{"id": 10}, {"id": 11}], "cursor": "abc123"},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?cursor=abc123",
        json={"entries": [{"id": 12}], "cursor": None},
    )
    results = [v async for v in pim.paginate_variations()]
    assert [r["id"] for r in results] == [10, 11, 12]


async def test_paginate_variations_stops_on_empty_entries(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll",
        json={"entries": [], "cursor": None},
    )
    results = [v async for v in pim.paginate_variations()]
    assert results == []


async def test_paginate_variations_preserves_filters_across_cursors(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?isActive=true&with=base",
        json={"entries": [{"id": 20}], "cursor": "tok99"},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/variations/scroll?isActive=true&with=base&cursor=tok99",
        json={"entries": [{"id": 21}], "cursor": None},
    )
    results = [
        v async for v in pim.paginate_variations(
            filters={"isActive": "true"}, with_=["base"]
        )
    ]
    assert [r["id"] for r in results] == [20, 21]


async def test_update_variation_bases_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations/bases",
        json={"updated": 1},
    )
    result = await pim.update_variation_bases([{"id": 7, "isActive": True}])
    assert result["updated"] == 1


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


async def test_create_variations_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"created": 1},
    )
    result = await pim.create_variations([{"id": 1, "base": {"itemId": 42}}])
    assert result["created"] == 1


async def test_delete_variations_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/variations",
        json={"deleted": 2},
    )
    result = await pim.delete_variations([1, 2])
    assert result["deleted"] == 2


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
