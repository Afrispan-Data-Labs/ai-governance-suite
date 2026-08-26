# Project History: Full Detail for Projects 1 and 2

Read this before modifying anything in `phase1-foundations/` through `phase9-portfolio-launch/`, `project-2-llm-evaluation-suite/`, or before building Project 3 features that depend on their real output. Every number and finding below is real and was independently verified during the original build, not approximated.

## Project 1: Nine Phases, Governance Principles Discovered

Executed against real Gemini API calls throughout. All notebooks include saved outputs.

| Phase | Focus | What Was Built | Key Finding |
|---|---|---|---|
| 01 | Python Foundations | Core language skills for AI evaluation work | |
| 02 | Data Handling & Visualization | Pandas, Matplotlib, structured evaluation output | |
| 03 | LLM Evaluation | Consistency testing, prompt sensitivity, LLM-as-judge | Same-family evaluator bias first appears: Gemini scoring Gemini produced near-perfect, structurally lenient scores |
| 04 | Red-Teaming & Safety Analysis | Adversarial testing across 8 attack vectors | Keyword classifier hit 28% accuracy, missed a research-framing attack that produced 1,095 words of harmful content |
| 05 | Bias Auditing & EU AI Act Compliance | Disparate impact ratios | Age 0.20, gender 0.43, ethnicity 0.80. Qualitative linguistic bias also found in generated text |
| 06 | Function Calling & Tool-Use Auditing | Agentic tool-use safety testing | A tool-calling system silently remapped an unrecognized input to the nearest known category instead of flagging it |
| 07 | RAG, Observer Agent & Semantic Intent Check | Three-layer agentic pipeline | Same-family Observer bias confirmed in a second, independent system. Semantic classifier built to fix Phase 4's failure hit 88-100% accuracy but introduced non-determinism on borderline cases |
| 08 | Multi-Agent Governance & Kill-Switch | Real human-in-the-loop kill-switch, SHA-256 hash-chained audit log | Kill-switch halts execution completely on breach detection. Requires a substantive documented position before resuming, not a reflexive click. Live demonstration: 4 minutes 33 seconds between breach detection and abort decision |
| 09 | Portfolio Synthesis & Regulatory Suite | FRIA template, Conformity Report, Cross-Border Framework, capstone synthesis | See regulatory suite table below |

### Project 1's Regulatory Documentation Suite (Phase 9)

Built as general-purpose generators, not one-off scripts.

- **FRIA Template**: generates a Fundamental Rights Impact Assessment per critical breach, not per audit. Accepts automated evidence from a real audit log (`from_audit_log()`) or manual client intake (`intake_fria()`). Every field tagged `AUTOMATED`, `ATTESTED`, or `MISSING`. Design rule: a value with no cited source is never accepted as evidence, regardless of intake path.
- **Conformity Report**: scores a system against 22 obligations across EU AI Act, NIST AI RMF, NIST AI 600-1, and ISO/IEC 42001 in one report. Untested obligations marked `NOT_ASSESSED`, never silently omitted.
- **Cross-Border Framework**: tests whether EU AI Act and NIST evidence transfers to Nigeria (NDPA 2023) and Canada. Honest finding: most of it does not. Canada's AIDA died with Bill C-27 in January 2025, no binding federal AI law exists there as of this writing. Nigeria's NDPA Section 37 transfers cleanly for human oversight; most other obligations only partially transfer.
- **AI Governance in Practice**: the capstone document synthesizing all nine phases and naming the five recurring principles (see CLAUDE.md).

## Project 2: Thirteen Notebooks, a Production Evaluation Architecture

Real architectural decision made in Phase 1, before any evaluation metric existed: two separate model clients, Gemini always the system under test, Claude always the judge, never reversed.

| Phase | Focus | Key Finding |
|---|---|---|
| 01 | Environment & Baseline | Dual-client architecture. Langfuse tracing wired in before the pipeline had run once. The only notebook executed for real, not simulated. A real live test query returned a grounded refusal rather than a hallucinated answer |
| 02a | RAGAS, same-family judge | Gemini judging Gemini: near-perfect scores, zero variance across all test samples |
| 02b | RAGAS, cross-model judge | Claude judging identical Gemini output: 0.15 point average quality inflation and 0.23 point noise-detection gap measured against the same-family baseline |
| 03a | DeepEval RAG regression suite | Three-queue routing (`PASS_THRESHOLD = 0.80`, `FAIL_THRESHOLD = 0.60`, `route_result()` function). 5/5 outcome accuracy. `tc_004` caught a hallucinated EUR 50 million penalty figure (correct: EUR 35 million) |
| 03b | DeepEval governance metrics | G-Eval criteria for EU AI Act Articles 10 and 14. Signed SHA-256 artifacts (`build_artifact_hash()`). ToolCorrectness and TaskCompletion agentic metrics. 7/7 outcome accuracy |
| 04a | RAGAS AspectCritic | Six aspects scored as binary yes/no. Pre-calibration alignment: 83.3% (5/6). `as_006` disagreement: judge said PASS, human said BORDERLINE, on a response accurate but not actionably complete |
| 04b | Judge alignment calibration | Diagnosed `as_006` as a rubric gap, not a judge error. Added a sixth aspect, `coverage_completeness`. Post-calibration alignment: 100% (6/6) |
| 05a | Promptfoo, OWASP LLM Top 10 | 10/10 categories detected, but 4 were structural absence (no attack surface existed), not active defense |
| 05b | Promptfoo, OWASP Agentic Top 10 | 12/12 detected after fixing a real bug: a substring check flagged the correct "EUR 35 million" as compromised because it contains the digits of a shorter, wrong "5 million" |
| 05c | MITRE ATLAS mapping | Deterministic lookup table, not an LLM call. 11 direct matches, 7 interpretive, 2 unresolved, confidence reported honestly rather than uniformly |
| 06a | Langfuse per-source honesty gating | A score is only pushed live if both the current notebook and its original source were genuinely real. All 9 upstream sources checked: 0 real, correctly reported as such, not laundered into looking genuine |
| 06b | Regression alarm | `check_governance_drift()`: WARNING at a 5-point drop, ALARM at a 10-point drop, using a rolling baseline. Proven correct at both phase level and individual case level using clearly labeled synthetic and real data |
| 07 | Synthesis | Full status inventory. Deliberately deferred LinkedIn and Medium capstone content until real findings existed to write about |

### Project 2's CI/CD Layer

Real files: `project-2-llm-evaluation-suite/Dockerfile`, `.github/workflows/deepeval-regression.yml`, `project-2-llm-evaluation-suite/tests/test_governance_suite.py`.

- `ClaudeJudge(DeepEvalBaseLLM)`: a real class implementing DeepEval's model-wrapper interface so Claude genuinely judges inside the CI-runnable file, not only inside notebooks.
- Verified live: 3 pure-logic routing tests pass for real. 5 API-dependent tests skip cleanly with a stated reason, rather than crash or false-pass, when API keys are absent.
- Real bug found and fixed: the workflow initially failed with a 403 Forbidden on the results-publishing step. Root cause: GitHub's default workflow token is read-only unless explicitly granted more. Fix: a `permissions` block (`checks: write`, `pull-requests: write`, `contents: read`). Confirmed by a fully green run immediately after.

### Design Contributions from Federico Blanco Sanchez-Llanos (Enforcement Infrastructure Capital and Compute)

Real, named, LinkedIn-sourced design exchanges, not invented attributions:

1. **Three-queue routing** (Phase 3): uncertainty needs a different owner than a confident miss.
2. **Signed-artifact mechanism** (Phase 3b): integrity of record is checkable, but is not the same claim as fidelity of judgment. A self-issued hash proves a record was not altered after signing; it does not prove an independent party recomputing from the same inputs would reach the same verdict.
3. **The integrity-of-record versus fidelity-of-judgment distinction itself** (Phase 6a): naming this gap explicitly is treated as the governance contribution, not a weakness to smooth over.
4. **Pre-committed verdicts** (not yet built): a real, still-open gap. Current honesty gating checks whether a recorded score's source was genuine. It has no answer for whether a real, unfavorable score could have simply never been recorded in the first place. The fix: commit to an evaluation's existence, which case, which rubric, which model, before its outcome is known, so publication is guaranteed regardless of what it says. This is the subject of Project 3, Phase 3. See `project-3-governance-runtime/PHASE_3_4_SPEC.md`.

## Project 3: What Already Exists

Two n8n workflows, exported as JSON in `project-3-governance-runtime/n8n-workflows/`. Full architecture in that folder's own README. Summary:

**Workflow 1** operationalizes Phase 3's three-queue routing as live, non-blocking infrastructure. A PR verdict routes to confident auto-merge, confident auto-reject with a failure tag fed into the regression suite, or a BORDERLINE human review queue (Slack and email, a real Wait node, an If branch resolving merge or reject). Only the flagged case waits; every other event keeps routing unaffected.

**Workflow 2** extends Phase 8's kill-switch into live orchestration, converging Phase 6's regression alarm and Phase 5's red-team findings into one shared gate. The halt itself, a GitHub Action disabling automatic merge, fires first and independently, before any notification goes out. A Continue On Fail branch guarantees the named accountable person is notified whether the halt succeeds or fails. Resuming requires the same substantive, recorded decision standard Phase 8 proved, checked directly, not a boolean approval.

Both workflows were reviewed and corrected through several real iterations, including catching and fixing a genuine ordering bug where the halt action originally fired downstream of the notifications rather than before them.
