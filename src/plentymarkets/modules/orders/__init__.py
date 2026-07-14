from __future__ import annotations

from ..._session import Session
from ._base import OrdersBase
from .core import CoreMixin
from .coupons import CouponsMixin
from .currencies import CurrenciesMixin
from .dates import DatesMixin
from .order_items import ItemsMixin
from .properties import PropertiesMixin
from .referrers import ReferrersMixin
from .reorders import ReordersMixin
from .status_history import StatusHistoryMixin
from .statuses import StatusMixin
from .taric import TaricMixin
from .transactions import TransactionsMixin

__all__ = ["OrdersModule"]


class OrdersModule(
    CoreMixin,
    StatusMixin,
    StatusHistoryMixin,
    DatesMixin,
    TransactionsMixin,
    ItemsMixin,
    ReordersMixin,
    PropertiesMixin,
    ReferrersMixin,
    CurrenciesMixin,
    CouponsMixin,
    TaricMixin,
    OrdersBase,
):
    """Wraps the PlentyMarkets ``/rest/orders`` endpoints.

    Internally composed from per-resource mixins under this package; the
    public API is unchanged — every method is available directly on this
    class, e.g. ``client.orders.list_status_definitions(...)``.

    Args:
        session: Shared authenticated session.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def __repr__(self) -> str:
        return "<OrdersModule /rest/orders>"
