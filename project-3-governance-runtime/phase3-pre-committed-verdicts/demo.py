"""Demonstration for Project 3, Phase 3: pre-committed verdicts.

Status: PROVEN. Verified 2026-08-26: run for real, all 5 real Phase 3a
commitments reconciled correctly against their real recorded outcomes
(PASS, PASS, BORDERLINE, FAIL, FAIL), and the 1 synthetic no-result
commitment correctly surfaced as MISSING_RESULT. See
data/phase3_demo_results.json for the actual saved output.

Two things happen here, kept clearly separate, same honesty pattern as
Project 2's Phase 06b demonstration:

1. REAL: commits intents for Project 2's five real Phase 3a test cases
   (tc_001-tc_005), sourced directly from
   project-2-llm-evaluation-suite/tests/test_governance_suite.py's
   TEST_CASES (expected_outcome field) and JUDGE_MODEL, then reconciles
   them against those real, already-recorded routing outcomes.

   Honest limitation, stated plainly: Phase 3a already ran before this
   demo exists. These commitments are necessarily constructed
   retroactively against already-known results, not captured live before
   the evaluation ran. This proves the commit/reconcile mechanism works
   correctly against real data, it is not a true prospective
   pre-registration capture. Wiring commit_intent() into an actual
   pre-run trigger is future work, not built here.

2. SYNTHETIC: one fabricated commitment, for a case id with no result
   anywhere, added only to prove the MISSING_RESULT branch of
   reconciliation actually fires, since no real Phase 3a case is missing
   a result. Labeled as fabricated at every level, never merged with the
   five real commitments.

Rubric versioning note: Project 2 has no existing formal rubric-version
string. "faithfulness_geval_v1" is introduced here by Phase 3 itself, for
the faithfulness GEval criteria used in 03a/03b, not a value that existed
in Project 2 before this phase.
"""

import json
import os
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from commitment import commit_intent, verify_commitment, load_commitments, DEFAULT_STORE_PATH
from reconciliation import reconcile

JUDGE_MODEL = "claude-sonnet-4-6"  # real, from Phase 3a / test_governance_suite.py
RUBRIC_VERSION = "faithfulness_geval_v1"  # introduced by Phase 3, see module docstring

# Real case ids and real routing outcomes, sourced directly from
# project-2-llm-evaluation-suite/tests/test_governance_suite.py's
# TEST_CASES (expected_outcome field), which mirrors 03a's actual
# recorded 5/5 routing result.
REAL_PHASE3A_RESULTS = {
    "tc_001": "PASS",
    "tc_002": "PASS",
    "tc_003": "BORDERLINE",
    "tc_004": "FAIL",
    "tc_005": "FAIL",
}

SYNTHETIC_CASE_ID = "SYNTHETIC_no_result_demo_only"

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "data", "phase3_demo_results.json")


def run_demo(store_path: str = DEFAULT_STORE_PATH) -> dict:
    if os.path.exists(store_path):
        os.remove(store_path)  # fresh demo run, not a real production store

    print("--- Committing intents for 5 real Phase 3a cases ---")
    real_commitments = []
    for case_id in REAL_PHASE3A_RESULTS:
        record = commit_intent(case_id, RUBRIC_VERSION, JUDGE_MODEL, store_path=store_path)
        assert verify_commitment(asdict(record)), f"hash did not verify for {case_id}"
        real_commitments.append(record)
        print(f"  committed {case_id}: {record.commitment_id} (hash verified independently)")

    print("\n--- Committing 1 synthetic case with no result, to prove MISSING_RESULT fires ---")
    synthetic_record = commit_intent(SYNTHETIC_CASE_ID, RUBRIC_VERSION, JUDGE_MODEL, store_path=store_path)
    print(f"  committed {SYNTHETIC_CASE_ID}: {synthetic_record.commitment_id} (fabricated case, no result exists)")

    commitments = load_commitments(store_path)

    # Backdate reconciliation's clock so the synthetic case clears the
    # window in this single-pass demo. Real usage runs reconciliation
    # again after window_hours has actually elapsed.
    reconciliation_now = datetime.now(timezone.utc) + timedelta(hours=25)

    report = reconcile(
        commitments,
        results_by_case_id={cid: {"outcome": outcome} for cid, outcome in REAL_PHASE3A_RESULTS.items()},
        current_rubric_version=RUBRIC_VERSION,
        window_hours=24,
        now=reconciliation_now,
    )

    print("\n--- Reconciliation report ---")
    for f in report.findings:
        print(f"  [{f.status}] {f.case_id} (rubric_at_commit={f.rubric_version_at_commit}, "
              f"outcome={f.result_outcome})")

    reconciled = [f for f in report.findings if f.status == "RECONCILED"]
    print(f"\nReconciled: {len(reconciled)}")
    print(f"Missing:    {len(report.missing)}")

    output = {
        "phase": "phase3_pre_committed_verdicts_demo",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rubric_version": RUBRIC_VERSION,
        "judge_model": JUDGE_MODEL,
        "real_demonstration": {
            "status": "REAL, commitments constructed retroactively against Phase 3a's "
                      "real, already-recorded routing outcomes. Not a live pre-run capture, "
                      "see module docstring.",
            "source": "project-2-llm-evaluation-suite/tests/test_governance_suite.py "
                      "TEST_CASES (expected_outcome) and JUDGE_MODEL",
            "commitments": [asdict(r) for r in real_commitments],
            "reconciliation": [asdict(f) for f in report.findings if f.case_id != SYNTHETIC_CASE_ID],
        },
        "synthetic_demonstration": {
            "status": "SYNTHETIC, fabricated case id with no result anywhere, added only to "
                      "prove the MISSING_RESULT branch fires",
            "commitment": asdict(synthetic_record),
            "reconciliation": [asdict(f) for f in report.findings if f.case_id == SYNTHETIC_CASE_ID],
        },
        "design_notes": {
            "storage": "append-only JSONL, same pattern as Phase 8's hash-chained audit log",
            "hash_helper": "hashing.build_commitment_hash(), a new shared function, not a "
                           "reuse of any of the three build_artifact_hash() notebook variants",
            "known_gap": "commit_intent() is not wired into a live pre-run trigger yet, this "
                        "demo proves the mechanism, not a production pre-registration flow",
        },
    }

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved: {RESULTS_PATH}")

    return output


if __name__ == "__main__":
    run_demo()
