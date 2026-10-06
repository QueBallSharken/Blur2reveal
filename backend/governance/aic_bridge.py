from __future__ import annotations

from pathlib import Path
import sys

AIC_ROOT = Path(
    r"C:\Repos\Active-Invariant-Cloning-Lab"
)

if str(AIC_ROOT) not in sys.path:
    sys.path.insert(0, str(AIC_ROOT))

from aic_harness.receipt import (
    receipt_from_dict,
)

from aic_harness.verifier import (
    audit,
)
def bridge_status():
    return {
        "aic_connected": True,
        "receipt_class":
            receipt_from_dict.__name__,
        "audit_function":
            audit.__name__,
    }

def verify_aic_receipt(
    receipt_dict,
    terminal_public_key_hex,
):
    receipt = receipt_from_dict(
        receipt_dict
    )

    result = audit(
        receipt,
        terminal_public_key_hex,
    )

    return {
        "lineage_valid":
            result.valid,

        "receipt_signature_valid":
            result.receipt_signature_valid,

        "receipt_integrity_valid":
            result.receipt_integrity_valid,

        "evidence_link_valid":
            result.evidence_link_valid,

        "evidence_chain_valid":
            result.evidence_chain_valid,
    }
