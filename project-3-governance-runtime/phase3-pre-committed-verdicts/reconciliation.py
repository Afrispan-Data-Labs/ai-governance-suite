"""Reconciliation step for Project 3, Phase 3: pre-committed verdicts.

Status: PROVEN. Verified 2026-08-26: tests/test_reconciliation.py passed
(4/4), and demo.py's real run correctly reconciled all 5 real Phase 3a
cases and surfaced the 1 synthetic case as MISSING_RESULT. See
data/phase3_demo_results.json for the actual output.

Compares every committed intent against actual evaluation results.
A commitment with a matching result is RECONCILED. A commitment with no
matching result is PENDING until it clears `window_hours`, then becomes a
named MISSING_RESULT finding, never silently dropped, per the spec's
acceptance criteria.

Design constraint (PHASE_3_4_SPEC.md): if the rubric has changed since a
commitment was made, reconciliation reports the rubric version that was
actually committed to, not whatever the current rubric version is.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ReconciliationFinding:
    commitment_id: str
    case_id: str
    rubric_version_at_commit: str
    judge_model: str
    status: str  # "RECONCILED", "PENDING", or "MISSING_RESULT"
    result_outcome: str = None
    rubric_changed: bool = False


@dataclass
class ReconciliationReport:
    findings: list = field(default_factory=list)

    @property
    def missing(self) -> list:
        return [f for f in self.findings if f.status == "MISSING_RESULT"]


def reconcile(commitments: list, results_by_case_id: dict,
              current_rubric_version: str = None,
              window_hours: float = 24.0,
              now: datetime = None) -> ReconciliationReport:
    """results_by_case_id maps case_id -> {"outcome": str}."""
    now = now or datetime.now(timezone.utc)
    report = ReconciliationReport()

    for c in commitments:
        committed_at = datetime.fromisoformat(c["committed_at"])
        age_hours = (now - committed_at).total_seconds() / 3600.0
        result = results_by_case_id.get(c["case_id"])
        rubric_changed = bool(current_rubric_version) and current_rubric_version != c["rubric_version"]

        if result is not None:
            status = "RECONCILED"
        elif age_hours >= window_hours:
            status = "MISSING_RESULT"
        else:
            status = "PENDING"

        report.findings.append(ReconciliationFinding(
            commitment_id=c["commitment_id"],
            case_id=c["case_id"],
            rubric_version_at_commit=c["rubric_version"],
            judge_model=c["judge_model"],
            status=status,
            result_outcome=result["outcome"] if result else None,
            rubric_changed=rubric_changed,
        ))

    return report
