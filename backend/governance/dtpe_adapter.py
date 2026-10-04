from __future__ import annotations

from typing import Any, Dict


def authorize_boundary(**kwargs: Any) -> Dict[str, Any]:
    """
    Placeholder DTPE adapter.

    Real implementation will call:

        dtpe-canonical-runtime/core/phase4/pipeline.py

    Fail closed until connected.
    """

    raise RuntimeError(
        "DTPE adapter not connected"
    )