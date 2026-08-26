"""Status: PROVEN. Run for real on 2026-08-26 via `pytest tests/`, 4/4
passed."""

import os
import tempfile
from dataclasses import asdict

from commitment import commit_intent, verify_commitment, load_commitments


def test_commit_intent_produces_verifiable_hash():
    with tempfile.TemporaryDirectory() as tmp:
        store_path = os.path.join(tmp, "commitments.jsonl")
        record = commit_intent("tc_001", "faithfulness_geval_v1", "claude-sonnet-4-6", store_path=store_path)
        assert verify_commitment(asdict(record))


def test_verify_commitment_fails_on_tampered_field():
    with tempfile.TemporaryDirectory() as tmp:
        store_path = os.path.join(tmp, "commitments.jsonl")
        record = commit_intent("tc_001", "faithfulness_geval_v1", "claude-sonnet-4-6", store_path=store_path)
        tampered = asdict(record)
        tampered["case_id"] = "tc_999"
        assert not verify_commitment(tampered)


def test_commit_intent_appends_without_rewriting():
    with tempfile.TemporaryDirectory() as tmp:
        store_path = os.path.join(tmp, "commitments.jsonl")
        commit_intent("tc_001", "faithfulness_geval_v1", "claude-sonnet-4-6", store_path=store_path)
        commit_intent("tc_002", "faithfulness_geval_v1", "claude-sonnet-4-6", store_path=store_path)
        records = load_commitments(store_path)
        assert len(records) == 2
        assert records[0]["case_id"] == "tc_001"
        assert records[1]["case_id"] == "tc_002"


def test_load_commitments_returns_empty_list_when_store_missing():
    assert load_commitments("/nonexistent/path/commitments.jsonl") == []
