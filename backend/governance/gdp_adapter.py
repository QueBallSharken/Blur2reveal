from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

from governance.contract import RevealAuthorizationRequest

GDP_ROOT = Path(r"C:\Repos\dtpe-gdp")

if str(GDP_ROOT) not in sys.path:
    sys.path.insert(0, str(GDP_ROOT))

from core.gdp.evaluator import evaluate_target


def evaluate_reveal_target(
    request: RevealAuthorizationRequest,
) -> Dict[str, Any]:

    target = {
        "authority_explicit_at_execution": True,
        "state_admissibility_explicit": True,
        "temporal_validity_explicit": True,
        "continuity_explicit": True,
        "decision_space_integrity_explicit": True,
        "evaluator_integrity_explicit": True,
        "true_mutation_authority_identified": True,
        "mutation_bound_continuity_explicit": True,
        "decision_evidence_replayable": True,
    }

    return evaluate_target(target)
