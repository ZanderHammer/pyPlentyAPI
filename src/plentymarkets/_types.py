"""TypedDict definitions for PlentyMarkets API request payloads.

Import these when constructing payloads to get IDE autocomplete and
static type checking. At runtime they are plain dicts — no overhead.

Example::

    from plentymarkets._types import OrderCreatePayload

    payload: OrderCreatePayload = {"typeId": 1, "plentyId": 12345}
    order = await client.orders.create(payload)
"""

from typing import Any, NotRequired, Required, TypedDict


# ---------------------------------------------------------------------------
# Orders  (/rest/orders)
# ---------------------------------------------------------------------------


class OrderCreatePayload(TypedDict, total=False):
    """Payload for :meth:`OrdersModule.create` (``POST /rest/orders``).

    Keys:
        typeId: Order type ID. **Required.**
            1=sales order, 2=delivery order, 3=returns, 4=credit note,
            5=warranty, 6=repair, 7=offer, 8=advance order, 9=multi-order.
        plentyId: Client (store) ID the order belongs to. **Required.**
        statusId: Numeric order status ID (e.g. ``3.0`` = waiting for payment,
            ``5.0`` = cleared for shipping). Decimal part is used for
            sub-statuses.
        ownerId: User ID of the order owner.
        lockStatus: Lock state of the order. ``"unlocked"`` or ``"locked"``.
        orderItems: List of order item dicts. Each item should include
            ``typeId``, ``itemVariationId``, ``quantity``, and ``amounts``.
        properties: List of order property dicts, each with ``typeId`` and
            ``value``.
        addressRelations: List of address relation dicts. Each entry requires
            ``typeId`` (1=billing, 2=delivery) and ``addressId``.
        relations: List of relation dicts, each with ``referenceType``,
            ``referenceId``, and ``relation``.
    """

    typeId: Required[int]
    plentyId: Required[int]
    statusId: NotRequired[float]
    ownerId: NotRequired[int]
    lockStatus: NotRequired[str]
    orderItems: NotRequired[list[dict]]
    properties: NotRequired[list[dict]]
    addressRelations: NotRequired[list[dict]]
    relations: NotRequired[list[dict]]


# ---------------------------------------------------------------------------
# Items  (/rest/items)
# ---------------------------------------------------------------------------


class ItemCreatePayload(TypedDict, total=False):
    """Payload for :meth:`ItemsModule.create` (``POST /rest/items``).

    Keys:
        position: Display position in item lists.
        stockType: Stock type. 0=stocked, 1=production, 2=colli,
            3=special order.
        storeSpecial: Special shop display flag. 0=none, 1=special offer,
            2=new item, 3=top item.
        ownerId: User ID of the item owner.
        manufacturerId: Manufacturer ID.
        producingCountryId: Country of origin ID (ISO country ID).
        vatId: VAT configuration ID.
        condition: Item condition. 0=new, 1=used, 2=refurbished,
            3=new with original packaging, 4=new with defects, 5=B-stock.
        conditionApi: Condition value exposed via marketplace APIs
            (0=new, 1=used, 2=not specified, 3=defective, 4=refurbished).
        customsTariffNumber: Harmonized System (HS) customs tariff code.
        revenueAccount: Revenue account number for accounting.
        couponRestriction: 0=allow all, 1=forbid all, 2=allow coupons only.
        isSubscribable: Whether the item supports subscription ordering.
        isShippingPackage: Whether the item ships as a package unit.
        flagOne: Item flag 1 (shop-specific integer tag).
        flagTwo: Item flag 2 (shop-specific integer tag).
        ageRestriction: Age restriction in years. Common values: 0, 6, 12,
            14, 16, 18, 50.
        itemType: Item type string. ``"Default"``, ``"Bundle"``,
            or ``"BundleItem"``.
        amazonFbaPlatform: Amazon FBA platform. 0=none, 1=AMAZON_EU,
            2=AMAZON_FE, 3=AMAZON_NA.
        isShippableByAmazon: Whether Amazon is allowed to fulfil this item.
        amazonProductType: Amazon browse-node / product type number.
        ebayPresetId: eBay listing preset ID.
        ebayCategory: Primary eBay category ID.
        ebayCategory2: Secondary eBay category ID.
        rakutenCategoryId: Rakuten product category ID.
        variations: List of variation dicts. Provide at least one variation
            with ``isMain: true`` to create a usable item.
    """

    position: NotRequired[int]
    stockType: NotRequired[int]
    storeSpecial: NotRequired[int]
    ownerId: NotRequired[int]
    manufacturerId: NotRequired[int]
    producingCountryId: NotRequired[int]
    vatId: NotRequired[int]
    condition: NotRequired[int]
    conditionApi: NotRequired[int]
    customsTariffNumber: NotRequired[str]
    revenueAccount: NotRequired[int]
    couponRestriction: NotRequired[int]
    isSubscribable: NotRequired[bool]
    isShippingPackage: NotRequired[bool]
    flagOne: NotRequired[int]
    flagTwo: NotRequired[int]
    ageRestriction: NotRequired[int]
    itemType: NotRequired[str]
    amazonFbaPlatform: NotRequired[int]
    isShippableByAmazon: NotRequired[bool]
    amazonProductType: NotRequired[int]
    ebayPresetId: NotRequired[int]
    ebayCategory: NotRequired[int]
    ebayCategory2: NotRequired[int]
    rakutenCategoryId: NotRequired[int]
    variations: NotRequired[list[dict]]


class ItemUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`ItemsModule.update` (``PUT /rest/items/{itemId}``).

    All keys are optional — only the fields provided are updated.

    Keys:
        position: Display position in item lists.
        stockType: Stock type. 0=stocked, 1=production, 2=colli,
            3=special order.
        storeSpecial: Special shop display flag.
        ownerId: User ID of the item owner.
        manufacturerId: Manufacturer ID.
        producingCountryId: Country of origin ID.
        vatId: VAT configuration ID.
        condition: Item condition (0–5).
        conditionApi: Marketplace condition value (0–4).
        customsTariffNumber: HS / customs tariff code.
        revenueAccount: Revenue account number.
        couponRestriction: 0=allow all, 1=forbid all, 2=allow coupons only.
        isSubscribable: Whether the item supports subscription ordering.
        isShippingPackage: Whether the item ships as a package unit.
        flagOne: Item flag 1.
        flagTwo: Item flag 2.
        ageRestriction: Age restriction in years.
        itemType: ``"Default"``, ``"Bundle"``, or ``"BundleItem"``.
        amazonFbaPlatform: 0=none, 1=AMAZON_EU, 2=AMAZON_FE, 3=AMAZON_NA.
        isShippableByAmazon: Whether Amazon can fulfil this item.
        amazonProductType: Amazon product type number.
        ebayPresetId: eBay listing preset ID.
        ebayCategory: Primary eBay category ID.
        ebayCategory2: Secondary eBay category ID.
        rakutenCategoryId: Rakuten product category ID.
    """

    position: NotRequired[int]
    stockType: NotRequired[int]
    storeSpecial: NotRequired[int]
    ownerId: NotRequired[int]
    manufacturerId: NotRequired[int]
    producingCountryId: NotRequired[int]
    vatId: NotRequired[int]
    condition: NotRequired[int]
    conditionApi: NotRequired[int]
    customsTariffNumber: NotRequired[str]
    revenueAccount: NotRequired[int]
    couponRestriction: NotRequired[int]
    isSubscribable: NotRequired[bool]
    isShippingPackage: NotRequired[bool]
    flagOne: NotRequired[int]
    flagTwo: NotRequired[int]
    ageRestriction: NotRequired[int]
    itemType: NotRequired[str]
    amazonFbaPlatform: NotRequired[int]
    isShippableByAmazon: NotRequired[bool]
    amazonProductType: NotRequired[int]
    ebayPresetId: NotRequired[int]
    ebayCategory: NotRequired[int]
    ebayCategory2: NotRequired[int]
    rakutenCategoryId: NotRequired[int]


# ---------------------------------------------------------------------------
# Stock  (/rest/stock/warehouses/{warehouseId}/stock/correction)
# ---------------------------------------------------------------------------


class StockCorrectionPayload(TypedDict):
    """Payload for :meth:`StockModule.correct`
    (``PUT /rest/stock/warehouses/{warehouseId}/stock/correction``).

    Keys:
        variationId: Variation ID whose stock should be corrected. **Required.**
        quantity: New absolute stock quantity after correction. **Required.**
            Positive values add stock; the API replaces the current level.
        reasonId: Correction reason ID. **Required.** Common values:
            301=stock correction, 304=incoming items, 305=outgoing items,
            309=returns.
        warehouseLocationId: Storage location ID within the warehouse.
            **Required.** Use ``0`` for the warehouse default location.
    """

    variationId: int
    quantity: float
    reasonId: int
    warehouseLocationId: int


# ---------------------------------------------------------------------------
# Contacts  (/rest/accounts/contacts)
# ---------------------------------------------------------------------------


class ContactCreatePayload(TypedDict, total=False):
    """Payload for :meth:`ContactsModule.create`
    (``POST /rest/accounts/contacts``).

    Keys:
        typeId: Contact type. 1=customer, 2=interested party, 3=sales rep,
            4=supplier, 5=manufacturer, 6=partner.
        referrerId: Sales referrer ID (float, links to the referrer table).
        title: Title or form of address string (e.g. ``"Dr."``).
        firstName: Contact first name.
        lastName: Contact last name.
        email: Primary e-mail address.
        gender: Gender string. ``"male"``, ``"female"``, or ``"diverse"``.
        lang: Two-letter ISO language code for the contact's preferred
            language (e.g. ``"de"``, ``"en"``).
        plentyId: Client (store) ID the contact belongs to.
        options: List of contact option dicts. Each option requires
            ``typeId`` (1=telephone, 2=email, 3=messenger, 4=marketplace),
            ``subTypeId``, ``value``, and ``priority``.
    """

    typeId: NotRequired[int]
    referrerId: NotRequired[float]
    title: NotRequired[str]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    email: NotRequired[str]
    gender: NotRequired[str]
    lang: NotRequired[str]
    plentyId: NotRequired[int]
    options: NotRequired[list[dict]]


class ContactUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`ContactsModule.update`
    (``PUT /rest/accounts/contacts/{contactId}``).

    All keys are optional — only the fields provided are updated.

    Keys:
        title: Title or form of address string.
        firstName: Contact first name.
        lastName: Contact last name.
        email: Primary e-mail address.
        gender: Gender string. ``"male"``, ``"female"``, or ``"diverse"``.
        lang: Two-letter ISO language code.
        options: List of contact option dicts (typeId, subTypeId, value,
            priority). Replaces all existing options of the provided types.
    """

    title: NotRequired[str]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    email: NotRequired[str]
    gender: NotRequired[str]
    lang: NotRequired[str]
    options: NotRequired[list[dict]]


# ---------------------------------------------------------------------------
# PIM  (/rest/pim/)
# ---------------------------------------------------------------------------


class VariationBaseUpdatePayload(TypedDict, total=False):
    """One entry in the list passed to :meth:`PimModule.update_variation_bases`
    (``PUT /rest/pim/variations/bases``).

    Keys:
        id: Variation ID to update. **Required.**
        number: Variation number / internal SKU string.
        isMain: Whether this is the item's main variation.
        isActive: Whether the variation is active and visible.
        model: Model identifier string shown in the back end.
        purchasePrice: Net purchase price used for margin calculations.
        vatId: VAT configuration ID.
        availabilityId: Availability level (1–10, maps to availability icons).
        weightG: Gross weight in grams.
        weightNetG: Net weight in grams.
        widthMM: Width in millimetres.
        lengthMM: Length in millimetres.
        heightMM: Height in millimetres.
        position: Display sort position within the item.
        stockLimitation: 0=no limit, 1=limited to net stock, 2=disabled.
        unitId: Unit ID (e.g. piece, litre).
        unitsContained: Quantity of base units within this variation unit.
        mainVariationId: ID of the item's main variation (set on child
            variations to declare the parent).
    """

    id: Required[int]
    number: NotRequired[str]
    isMain: NotRequired[bool]
    isActive: NotRequired[bool]
    model: NotRequired[str]
    purchasePrice: NotRequired[float]
    vatId: NotRequired[int]
    availabilityId: NotRequired[int]
    weightG: NotRequired[float]
    weightNetG: NotRequired[float]
    widthMM: NotRequired[float]
    lengthMM: NotRequired[float]
    heightMM: NotRequired[float]
    position: NotRequired[int]
    stockLimitation: NotRequired[int]
    unitId: NotRequired[int]
    unitsContained: NotRequired[int]
    mainVariationId: NotRequired[int]


class VariationCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_variations` (``PUT /rest/pim/variations``).

    Creates or fully replaces variations along with their nested related data
    in a single call. Prefer :meth:`PimModule.update_variation_bases` for
    simple base-field updates; use this payload when creating new variations
    or writing several related-data collections at once.

    Keys:
        id: Variation ID. Required when updating an existing variation;
            omit to create a new one.
        base: Base variation fields (see
            :class:`~plentymarkets._types.VariationBaseUpdatePayload`).
        additionalSkus: List of additional-SKU dicts (see
            :class:`~plentymarkets._types.VariationAdditionalSkuPayload`).
        attributeValues: List of attribute-value link dicts, each with
            ``attributeId`` and ``valueId``.
        barcodes: List of barcode link dicts (see
            :class:`~plentymarkets._types.VariationBarcodePayload`).
        bundleComponents: List of bundle component dicts (see
            :class:`~plentymarkets._types.VariationBundleComponentPayload`).
        categories: List of category link dicts (see
            :class:`~plentymarkets._types.VariationCategoryPayload`).
        clients: List of client visibility dicts (see
            :class:`~plentymarkets._types.VariationClientPayload`).
        defaultCategories: List of default-category dicts (see
            :class:`~plentymarkets._types.VariationDefaultCategoryPayload`).
        images: List of image link dicts (see
            :class:`~plentymarkets._types.VariationImagePayload`).
        markets: List of market availability dicts (see
            :class:`~plentymarkets._types.VariationMarketPayload`).
        marketIdentNumbers: List of MIN dicts (see
            :class:`~plentymarkets._types.VariationMarketIdentNumberPayload`).
        salesPrices: List of sales price link dicts (see
            :class:`~plentymarkets._types.VariationSalesPricePayload`).
        skus: List of marketplace SKU dicts (see
            :class:`~plentymarkets._types.VariationSkuPayload`).
        supplier: List of supplier link dicts (see
            :class:`~plentymarkets._types.VariationSupplierPayload`).
        warehouses: List of warehouse stock dicts (see
            :class:`~plentymarkets._types.VariationWarehousePayload`).
        properties: List of property dicts (see
            :class:`~plentymarkets._types.VariationPropertyPayload`).
        tags: List of tag link dicts (see
            :class:`~plentymarkets._types.VariationTagPayload`).
        comments: List of comment dicts (see
            :class:`~plentymarkets._types.VariationCommentPayload`).
        inheritance: List of inheritance-configuration dicts controlling
            which fields a child variation inherits from its parent.
        unit: List with a single unit-configuration dict, e.g.
            ``{"unitId": 1, "content": 1}``.
    """

    id: NotRequired[int]
    base: NotRequired[dict[str, Any]]
    additionalSkus: NotRequired[list[dict[str, Any]]]
    attributeValues: NotRequired[list[dict[str, Any]]]
    barcodes: NotRequired[list[dict[str, Any]]]
    bundleComponents: NotRequired[list[dict[str, Any]]]
    categories: NotRequired[list[dict[str, Any]]]
    clients: NotRequired[list[dict[str, Any]]]
    defaultCategories: NotRequired[list[dict[str, Any]]]
    images: NotRequired[list[dict[str, Any]]]
    markets: NotRequired[list[dict[str, Any]]]
    marketIdentNumbers: NotRequired[list[dict[str, Any]]]
    salesPrices: NotRequired[list[dict[str, Any]]]
    skus: NotRequired[list[dict[str, Any]]]
    supplier: NotRequired[list[dict[str, Any]]]
    warehouses: NotRequired[list[dict[str, Any]]]
    properties: NotRequired[list[dict[str, Any]]]
    tags: NotRequired[list[dict[str, Any]]]
    comments: NotRequired[list[dict[str, Any]]]
    inheritance: NotRequired[list[dict[str, Any]]]
    unit: NotRequired[list[dict[str, Any]]]


class VariationAdditionalSkuPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_additional_skus`
    (``PUT /rest/pim/variations/additional_skus``).

    Keys:
        variationId: Variation ID to attach the SKU to. **Required.**
        id: Additional-SKU record ID, when updating an existing entry.
        referrerId: Referrer/marketplace ID the SKU applies to.
        sku: The additional SKU string.
    """

    variationId: Required[int]
    id: NotRequired[int]
    referrerId: NotRequired[int]
    sku: NotRequired[str]


class VariationBarcodePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_barcodes`
    (``PUT /rest/pim/variations/barcodes``).

    Keys:
        variationId: Variation ID to link the barcode to. **Required.**
        barcodeId: ID of an existing barcode type from
            ``/rest/pim/barcodes``. **Required.**
        code: Barcode value override for this variation, if the barcode
            type allows per-variation codes.
    """

    variationId: Required[int]
    barcodeId: Required[int]
    code: NotRequired[str]


class VariationBundleComponentPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_bundle_components`
    (``PUT /rest/pim/variations/bundle_components``).

    Keys:
        variationId: Variation ID of the bundle itself. **Required.**
        componentVariationId: Variation ID of the component contained in
            the bundle. **Required.**
        componentQuantity: Quantity of the component variation included
            per bundle unit.
    """

    variationId: Required[int]
    componentVariationId: Required[int]
    componentQuantity: NotRequired[float]


class VariationCategoryPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_categories`
    (``PUT /rest/pim/variations/categories``).

    Keys:
        variationId: Variation ID to link to the category. **Required.**
        categoryId: Category ID to link. **Required.**
        plentyId: Client (store) ID the link applies to.
    """

    variationId: Required[int]
    categoryId: Required[int]
    plentyId: NotRequired[int]


class VariationClientPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_clients`
    (``PUT /rest/pim/variations/clients``).

    Keys:
        variationId: Variation ID to make visible in the client. **Required.**
        plentyId: Client (store) ID the variation should be visible in.
            **Required.**
    """

    variationId: Required[int]
    plentyId: Required[int]


class VariationCommentPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_comments`
    (``PUT /rest/pim/variations/comments``).

    Keys:
        variationId: Variation ID to attach the comment to. **Required.**
        text: Comment text. **Required.**
        userId: ID of the back-end user who authored the comment.
        isPermanent: Whether the comment persists across imports/syncs
            instead of being overwritten.
    """

    variationId: Required[int]
    text: Required[str]
    userId: NotRequired[int]
    isPermanent: NotRequired[bool]


class VariationDefaultCategoryPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_default_categories`
    (``PUT /rest/pim/variations/default_categories``).

    Keys:
        variationId: Variation ID to set the default category for.
            **Required.**
        categoryId: Category ID to use as the default (canonical) category
            for this client. **Required.**
        plentyId: Client (store) ID the default applies to. **Required.**
    """

    variationId: Required[int]
    categoryId: Required[int]
    plentyId: Required[int]


class VariationImagePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_images`
    (``PUT /rest/pim/variations/images``).

    Keys:
        variationId: Variation ID to link the image to. **Required.**
        imageId: ID of an existing item image to link. **Required.**
        position: Display sort position among the variation's images.
    """

    variationId: Required[int]
    imageId: Required[int]
    position: NotRequired[int]


class VariationMarketIdentNumberPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_market_ident_numbers`
    (``PUT /rest/pim/variations/market_ident_numbers``).

    Keys:
        variationId: Variation ID to attach the identifier to. **Required.**
        marketIdentNumberType: Identifier type, e.g. ``"ean"``, ``"isbn"``,
            ``"upc"``, ``"gtin"``. **Required.**
        marketIdentNumber: The identifier value itself. **Required.**
    """

    variationId: Required[int]
    marketIdentNumberType: Required[str]
    marketIdentNumber: Required[str]


class VariationMarketPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_markets`
    (``PUT /rest/pim/variations/markets``).

    Keys:
        variationId: Variation ID to enable for the market. **Required.**
        marketId: Marketplace ID (e.g. an Amazon or eBay account ID
            configured under Market settings). **Required.**
    """

    variationId: Required[int]
    marketId: Required[int]


class VariationPropertyPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_properties`
    (``PUT /rest/pim/variations/properties``).

    Keys:
        variationId: Variation ID to set the property on. **Required.**
        propertyId: Item property ID (from ``/rest/items/properties``).
            **Required.**
        propertyValue: Value to assign for this variation. Required for
            text/number/date property types; omitted for selection types
            configured via property-value IDs instead.
    """

    variationId: Required[int]
    propertyId: Required[int]
    propertyValue: NotRequired[str]


class VariationSalesPricePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_sales_prices`
    (``PUT /rest/pim/variations/sales_prices``).

    Links a variation to a sales price *configuration* and sets its price
    *value*. See :class:`~plentymarkets._types.SalesPriceCreatePayload` for
    the configuration itself.

    Keys:
        variationId: Variation ID to set the price on. **Required.**
        salesPriceId: Sales price configuration ID (from
            ``/rest/pim/sales_prices``). **Required.**
        price: Net or gross price value, depending on the sales price
            configuration's settings. **Required.**
    """

    variationId: Required[int]
    salesPriceId: Required[int]
    price: Required[float]


class VariationSkuPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_skus`
    (``PUT /rest/pim/variations/skus``).

    Keys:
        variationId: Variation ID to set the marketplace SKU for.
            **Required.**
        marketId: Marketplace ID the SKU applies to. **Required.**
        sku: The marketplace-specific SKU string. **Required.**
    """

    variationId: Required[int]
    marketId: Required[int]
    sku: Required[str]


class VariationSupplierPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_supplier`
    (``PUT /rest/pim/variations/supplier``).

    Keys:
        variationId: Variation ID to link the supplier to. **Required.**
        supplierId: Supplier contact ID (from ``/rest/accounts/contacts``
            where the contact is flagged as a supplier). **Required.**
        supplierPartNumber: Supplier's own part number for this variation.
        priority: Preference order when a variation has multiple suppliers
            (lower = preferred).
    """

    variationId: Required[int]
    supplierId: Required[int]
    supplierPartNumber: NotRequired[str]
    priority: NotRequired[int]


class VariationTagPayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_tags`
    (``PUT /rest/pim/variations/tags``).

    Keys:
        variationId: Variation ID to tag. **Required.**
        tagId: Tag ID to attach. **Required.**
    """

    variationId: Required[int]
    tagId: Required[int]


class VariationWarehousePayload(TypedDict, total=False):
    """One entry for :meth:`PimModule.update_variation_warehouses`
    (``PUT /rest/pim/variations/warehouses``).

    Keys:
        variationId: Variation ID to link the warehouse to. **Required.**
        warehouseId: Warehouse ID to stock the variation in. **Required.**
        stockManagementActive: Whether stock levels for this variation are
            actively managed in this warehouse.
    """

    variationId: Required[int]
    warehouseId: Required[int]
    stockManagementActive: NotRequired[bool]


# ---------------------------------------------------------------------------
# PIM Attributes  (/rest/pim/attributes)
# ---------------------------------------------------------------------------


class AttributeCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attributes` (``POST /rest/pim/attributes``).

    Keys:
        backendName: Internal back-end name (unique, no commas, colons,
            semicolons, or quotes). **Required.**
        position: Display sort position in the attribute list.
        isSurchargePercental: Whether value surcharges are treated as a
            percentage rather than a fixed amount.
        isLinkableToImage: Whether images can be linked to attribute values.
        isGroupable: Whether attribute values can be grouped in the
            online store's filter navigation.
        amazonAttribute: Linked Amazon attribute name.
        fruugoAttribute: Linked Fruugo attribute name.
        pixmaniaAttribute: Linked Pixmania attribute ID.
        ottoAttribute: Linked Otto attribute name.
        googleShoppingAttribute: Linked Google Shopping attribute name.
        neckermannAtEpAttribute: Linked neckermann.at attribute ID.
        typeOfSelectionInOnlineStore: Selection widget type in the online
            store, e.g. ``"box"``, ``"list"``, ``"color"``, ``"image"``.
        laRedouteAttribute: Linked La Redoute attribute ID.
    """

    backendName: Required[str]
    position: NotRequired[int]
    isSurchargePercental: NotRequired[bool]
    isLinkableToImage: NotRequired[bool]
    isGroupable: NotRequired[bool]
    amazonAttribute: NotRequired[str]
    fruugoAttribute: NotRequired[str]
    pixmaniaAttribute: NotRequired[int]
    ottoAttribute: NotRequired[str]
    googleShoppingAttribute: NotRequired[str]
    neckermannAtEpAttribute: NotRequired[int]
    typeOfSelectionInOnlineStore: NotRequired[str]
    laRedouteAttribute: NotRequired[int]


class AttributeUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.update_attributes` (``PUT /rest/pim/attributes``).

    Keys:
        id: Attribute ID to update. **Required.**
        backendName: Internal back-end name (unique, no commas, colons,
            semicolons, or quotes).
        position: Display sort position in the attribute list.
        isSurchargePercental: Whether value surcharges are treated as a
            percentage rather than a fixed amount.
        isLinkableToImage: Whether images can be linked to attribute values.
        isGroupable: Whether attribute values can be grouped in the
            online store's filter navigation.
        amazonAttribute: Linked Amazon attribute name.
        fruugoAttribute: Linked Fruugo attribute name.
        pixmaniaAttribute: Linked Pixmania attribute ID.
        ottoAttribute: Linked Otto attribute name.
        googleShoppingAttribute: Linked Google Shopping attribute name.
        neckermannAtEpAttribute: Linked neckermann.at attribute ID.
        typeOfSelectionInOnlineStore: Selection widget type in the online
            store, e.g. ``"box"``, ``"list"``, ``"color"``, ``"image"``.
        laRedouteAttribute: Linked La Redoute attribute ID.
    """

    id: Required[int]
    backendName: NotRequired[str]
    position: NotRequired[int]
    isSurchargePercental: NotRequired[bool]
    isLinkableToImage: NotRequired[bool]
    isGroupable: NotRequired[bool]
    amazonAttribute: NotRequired[str]
    fruugoAttribute: NotRequired[str]
    pixmaniaAttribute: NotRequired[int]
    ottoAttribute: NotRequired[str]
    googleShoppingAttribute: NotRequired[str]
    neckermannAtEpAttribute: NotRequired[int]
    typeOfSelectionInOnlineStore: NotRequired[str]
    laRedouteAttribute: NotRequired[int]


class AttributeNamePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attribute_names` and
    :meth:`PimModule.update_attribute_names`
    (``POST``/``PUT /rest/pim/attributes/names``).

    Keys:
        attributeId: Attribute ID the name belongs to. **Required.**
        lang: Two-letter language code, e.g. ``"en"``, ``"de"``.
            **Required.**
        name: Display name shown in the back end and online store for this
            language. **Required.**
    """

    attributeId: Required[int]
    lang: Required[str]
    name: Required[str]


class AttributeValuePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attribute_values` and
    :meth:`PimModule.update_attribute_values`
    (``POST``/``PUT /rest/pim/attributes/values``).

    PlentyMarkets does not publish a request schema for this endpoint; keys
    are inferred from the ``GET`` search parameters and general attribute
    conventions. Verify against a live system before relying on optional
    keys.

    Keys:
        id: Attribute value ID, required when updating an existing value.
        attributeId: Attribute ID this value belongs to. **Required.**
        backendName: Internal back-end name for this value (e.g. ``"Red"``
            for a colour attribute). **Required.**
        position: Display sort position among the attribute's values.
        image: Path or URL of an image representing this value, used when
            the attribute's ``typeOfSelectionInOnlineStore`` is
            ``"image"`` or ``"color"``.
    """

    id: NotRequired[int]
    attributeId: Required[int]
    backendName: Required[str]
    position: NotRequired[int]
    image: NotRequired[str]


class AttributeValueNamePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_attribute_value_names` and
    :meth:`PimModule.update_attribute_value_names`
    (``POST``/``PUT /rest/pim/attributes/values/names``).

    Keys:
        valueId: Attribute value ID the name belongs to. **Required.**
        lang: Two-letter language code, e.g. ``"en"``, ``"de"``.
            **Required.**
        name: Display name shown in the back end and online store for this
            language. **Required.**
    """

    valueId: Required[int]
    lang: Required[str]
    name: Required[str]


# ---------------------------------------------------------------------------
# PIM Sales Prices  (/rest/pim/sales_prices)
# ---------------------------------------------------------------------------


class SalesPriceCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_sales_prices` (``POST /rest/pim/sales_prices``).

    Keys:
        type: Price type. Common values: ``"default"``, ``"rrp"``,
            ``"specialOffer"``, ``"setPrice"``. **Required.**
        position: Display sort position.
        minimumOrderQuantity: Minimum quantity for this price to apply.
        isCustomerPrice: Whether the price is customer-class specific.
        isDisplayedByDefault: Whether this price is shown by default in
            the online store.
        isLiveConversion: Whether to apply live FX conversion.
        interval: Interval this price applies over, e.g. ``"weekly"``.
        names: List of multilingual name dicts, each with ``lang``,
            ``nameInternal``, and ``nameExternal``.
        countries: List of dicts restricting the price to specific
            countries, each with ``countryId``.
        currencies: List of dicts declaring supported currencies, each
            with ``currency`` (ISO 4217 code, e.g. ``"EUR"``).
        customerClasses: List of dicts restricting the price to specific
            customer classes, each with ``customerClassId``.
        referrers: List of dicts restricting the price to specific
            referrers, each with ``referrerId``.
        clients: List of dicts restricting the price to specific clients
            (stores), each with ``plentyId``.
        accounts: List of dicts linking the price to specific accounts,
            each with ``accountId``.
    """

    type: Required[str]
    position: NotRequired[int]
    minimumOrderQuantity: NotRequired[float]
    isCustomerPrice: NotRequired[bool]
    isDisplayedByDefault: NotRequired[bool]
    isLiveConversion: NotRequired[bool]
    interval: NotRequired[str]
    names: NotRequired[list[dict[str, Any]]]
    countries: NotRequired[list[dict[str, Any]]]
    currencies: NotRequired[list[dict[str, Any]]]
    customerClasses: NotRequired[list[dict[str, Any]]]
    referrers: NotRequired[list[dict[str, Any]]]
    clients: NotRequired[list[dict[str, Any]]]
    accounts: NotRequired[list[dict[str, Any]]]


class SalesPriceUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.update_sales_prices` (``PUT /rest/pim/sales_prices``).

    Keys:
        id: Sales price configuration ID to update. **Required.**
        type: Price type. Common values: ``"default"``, ``"rrp"``,
            ``"specialOffer"``, ``"setPrice"``.
        position: Display sort position.
        minimumOrderQuantity: Minimum quantity for this price to apply.
        isCustomerPrice: Whether the price is customer-class specific.
        isDisplayedByDefault: Whether this price is shown by default in
            the online store.
        isLiveConversion: Whether to apply live FX conversion.
        interval: Interval this price applies over, e.g. ``"weekly"``.
        names: List of multilingual name dicts, each with ``lang``,
            ``nameInternal``, and ``nameExternal``.
        countries: List of dicts restricting the price to specific
            countries, each with ``countryId``.
        currencies: List of dicts declaring supported currencies, each
            with ``currency`` (ISO 4217 code, e.g. ``"EUR"``).
        customerClasses: List of dicts restricting the price to specific
            customer classes, each with ``customerClassId``.
        referrers: List of dicts restricting the price to specific
            referrers, each with ``referrerId``.
        clients: List of dicts restricting the price to specific clients
            (stores), each with ``plentyId``.
        accounts: List of dicts linking the price to specific accounts,
            each with ``accountId``.
    """

    id: Required[int]
    type: NotRequired[str]
    position: NotRequired[int]
    minimumOrderQuantity: NotRequired[float]
    isCustomerPrice: NotRequired[bool]
    isDisplayedByDefault: NotRequired[bool]
    isLiveConversion: NotRequired[bool]
    interval: NotRequired[str]
    names: NotRequired[list[dict[str, Any]]]
    countries: NotRequired[list[dict[str, Any]]]
    currencies: NotRequired[list[dict[str, Any]]]
    customerClasses: NotRequired[list[dict[str, Any]]]
    referrers: NotRequired[list[dict[str, Any]]]
    clients: NotRequired[list[dict[str, Any]]]
    accounts: NotRequired[list[dict[str, Any]]]


# ---------------------------------------------------------------------------
# PIM Barcodes  (/rest/pim/barcodes)
# ---------------------------------------------------------------------------


class BarcodeCreatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.create_barcodes` (``POST /rest/pim/barcodes``).

    Keys:
        name: Display name for the barcode type. **Required.**
        type: Barcode symbology/type, e.g. ``"EAN13"``, ``"EAN8"``,
            ``"CODE128"``, ``"GTIN"``. **Required.**
        referrers: List of referrer restriction dicts, each with
            ``referrerId`` (float — the spec declares this field as a
            number rather than an integer).
    """

    name: Required[str]
    type: Required[str]
    referrers: NotRequired[list[dict[str, Any]]]


class BarcodeUpdatePayload(TypedDict, total=False):
    """Payload for :meth:`PimModule.update_barcodes` (``PUT /rest/pim/barcodes``).

    Keys:
        id: Barcode configuration ID to update. **Required.**
        name: Display name for the barcode type.
        type: Barcode symbology/type, e.g. ``"EAN13"``, ``"EAN8"``,
            ``"CODE128"``, ``"GTIN"``.
        referrers: List of referrer restriction dicts, each with
            ``referrerId`` (float — the spec declares this field as a
            number rather than an integer).
    """

    id: Required[int]
    name: NotRequired[str]
    type: NotRequired[str]
    referrers: NotRequired[list[dict[str, Any]]]
