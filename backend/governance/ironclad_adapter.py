from __future__ import annotations

from typing import Any


def verify_boundary(request: Any) -> dict[str, Any]:
    """
    IRONCLAD boundary verification.

    Fail closed until real host/snapshot
    artifacts are supplied.
    """

    return {
        "allowed": False,
        "decision": "deny",
        "reasons": [
            "IRONCLAD adapter not connected"
        ],
        "receipt": None,
    }
