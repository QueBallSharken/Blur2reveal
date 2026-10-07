from __future__ import annotations

from governance.contract import (
    RevealAuthorizationRequest,
    RevealAuthorizationResult,
)

from governance.gdp_adapter import evaluate_reveal_target
from governance.aic_adapter import validate_invariant_lineage
from governance.beaf_adapter import evaluate_boundary_evidence
from governance.ironclad_adapter import verify_boundary
from governance.fst_adapter import evaluate_stress_receipts
from governance.dtpe_adapter import authorize_boundary


def authorize_reveal(
    request: RevealAuthorizationRequest,
) -> RevealAuthorizationResult:

    governance_result = evaluate_reveal_target(request)

    if not governance_result.get("governance_valid", False):
        return RevealAuthorizationResult(
            allowed=False,
            governance_result=governance_result,
            denial_reason="Governance validation failed",
        )

    lineage_result = validate_invariant_lineage(request)

    if not lineage_result.get("lineage_valid", False):
        return RevealAuthorizationResult(
            allowed=False,
            governance_result={
                **governance_result,
                "aic": lineage_result,
            },
            denial_reason="Invariant lineage validation failed",
        )

    request.governance_context["governance_result"] = governance_result
    request.governance_context["lineage_result"] = lineage_result

    beaf_result = evaluate_boundary_evidence(request)

    ironclad_result = verify_boundary(request)

    fst_result = evaluate_stress_receipts()

    request.governance_context["fst"] = fst_result

    dtpe_result = authorize_boundary(
        identity_id=request.governance_context.get("identity_id"),
        owner_id=request.governance_context.get("owner_id"),
        intent=request.action,
        action=request.action,
        expires_at=request.governance_context.get("expires_at"),
        execution_time=request.governance_context.get("execution_time"),
        constraint_profile=request.governance_context.get("constraint_profile"),
        temporal_rule_profile=request.governance_context.get(
            "temporal_rule_profile"
        ),
    )

    if not dtpe_result["allowed"]:
        return RevealAuthorizationResult(
            allowed=False,
            governance_result={
                **governance_result,
                "aic": lineage_result,
                "beaf": beaf_result,
                "ironclad": ironclad_result,
                "fst": fst_result,
                "dtpe": dtpe_result,
            },
            denial_reason=dtpe_result["reason"],
        )

    return RevealAuthorizationResult(
        allowed=True,
        governance_result={
            **governance_result,
            "aic": lineage_result,
            "beaf": beaf_result,
            "ironclad": ironclad_result,
            "fst": fst_result,
            "dtpe": dtpe_result,
        },
        receipt=dtpe_result.get("receipt"),
    )
