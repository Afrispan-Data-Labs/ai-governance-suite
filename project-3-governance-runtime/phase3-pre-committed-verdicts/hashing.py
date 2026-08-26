"""Shared hashing helper for Project 3, Phase 3 (pre-committed verdicts).

Status: PROVEN. Verified 2026-08-26: tests/test_commitment.py exercises
this function directly, 8/8 tests in tests/ passed for real, see
data/phase3_demo_results.json for real hash output from a live run.

Same pattern as Project 2's build_artifact_hash() variants in
03b_deepeval_governance_metrics.ipynb, 04a_ragas_aspect_critic.ipynb, and
04b_judge_alignment.ipynb: sort keys, JSON-serialize, SHA-256, hexdigest.
Those three notebook copies are left unmodified, their duplication is a
known cleanup item, not addressed here. This function generalizes the
pattern into one small, reusable piece for Project 3's own field schema.
"""

import hashlib
import json


def build_commitment_hash(fields: dict) -> str:
    """Return a SHA-256 hex digest over fields, sorted-key JSON encoded."""
    return hashlib.sha256(json.dumps(fields, sort_keys=True).encode()).hexdigest()
