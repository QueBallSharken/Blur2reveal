import pytest

from pydantic import ValidationError

from governance.contract import (
    RevealAuthorizationRequest,
)
from governance.doorway import (
    authorize_reveal,
)
import governance.evidence_chain as evidence_chain


@pytest.fixture
def isolated_ledger(tmp_path, monkeypatch):

    test_ledger = (
        tmp_path
        / "doorway_ledger.json"
    )

    monkeypatch.setattr(
        evidence_chain,
        "LEDGER_PATH",
        test_ledger,
    )

    return test_ledger


def test_valid_request_is_authorized(
    isolated_ledger,
):

    request = RevealAuthorizationRequest(
        requester_id="alice",
        asset_id="test-asset-001",
    )

    result = authorize_reveal(
        request
    )

    assert result.allowed is True

    ledger = evidence_chain.load_ledger()

    assert len(ledger) == 1
    assert ledger[0]["sequence"] == 1


def test_missing_requester_is_rejected():

    with pytest.raises(
        ValidationError
    ):
        RevealAuthorizationRequest(
            requester_id="",
            asset_id="asset-001",
        )


def test_tampered_evidence_material_is_rejected():

    ledger = [
        {
            "sequence": 1,
            "requester_id": "alice",
            "asset_id": "asset-001",
            "chain_hash": "legacy-hash",
        },
        {
            "sequence": 2,
            "requester_id": "alice",
            "asset_id": "asset-005",
            "previous_chain_hash":
                "legacy-hash",
            "chain_hash":
                "original-chain-hash",
            "evidence_material": {
                "governance_valid": True,
                "lineage_hash": "TAMPERED",
                "evidence_hash":
                    "evidence-hash",
                "receipt_hash":
                    "receipt-hash",
                "previous_chain_hash":
                    "legacy-hash",
            },
            "evidence_material_hash":
                "original-material-hash",
        },
    ]

    result = evidence_chain.verify_chain(
        ledger
    )

    assert result["valid"] is False
    assert result["breaks"]

    assert any(
        item["type"]
        == "EVIDENCE_MATERIAL_HASH_MISMATCH"
        for item in result["breaks"]
    )

def test_append_rejects_forged_predecessor(
    tmp_path,
    monkeypatch,
):

    import governance.evidence_chain as evidence_chain

    test_ledger = (
        tmp_path
        / "doorway_ledger.json"
    )

    monkeypatch.setattr(
        evidence_chain,
        "LEDGER_PATH",
        test_ledger,
    )

    valid_material = (
        evidence_chain.build_evidence_material(
            governance_valid=True,
            lineage_hash="lineage-hash",
            evidence_hash="evidence-hash",
            receipt_hash="receipt-hash",
            previous_chain_hash=None,
        )
    )

    valid_hash = (
        evidence_chain.hash_evidence_material(
            valid_material
        )
    )

    evidence_chain.append_ledger_event(
        chain_hash=valid_hash,
        requester_id="alice",
        asset_id="test-asset-001",
        evidence_material=valid_material,
    )

    forged_material = (
        evidence_chain.build_evidence_material(
            governance_valid=True,
            lineage_hash="lineage-hash-2",
            evidence_hash="evidence-hash-2",
            receipt_hash="receipt-hash-2",
            previous_chain_hash="FORGED",
        )
    )

    forged_hash = (
        evidence_chain.hash_evidence_material(
            forged_material
        )
    )

    with pytest.raises(
        ValueError,
        match="predecessor",
    ):
        evidence_chain.append_ledger_event(
            chain_hash=forged_hash,
            requester_id="alice",
            asset_id="test-asset-002",
            evidence_material=forged_material,
        )


def test_append_rejects_forged_chain_hash(
    tmp_path,
    monkeypatch,
):

    import governance.evidence_chain as evidence_chain

    test_ledger = (
        tmp_path
        / "doorway_ledger.json"
    )

    monkeypatch.setattr(
        evidence_chain,
        "LEDGER_PATH",
        test_ledger,
    )

    material = (
        evidence_chain.build_evidence_material(
            governance_valid=True,
            lineage_hash="lineage-hash",
            evidence_hash="evidence-hash",
            receipt_hash="receipt-hash",
            previous_chain_hash=None,
        )
    )

    with pytest.raises(
        ValueError,
        match="Chain hash",
    ):
        evidence_chain.append_ledger_event(
            chain_hash="FORGED_CHAIN_HASH",
            requester_id="alice",
            asset_id="test-asset-001",
            evidence_material=material,
        )
