from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

DTPE_ROOT = Path(r"C:\Repos\dtpe-canonical-runtime")

if str(DTPE_ROOT) not in sys.path:
    sys.path.insert(0, str(DTPE_ROOT))

from core.spectre.fst.runner import run_all_known_suites
from core.spectre.fst.rule_profiles import (
    get_first_target_rule_profile,
)


def evaluate_stress_receipts() -> Dict[str, Any]:

    profile = get_first_target_rule_profile()

    results = run_all_known_suites(
        rule_profile_id=profile["fst_rule_profile_id"]
    )

    contradiction_count = 0

    for suite in results["suites_by_category"].values():
        for receipt in suite["receipts"]:
            if receipt["fst_result"] == "CONTRADICTION_EXPOSED":
                contradiction_count += 1

    return {
        "fst_valid": True,
        "contradiction_count": contradiction_count,
        "results": results,
    }
