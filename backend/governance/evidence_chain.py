from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict


LEDGER_PATH = (
    Path(__file__).parent
    / "doorway_ledger.json"
)


def build_evidence_material(
    *,
    governance_valid: bool,
    lineage_hash: str | None,
    evidence_hash: str | None,
    receipt_hash: str | None,
    previous_chain_hash: str | None,
) -> Dict[str, Any]:

    return {
        "governance_valid":
            governance_valid,

        "lineage_hash":
            lineage_hash,

        "evidence_hash":
            evidence_hash,

        "receipt_hash":
            receipt_hash,

        "previous_chain_hash":
            previous_chain_hash,
    }


def hash_evidence_material(
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


def build_doorway_chain_hash(
    *,
    governance_result: Dict[str, Any],
    lineage_result: Dict[str, Any],
    beaf_result: Dict[str, Any],
    dtpe_result: Dict[str, Any],
    previous_chain_hash: str | None = None,
) -> str:

    material = build_evidence_material(
        governance_valid=
            governance_result.get(
                "governance_valid",
                False,
            ),

        lineage_hash=
            lineage_result.get(
                "lineage_hash"
            ),

        evidence_hash=
            beaf_result.get(
                "evidence_hash"
            ),

        receipt_hash=
            dtpe_result.get(
                "receipt_hash"
            ),

        previous_chain_hash=
            previous_chain_hash,
    )

    return hash_evidence_material(
        material
    )


def load_ledger() -> list[Dict[str, Any]]:

    if not LEDGER_PATH.exists():
        return []

    content = LEDGER_PATH.read_text(
        encoding="utf-8"
    ).strip()

    if not content:
        return []

    return json.loads(content)


def save_ledger(
    ledger: list[Dict[str, Any]]
) -> None:

    LEDGER_PATH.write_text(
        json.dumps(
            ledger,
            indent=2,
        ),
        encoding="utf-8",
    )


def latest_chain_hash() -> str | None:

    ledger = load_ledger()

    if not ledger:
        return None

    return ledger[-1].get(
        "chain_hash"
    )


def append_ledger_event(
    *,
    chain_hash: str,
    requester_id: str,
    asset_id: str,
    evidence_material: Dict[str, Any] | None = None,
) -> Dict[str, Any]:

    ledger = load_ledger()

    previous_chain_hash = None

    if ledger:
        previous_chain_hash = ledger[-1].get(
            "chain_hash"
        )

    if evidence_material is not None:

        material_previous_hash = (
            evidence_material.get(
                "previous_chain_hash"
            )
        )

        if material_previous_hash != (
            previous_chain_hash
        ):

            raise ValueError(
                "Evidence material predecessor "
                "does not match the current ledger "
                "chain head"
            )

        computed_material_hash = (
            hash_evidence_material(
                evidence_material
            )
        )

        if computed_material_hash != (
            chain_hash
        ):

            raise ValueError(
                "Chain hash does not match "
                "the supplied evidence material"
            )

    entry = {
        "sequence":
            len(ledger) + 1,

        "requester_id":
            requester_id,

        "asset_id":
            asset_id,

        "previous_chain_hash":
            previous_chain_hash,

        "chain_hash":
            chain_hash,
    }

    if evidence_material is not None:

        entry[
            "evidence_material"
        ] = evidence_material

        entry[
            "evidence_material_hash"
        ] = hash_evidence_material(
            evidence_material
        )

    ledger.append(
        entry
    )

    save_ledger(
        ledger
    )

    return entry

def verify_chain(
    ledger: list[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:

    if ledger is None:
        ledger = load_ledger()

    if not ledger:
        return {
            "valid": True,
            "chain_active": False,
            "records": 0,
            "verified_links": 0,
            "recomputed_records": 0,
            "legacy_records": 0,
            "migration_boundary": None,
            "breaks": [],
        }

    breaks = []
    verified_links = 0
    recomputed_records = 0
    legacy_records = 0
    migration_boundary = None

    expected_sequence = 1

    for index, entry in enumerate(ledger):

        sequence = entry.get(
            "sequence"
        )

        if sequence != expected_sequence:

            breaks.append({
                "type":
                    "SEQUENCE_ERROR",

                "index":
                    index,

                "expected":
                    expected_sequence,

                "actual":
                    sequence,
            })

        expected_sequence += 1

        if index == 0:

            if entry.get(
                "previous_chain_hash"
            ) is not None:

                breaks.append({
                    "type":
                        "GENESIS_PREDECESSOR_PRESENT",

                    "index":
                        index,
                })

            continue

        previous_entry = ledger[
            index - 1
        ]

        previous_hash = previous_entry.get(
            "chain_hash"
        )

        current_previous_hash = entry.get(
            "previous_chain_hash"
        )

        if current_previous_hash is None:

            legacy_records += 1

            continue

        if migration_boundary is None:
            migration_boundary = sequence

        if current_previous_hash != previous_hash:

            breaks.append({
                "type":
                    "CHAIN_LINK_MISMATCH",

                "index":
                    index,

                "sequence":
                    sequence,

                "expected":
                    previous_hash,

                "actual":
                    current_previous_hash,
            })

            continue

        verified_links += 1

        evidence_material = entry.get(
            "evidence_material"
        )

        if evidence_material is None:

            legacy_records += 1

            continue

        stored_material_hash = entry.get(
            "evidence_material_hash"
        )

        computed_material_hash = (
            hash_evidence_material(
                evidence_material
            )
        )

        if stored_material_hash != (
            computed_material_hash
        ):

            breaks.append({
                "type":
                    "EVIDENCE_MATERIAL_HASH_MISMATCH",

                "index":
                    index,

                "sequence":
                    sequence,

                "expected":
                    computed_material_hash,

                "actual":
                    stored_material_hash,
            })

            continue

        computed_chain_hash = (
            hash_evidence_material(
                evidence_material
            )
        )

        stored_chain_hash = entry.get(
            "chain_hash"
        )

        if computed_chain_hash != (
            stored_chain_hash
        ):

            breaks.append({
                "type":
                    "CHAIN_HASH_RECOMPUTATION_MISMATCH",

                "index":
                    index,

                "sequence":
                    sequence,

                "expected":
                    computed_chain_hash,

                "actual":
                    stored_chain_hash,
            })

            continue

        recomputed_records += 1

    return {
        "valid":
            len(breaks) == 0,

        "chain_active":
            verified_links > 0,

        "records":
            len(ledger),

        "verified_links":
            verified_links,

        "recomputed_records":
            recomputed_records,

        "legacy_records":
            legacy_records,

        "migration_boundary":
            migration_boundary,

        "breaks":
            breaks,
    }


