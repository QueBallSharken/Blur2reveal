from __future__ import annotations

from governance.contract import (
    RevealAuthorizationRequest,
    RevealAuthorizationResult,
)

from governance.gdp_adapter import evaluate_reveal_target
from governance.aic_adapter import validate_invariant_lineage
from governance.beaf_adapter import evaluate_boundary_evidence


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

    beaf_result = evaluate_boundary_evidence(
        request
    )

    return RevealAuthorizationResult(
        allowed=False,
        governance_result={
            **governance_result,
            "aic": lineage_result,
            "beaf": beaf_result,
        },
        denial_reason="DTPE authorization not yet connected",
    )
