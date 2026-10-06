from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

from governance.contract import RevealAuthorizationRequest
from governance.aic_bridge import (
    verify_aic_receipt,
)


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

    if not bridge_available():
        return {
            "lineage_valid": False,
            "lineage_provider": "AIC",
            "lineage_hash": lineage_hash,
            "clone_count": 0,
            "gaps": ["AIC bridge unavailable"],
            "risk_class": "CRITICAL",
            "invariant_material": material,
        }

    context = request.governance_context

    receipt_dict = context.get(
        "aic_receipt"
    )

    terminal_public_key_hex = context.get(
        "aic_terminal_public_key_hex"
    )

    if not receipt_dict:
        return {
            "lineage_valid": False,
            "lineage_provider": "AIC",
            "lineage_hash": lineage_hash,
            "clone_count": 0,
            "gaps": ["AIC terminal receipt missing"],
            "risk_class": "CRITICAL",
            "invariant_material": material,
        }

    if not terminal_public_key_hex:
        return {
            "lineage_valid": False,
            "lineage_provider": "AIC",
            "lineage_hash": lineage_hash,
            "clone_count": 0,
            "gaps": ["AIC terminal public key missing"],
            "risk_class": "CRITICAL",
            "invariant_material": material,
        }

    try:
        audit_result = verify_aic_receipt(
            receipt_dict,
            terminal_public_key_hex,
        )
    except Exception as exc:
        return {
            "lineage_valid": False,
            "lineage_provider": "AIC",
            "lineage_hash": lineage_hash,
            "clone_count": 0,
            "gaps": [
                f"AIC receipt audit failed: {type(exc).__name__}"
            ],
            "risk_class": "CRITICAL",
            "invariant_material": material,
        }

    audit_valid = bool(
        audit_result.get("lineage_valid", False)
    )

    return {
        "lineage_valid": audit_valid,
        "lineage_provider": "AIC",
        "lineage_hash": lineage_hash,
        "clone_count": 1 if audit_valid else 0,
        "gaps": []
        if audit_valid
        else ["AIC receipt audit invalid"],
        "risk_class": "LOW"
        if audit_valid
        else "CRITICAL",
        "invariant_material": material,
        "aic_audit": audit_result,
        "continuity_established": False,
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

