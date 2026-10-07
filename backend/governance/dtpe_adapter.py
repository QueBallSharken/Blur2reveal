from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict


DTPE_ROOT = Path(r"C:\Repos\dtpe-canonical-runtime")

if str(DTPE_ROOT) not in sys.path:
    sys.path.insert(0, str(DTPE_ROOT))


from core.phase4.pipeline import execute_request


def authorize_boundary(**kwargs: Any) -> Dict[str, Any]:
    """
    B2R -> DTPE integration boundary.

    DTPE remains an external, read-only dependency.
    B2R translates its governance context into the established
    DTPE execute_request() interface.

    Fail closed when required DTPE authorization context is absent.
    """

    required = (
        "identity_id",
        "owner_id",
        "intent",
        "action",
        "expires_at",
        "execution_time",
        "constraint_profile",
        "temporal_rule_profile",
    )

    missing = [
        name for name in required
        if kwargs.get(name) in (None, "")
    ]

    if missing:
        return {
            "allowed": False,
            "decision": "DENY",
            "reason": "DTPE authorization context incomplete",
            "missing": missing,
            "receipt": None,
        }

    try:
        receipt = execute_request(
            policy_filename=kwargs.get(
                "policy_filename",
                "default.json",
            ),
            identity_id=kwargs["identity_id"],
            owner_id=kwargs["owner_id"],
            intent=kwargs["intent"],
            action=kwargs["action"],
            expires_at=kwargs["expires_at"],
            execution_time=kwargs["execution_time"],
            constraint_profile=kwargs["constraint_profile"],
            temporal_rule_profile=kwargs[
                "temporal_rule_profile"
            ],
            prior_invariant_frame_hash=kwargs.get(
                "prior_invariant_frame_hash"
            ),
            prior_execution_time=kwargs.get(
                "prior_execution_time"
            ),
            continuity_required=kwargs.get(
                "continuity_required",
                False,
            ),
            transition_mode=kwargs.get(
                "transition_mode",
                "DISABLED",
            ),
            allowed_frame_transitions=kwargs.get(
                "allowed_frame_transitions"
            ),
        )

    except Exception as exc:
        return {
            "allowed": False,
            "decision": "DENY",
            "reason": "DTPE execution failed",
            "error_type": type(exc).__name__,
            "receipt": None,
        }

    allowed = (
        receipt.get("execution_state") == "ALLOW"
        and receipt.get("reason") == "BOUNDARY_ALLOW"
    )

    return {
        "allowed": allowed,
        "decision": "ALLOW" if allowed else "DENY",
        "reason": (
            "DTPE boundary allowed"
            if allowed
            else receipt.get("reason", "DTPE boundary denied")
        ),
        "receipt": receipt,
    }
