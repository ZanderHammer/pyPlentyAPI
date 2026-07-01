"""TypedDict definitions for PlentyMarkets API request payloads.

Import these when constructing payloads to get IDE autocomplete and
static type checking. At runtime they are plain dicts — no overhead.

Example::

    from plentymarkets._types import OrderCreatePayload

    payload: OrderCreatePayload = {"typeId": 1, "plentyId": 12345}
    order = await client.orders.create(payload)
"""

from typing import NotRequired, Required, TypedDict


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
