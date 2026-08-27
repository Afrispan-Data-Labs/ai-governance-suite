"""Status: PROVEN. Run for real on 2026-08-27 via `pytest tests/`, 5/5
passed."""

import os
import tempfile

from commitment import commit_intent

from data_store import (
    build_routing_rates,
    build_judge_alignment_trend,
    build_regression_status,
    build_verdict_drilldown,
)


def test_routing_rates_counts_five_real_cases():
    result = build_routing_rates()
    assert result["total_cases"] == 5
    assert result["counts"] == {"PASS": 2, "BORDERLINE": 1, "FAIL": 2}


def test_judge_alignment_has_exactly_two_real_points():
    result = build_judge_alignment_trend()
    assert len(result["points"]) == 2
    assert result["points"][0]["rate"] < result["points"][1]["rate"]


def test_regression_status_counts_match_labels():
    result = build_regression_status()
    assert result["counts"] == {"OK": 1, "WARNING": 1, "ALARM": 5}
    real_count = sum(1 for c in result["cases"] if c["real"])
    assert real_count == 6  # 5 ALARM + 1 OK are real, 1 WARNING is synthetic


def test_verdict_drilldown_missing_file_is_labeled_missing():
    result = build_verdict_drilldown(commitments_path="/nonexistent/commitments.jsonl")
    assert result["verdicts"] == []
    assert "MISSING" in result["note"]


def test_verdict_drilldown_verifies_real_commitment_hash():
    with tempfile.TemporaryDirectory() as tmp:
        store_path = os.path.join(tmp, "commitments.jsonl")
        commit_intent("tc_001", "v1", "claude-sonnet-4-6", store_path=store_path)
        result = build_verdict_drilldown(commitments_path=store_path)
        assert len(result["verdicts"]) == 1
        assert result["verdicts"][0]["hash_verified"] is True
