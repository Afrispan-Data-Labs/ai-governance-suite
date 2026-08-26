# Phase 3: Pre-Committed Verdicts

Status: PROVEN. Verified 2026-08-26: `pytest tests/` passed 8/8, and `demo.py` ran for real, committing and reconciling all 5 real Phase 3a test cases correctly and surfacing the 1 labeled synthetic case as `MISSING_RESULT`. Real output saved at `data/phase3_demo_results.json`.

## What this closes

Federico Blanco Sanchez-Llanos's fourth named design contribution. Phase 3b's signed-artifact mechanism (`build_artifact_hash()`) proves a recorded verdict was not altered after signing. It says nothing about a real, unfavorable verdict that was simply never recorded in the first place. This phase commits to an evaluation's existence, case, rubric version, and judge model, before its outcome is known, so publication is guaranteed regardless of what the result says. Full spec: [`../PHASE_3_4_SPEC.md`](../PHASE_3_4_SPEC.md).

## Files

- `hashing.py`: `build_commitment_hash(fields: dict) -> str`. A new, small, shared helper (sort keys, JSON-serialize, SHA-256, hexdigest), the same pattern Project 2's three `build_artifact_hash()` notebook variants each implement separately. Those three are left unmodified; their duplication is a known cleanup item, not addressed here.
- `commitment.py`: `commit_intent()` appends a committed-intent record to an append-only JSONL store. `verify_commitment()` independently recomputes the hash from a record's plaintext fields, no evaluation run required.
- `reconciliation.py`: `reconcile()` compares committed intents against actual results. Each commitment is `RECONCILED`, `PENDING` (within the reconciliation window, no result yet), or `MISSING_RESULT` (past the window, no result, a named finding, never silently dropped).
- `demo.py`: demonstrates the mechanism against Project 2's five real Phase 3a test cases, plus one clearly labeled fabricated case that proves the `MISSING_RESULT` branch fires. Writes `data/phase3_demo_results.json`.
- `tests/`: pytest unit tests for both modules, pure logic, no API keys or network access required.

## Storage decision

An append-only JSONL file (`data/commitments.jsonl`), not Langfuse and not a database. This follows the same pattern Phase 8 already proved in this repo for a structurally identical need: a record that must be independently verifiable and never quietly rewritten.

Tradeoff, stated plainly: a flat file has no concurrent-writer safety and no query performance at scale. That is acceptable for this repo's real data volumes. It would need to become an actual database before this held up for a real production caseload.

## Honest limitations

- The Phase 3a demonstration commits are constructed retroactively against results that already existed, since Phase 3a already ran before this phase was built. This proves the commit/reconcile mechanism is correct against real data. It is not a true prospective pre-registration capture. Wiring `commit_intent()` into an actual live pre-run trigger is future work, not built here.
- `"faithfulness_geval_v1"` is a rubric-version string introduced by this phase. Project 2 never had a formal rubric-versioning scheme before this.
- No n8n workflow is built in this phase. A scheduled trigger calling `reconcile()` is a legitimate future hook per the spec, deferred until Phase 4's dashboard needs to consume reconciliation output.
