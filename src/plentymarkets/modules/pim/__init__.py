from __future__ import annotations

from ..._session import Session
from ._base import PimBase
from .attribute_names import AttributeNamesMixin
from .attribute_values import AttributeValuesMixin
from .attributes import AttributesMixin
from .barcodes import BarcodesMixin
from .categories import CategoriesMixin
from .item_serial_numbers import ItemSerialNumbersMixin
from .lookups import LookupsMixin
from .sales_prices import SalesPricesMixin
from .variation_commerce import VariationCommerceMixin
from .variation_identifiers import VariationIdentifiersMixin
from .variation_taxonomy import VariationTaxonomyMixin
from .variations import VariationsMixin

__all__ = ["PimModule"]


class PimModule(
    VariationsMixin,
    VariationIdentifiersMixin,
    VariationTaxonomyMixin,
    VariationCommerceMixin,
    AttributesMixin,
    AttributeNamesMixin,
    AttributeValuesMixin,
    CategoriesMixin,
    SalesPricesMixin,
    BarcodesMixin,
    ItemSerialNumbersMixin,
    LookupsMixin,
    PimBase,
):
    """Wraps the PlentyMarkets ``/rest/pim`` endpoints.

    Internally composed from per-resource mixins under this package; the
    public API is unchanged — every method is available directly on this
    class, e.g. ``client.pim.list_variations(...)``.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<PimModule /rest/pim>"
