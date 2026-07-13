from __future__ import annotations

from typing import Any

from ..._session import Session


class PimBase:
    """Shared state and helpers for every ``PimModule`` mixin.

    ``_session`` is declared here only as a class-level type annotation (no
    ``__init__``) so every mixin's methods can reference ``self._session``
    with type-checker support; the attribute is actually assigned once, in
    ``PimModule.__init__``.
    """

    _session: Session

    @staticmethod
    def _build_params(
        filters: dict[str, Any] | None,
        with_: list[str] | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if filters:
            params.update(filters)
        if with_:
            params["with"] = ",".join(with_)
        return params
