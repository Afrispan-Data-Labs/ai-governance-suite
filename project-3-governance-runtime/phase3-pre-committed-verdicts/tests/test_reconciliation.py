"""Status: PROVEN. Run for real on 2026-08-26 via `pytest tests/`, 4/4
passed."""

from datetime import datetime, timedelta, timezone

from reconciliation import reconcile


def _commitment(case_id, rubric_version="v1", judge_model="claude-sonnet-4-6",
                 committed_at=None, commitment_id="cid-1"):
    return {
        "commitment_id": commitment_id,
        "case_id": case_id,
        "rubric_version": rubric_version,
        "judge_model": judge_model,
        "committed_at": (committed_at or datetime.now(timezone.utc)).isoformat(),
    }


def test_matched_commitment_is_reconciled():
    now = datetime.now(timezone.utc)
    commitments = [_commitment("tc_001", committed_at=now)]
    report = reconcile(commitments, {"tc_001": {"outcome": "PASS"}}, now=now)
    assert len(report.findings) == 1
    assert report.findings[0].status == "RECONCILED"
    assert report.findings[0].result_outcome == "PASS"


def test_unmatched_commitment_past_window_is_missing_result():
    old = datetime.now(timezone.utc) - timedelta(hours=48)
    commitments = [_commitment("tc_999", committed_at=old)]
    report = reconcile(commitments, {}, window_hours=24, now=datetime.now(timezone.utc))
    assert len(report.missing) == 1
    assert report.missing[0].case_id == "tc_999"


def test_unmatched_commitment_within_window_is_pending_not_missing():
    recent = datetime.now(timezone.utc) - timedelta(hours=1)
    commitments = [_commitment("tc_998", committed_at=recent)]
    report = reconcile(commitments, {}, window_hours=24, now=datetime.now(timezone.utc))
    assert len(report.missing) == 0
    assert report.findings[0].status == "PENDING"


def test_reconciliation_flags_rubric_change():
    now = datetime.now(timezone.utc)
    commitments = [_commitment("tc_001", rubric_version="v1", committed_at=now)]
    report = reconcile(commitments, {"tc_001": {"outcome": "PASS"}},
                        current_rubric_version="v2", now=now)
    assert report.findings[0].rubric_changed is True
    assert report.findings[0].rubric_version_at_commit == "v1"
