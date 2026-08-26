# Project 3: Phase 3 and Phase 4 Build Spec

Read `CLAUDE.md` and `docs/PROJECT_HISTORY.md` first. This document is the actionable spec for the two remaining planned phases. Phases 1 and 2 (the two n8n workflows in this folder) are already built; do not modify them without a specific reason, and if a change to either is genuinely required for Phase 3 or 4 to work, state why before making it.

---

## Phase 3: Pre-Committed Verdicts

### The gap this closes

Federico Blanco Sanchez-Llanos's fourth named design contribution, real and still open. Phase 6a's honesty gating (Project 2) checks whether a recorded score's source was genuine. It has no answer for whether a real, unfavorable score could have simply never been recorded in the first place. A signed artifact (Phase 3b) proves a record was not altered after signing; it says nothing about records that were never created.

The fix, in Federico's own framing: commit to an evaluation's existence, which case, which rubric, which model, before its outcome is known, so the verdict's publication is guaranteed regardless of what it says. The AI-evaluation equivalent of clinical trial pre-registration.

### Functional requirement

Before any evaluation runs (a DeepEval test case, a RAGAS score, a red-team payload check), commit a record of intent to a durable, append-only store. That record must include, at minimum:
- A unique identifier for the evaluation about to run.
- The case or payload identifier being evaluated.
- The rubric or criteria version being applied (see versioning note below).
- The judge model being used.
- A timestamp.
- A hash of the above, computed the same way `build_artifact_hash()` already does in Phase 3b, for consistency with the existing signed-artifact pattern.

After the evaluation completes, the actual result must be reconciled against this pre-committed record. A reconciliation process (can be a scheduled check, does not need to be real-time) must be able to answer: for every committed intent, does a corresponding result exist? Any committed intent with no corresponding result after a reasonable window is itself a finding, surfaced explicitly, not silently dropped.

### Design constraints

- Reuse the existing SHA-256 hashing pattern from Phase 3b's `build_artifact_hash()` rather than inventing a new hashing approach.
- The commit step and the reconciliation step should be genuinely separable, the commit must be possible to verify independently of whether the evaluation that follows ever actually completes.
- Do not build this as an n8n workflow node performing evaluation logic. If orchestration is needed (for example, triggering the reconciliation check on a schedule), that is a legitimate use of the existing n8n instance, following the same principle already established for Phase 2: n8n orchestrates, it does not compute scores or judge quality itself.
- Rubric versioning: if a rubric changes between when a verdict was committed and when it was reconciled, the reconciliation must reference which rubric version was actually committed to, not silently assume the current one.

### Acceptance criteria

- A committed intent record can be created and independently verified (hash matches) without running the evaluation itself.
- A completed evaluation can be reconciled against its prior committed intent.
- A committed intent with no corresponding result is surfaced as a named finding, not silently ignored, in whatever reporting mechanism is built.
- The mechanism is demonstrated against at least one real, already-existing evaluation path from Project 2 (for example, a Phase 3a or 3b test case), not only a synthetic example built solely to prove the mechanism.

### Honest open question, do not resolve by assumption

Where committed-intent records should actually live (a Langfuse custom event, a separate lightweight database, a file-based log) has not been decided. Propose an approach and state the tradeoff explicitly rather than picking one silently.

---

## Phase 4: Bird's-Eye-View Dashboard

### The gap this closes

A real, honestly-named gap from the Talabat interview preparation work: no single view exists across the systems this evaluation architecture governs. Per-system tracing exists (Langfuse), but nothing aggregates across systems into one place a non-technical reader could scan.

### Functional requirement

A read-only dashboard, pulling from Langfuse's own API (or a store fed by it), showing at minimum:
- Pass, borderline, and fail rates over time, matching Phase 3a's three-queue categories.
- Judge alignment trend, referencing Phase 4b's alignment methodology, not a one-time snapshot.
- Regression alarm status, referencing Phase 6b's severity tiers (OK, WARNING, ALARM).
- A drill-down view for any individual verdict showing its signed artifact hash and the inputs that produced it, per Phase 3b's pattern.

### Design constraints, stated plainly because they were gotten wrong once already

**Do not build this in n8n.** Workflow nodes are the wrong tool for rendering visualizations; this was corrected once already in this project's design history and should not be repeated. n8n's only legitimate role here is a scheduled job that polls Langfuse (or another source) and writes normalized data somewhere the dashboard reads from, feeding the dashboard, never rendering it.

Build the dashboard itself as a proper frontend. Streamlit is the lower-effort option and is consistent with the kind of tooling already used elsewhere in this portfolio's practical work; a small React app is the more capable option if genuine interactivity is needed. Choose one and state why, do not build both.

### Acceptance criteria

- The dashboard runs locally and displays real data pulled from at least one genuinely existing Project 2 evaluation run, not entirely synthetic placeholder data.
- No visualization logic lives inside an n8n workflow.
- A viewer can go from the aggregate view to a single verdict's signed artifact detail without needing to open a notebook or query Langfuse directly.

### Honest open question, do not resolve by assumption

Whether this dashboard needs authentication or access control before it could ever be shown to anyone outside this project has not been decided. For a personal portfolio demonstration, it likely does not. Note this limitation explicitly in the dashboard's own README rather than silently building it as if that question does not exist.

---

## Before Starting Either Phase

Confirm the following are true by actually checking, not assuming:
1. The two existing n8n workflows in this folder still export cleanly and match the description in `PROJECT_HISTORY.md`.
2. Project 2's `check_regression()` and `build_artifact_hash()` functions exist and run as described, since both phases above depend on reusing them, not reimplementing them.
3. Langfuse credentials and access are available in whatever environment this is being built in.

If any of these are not true, stop and report exactly what was found rather than working around the discrepancy silently.
