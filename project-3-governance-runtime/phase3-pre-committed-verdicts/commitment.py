"""Commit step for Project 3, Phase 3: pre-committed verdicts.

Status: PROVEN. Verified 2026-08-26: tests/test_commitment.py passed
(4/4), and demo.py committed and independently hash-verified 5 real
Phase 3a intents plus 1 labeled synthetic intent in a real run. See
data/phase3_demo_results.json for the actual output.

Commits a record of intent to evaluate a case, before the evaluation's
outcome is known, to an append-only JSONL store. The commitment hash
covers only the plaintext fields known at commit time (commitment id,
case id, rubric version, judge model, timestamp), so it can be
independently recomputed and verified without running the evaluation
itself.

Design constraint (PHASE_3_4_SPEC.md): the commit step and the
reconciliation step are separable. This module only writes commitments,
it never checks for or waits on a result. See reconciliation.py for that.

Storage decision: an append-only JSONL file, following the same pattern
as Phase 8's hash-chained audit log, rather than Langfuse or a database.
Tradeoff, stated plainly: this has no concurrent-writer safety and no
query performance at scale, acceptable for this repo's real data volumes,
not something that would hold up for a real production caseload without
becoming an actual database first.
"""

import json
import os
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

from hashing import build_commitment_hash

DEFAULT_STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "commitments.jsonl")


@dataclass
class CommittedIntent:
    commitment_id: str
    case_id: str
    rubric_version: str
    judge_model: str
    committed_at: str
    hash: str


def commit_intent(case_id: str, rubric_version: str, judge_model: str,
                   store_path: str = DEFAULT_STORE_PATH) -> CommittedIntent:
    """Build and append one committed-intent record. Returns the record."""
    hash_fields = {
        "commitment_id": str(uuid.uuid4()),
        "case_id": case_id,
        "rubric_version": rubric_version,
        "judge_model": judge_model,
        "committed_at": datetime.now(timezone.utc).isoformat(),
    }
    record = CommittedIntent(**hash_fields, hash=build_commitment_hash(hash_fields))

    os.makedirs(os.path.dirname(store_path), exist_ok=True)
    with open(store_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record)) + "\n")

    return record


def verify_commitment(record: dict) -> bool:
    """Independently recompute the hash from a commitment's plaintext
    fields and confirm it matches the stored hash. Does not require the
    evaluation the commitment refers to to have ever run."""
    hash_fields = {k: record[k] for k in
                   ("commitment_id", "case_id", "rubric_version", "judge_model", "committed_at")}
    return build_commitment_hash(hash_fields) == record["hash"]


def load_commitments(store_path: str = DEFAULT_STORE_PATH) -> list:
    if not os.path.exists(store_path):
        return []
    with open(store_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
