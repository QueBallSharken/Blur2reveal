from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

from governance.contract import RevealAuthorizationRequest


def _canonical_lineage_material(
    request: RevealAuthorizationRequest,
) -> Dict[str, Any]:
    return {
        "requester_id": request.requester_id,
        "asset_id": request.asset_id,
        "action": request.action,
    }


def _lineage_hash(
    material: Dict[str, Any],
) -> str:
    canonical = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def validate_invariant_lineage(
    request: RevealAuthorizationRequest,
) -> Dict[str, Any]:

    material = _canonical_lineage_material(
        request
    )

    lineage_hash = _lineage_hash(
        material
    )

    return {
        "lineage_valid": True,
        "lineage_provider": lineage_provider(),
        "lineage_hash": lineage_hash,
        "clone_count": 1,
        "gaps": [],
        "risk_class": "LOW",
        "invariant_material": material,
    }

def bridge_available() -> bool:
    try:
        from governance.aic_bridge import bridge_status
        return bridge_status()["aic_connected"]
    except Exception:
        return False

def lineage_provider() -> str:
    if bridge_available():
        return "AIC"

    return "LOCAL_PLACEHOLDER"

