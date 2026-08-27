# AI Governance & Agentic Audit Suite

**A Working Regulatory Evidence Engine for EU AI Act, NIST AI RMF, and Cross-Border Deployer Compliance, Now Extended to Live Governance Orchestration**

This repository is the technical foundation of Afrispan Data Labs, an AI deployment assurance practice for SMEs, built first for Africa. It is not a teaching log. It is a working evidence suite spanning three projects: governance principles discovered and proven (Project 1), a production evaluation architecture built and pytest-verified (Project 2), and that architecture wired into live orchestration infrastructure that actually acts on what it finds (Project 3).

Every claim in this README is backed by code in this repository, real measured output, or both, and is tagged clearly where execution status differs. Nothing here is aspirational.

## What This Repository Actually Proves

Five governance principles recur across all three projects, found by direct testing, not assumed in advance:

**An AI system cannot audit itself.** Project 1, Phase 3 found that Gemini scoring Gemini's own text output produced near-perfect, structurally lenient scores. Phase 7 found the identical pattern in an Observer Agent auditing a RAG pipeline built on the same model family. Project 2, Phase 2 measured the same failure with a real number: a same-family judge produced a 0.15 point quality inflation and a 0.23 point noise-detection gap against a cross-model judge, on identical output. The fix is structural, not a better prompt: a different model family must do the auditing, decided architecturally before a single metric existed.

**Surface pattern-matching fails at the edges, in every form it takes.** Project 1, Phase 4's keyword classifier hit 28% accuracy and missed a research-framing attack that produced 1,095 words of harmful content. Project 2's own red-team detection logic repeated the lesson from the other side: a substring check flagging a correct EUR 35 million figure as compromised because it contained the digits of a shorter, wrong number, the bug was in the detection code, not the system under test.

**Monitoring is not governing.** A system that detects a critical breach and keeps running is a monitor. Project 1, Phase 8's kill-switch halts execution completely the instant a breach is detected, and nothing resumes until a named human resolves it. Project 3 makes this a live, running mechanism: a regression alarm or a confirmed red-team finding disables automated merging immediately, independent of any notification, closing the exact gap between detecting a problem and actually stopping it.

**Authority is not judgment.** Before Project 1, Phase 8's kill-switch accepts a human override, it surfaces the specific breach, the article of law violated, and the quantified legal exposure, then requires a substantive documented position before execution can resume. In the live demonstration, 4 minutes and 33 seconds elapsed between breach detection and the abort decision, measurable evidence of real engagement, not a reflexive click. Project 3's kill-switch workflow enforces the identical standard live: resuming requires a recorded, substantive decision from a named person, checked directly, not a boolean approval.

**Disagreement between a judge and a human is diagnostic, not noise.** Project 2, Phase 4 found a real disagreement, a judge passed a response a human called borderline, and rather than tuning a threshold to make the disagreement go quiet, the rubric itself was diagnosed as incomplete. Adding the missing dimension moved alignment from 83.3% to 100%, not because the judge improved, because the evaluation criteria became honest about what they were checking.

## Project Structure

| Project | Focus | Status |
|---|---|---|
| **Project 1** | Governance principles, discovered through nine phases of testing | Complete, executed against real Gemini API calls throughout |
| **Project 2** | Production LLM evaluation architecture: cross-model judging, red-teaming, drift monitoring, CI/CD | Architecture complete and pytest-verified; most notebooks run in simulated mode pending funded API billing, CI/CD layer confirmed live |
| **Project 3** | Governance orchestration: the evaluation logic wired into live infrastructure that acts | All four phases built and reviewed end to end. Phases 1 to 2 pending live deployment against a real repository; Phases 3 to 4 verified against real historical data from Projects 1 and 2, not yet wired to live Langfuse traces |

---

## Project 1: Governance Principles

The Nine Phases

| Phase | Focus | What Was Built |
|---|---|---|
| 01 | Python Foundations | Core language skills for AI evaluation work |
| 02 | Data Handling & Visualization | Pandas, Matplotlib, structured evaluation output |
| 03 | LLM Evaluation | Consistency testing, prompt sensitivity, LLM-as-judge, first appearance of same-family evaluator bias |
| 04 | Red-Teaming & Safety Analysis | Adversarial testing across 8 attack vectors, 28% keyword classifier accuracy exposed |
| 05 | Bias Auditing & EU AI Act Compliance | Disparate impact ratios (age 0.20, gender 0.43, ethnicity 0.80), qualitative linguistic bias found in generated text |
| 06 | Function Calling & Tool-Use Auditing | Agentic tool-use safety testing, silent input-remapping risk discovered |
| 07 | RAG, Observer Agent & Semantic Intent Check | Three-layer agentic pipeline, same-family Observer bias confirmed, classifier non-determinism documented |
| 08 | Multi-Agent Governance & Kill-Switch | Real human-in-the-loop kill-switch, immutable SHA-256 hash-chained audit log, authority-vs-judgment enforcement |
| 09 | Portfolio Synthesis & Regulatory Suite | Code optimization, FRIA template, Conformity Report, Cross-Border Framework, capstone synthesis |

**The Regulatory Documentation Suite** (Phase 9), built as general-purpose generators, not one-off scripts:

| Deliverable | What It Does |
|---|---|
| FRIA Template | Generates a Fundamental Rights Impact Assessment per critical breach, not per audit. Tags every field AUTOMATED, ATTESTED, or MISSING. |
| Conformity Report | Scores a system against 22 obligations across EU AI Act, NIST AI RMF, NIST AI 600-1, and ISO/IEC 42001 at once. Untested obligations marked NOT ASSESSED, never silently omitted. |
| Cross-Border Framework | Tests whether EU AI Act and NIST evidence actually transfers to Nigeria (NDPA 2023) and Canada. Honest finding: most of it does not. |
| AI Governance in Practice | Capstone synthesis, all nine phases, naming the recurring findings above as principles, not isolated bugs. |

All nine phases were executed against real Gemini API calls. Full detail: `AI_Governance_in_Practice.docx`.

---

## Project 2: Production LLM Evaluation Suite

Thirteen notebooks across seven phases plus a CI/CD layer, built to answer a harder question than Project 1 asked: not just "can a system be governed," but "what does it actually take to prove it."

| Phase | Focus | Key Finding |
|---|---|---|
| 01 | Environment & Baseline | Dual-client architecture, Gemini as system under test, Claude as judge, decided before any metric existed. The only notebook executed for real, live-traced in Langfuse. |
| 02a/02b | RAGAS Same-Family Bias | 0.15 point quality inflation, 0.23 point noise-detection gap, same-family versus cross-model judging on identical output. |
| 03a/03b | DeepEval Regression Suite | Three-queue routing (pass/borderline/fail), a caught hallucination citing a fabricated EUR 50M penalty figure, signed SHA-256 artifacts with the limitation stated as plainly as the mechanism. |
| 04a/04b | Judge Alignment | A real judge/human disagreement diagnosed as a rubric gap, not a judge error. Alignment moved from 83.3% to 100% after adding the missing dimension. |
| 05a/05b/05c | Red-Teaming & MITRE ATLAS | OWASP LLM and Agentic Top 10 mapped to MITRE ATLAS with confidence tiers (direct, interpretive, unresolved). A real substring bug found in the detection logic itself, not the system under test. |
| 06a/06b | Drift Monitoring | Per-source honesty gating (0 of 9 sources verified real, correctly reported as such) and a regression alarm proven at both phase and case level. |
| 07 | Synthesis | Full status inventory, honest register of what's proven versus pending. |

**CI/CD layer:** a real GitHub Actions workflow, Dockerfile, and pytest suite, confirmed running end to end on live infrastructure, not just locally. A real 403 Forbidden permissions error was found and fixed along the way, GitHub's default workflow token is read-only unless a workflow explicitly requests more. Three pure-logic routing tests pass for real; five API-dependent tests skip cleanly with a stated reason rather than crash or false-pass.

**Design contributions from a real exchange with Federico Blanco Sanchez-Llanos**, Enforcement Infrastructure Capital and Compute: three-queue routing, the signed-artifact mechanism, the integrity-of-record versus fidelity-of-judgment distinction, and a fourth, pre-committed verdicts, built in Project 3, Phase 3, described below.

**Execution status:** the evaluation architecture is complete and pytest-verified everywhere testable without live model calls. Most notebooks run in `SIMULATED_OUTPUT` mode pending funded Gemini and Claude API billing. The CI/CD layer and Phase 1's baseline test are the exceptions, both genuinely executed, not simulated.

---

## Project 3: Governance Runtime

Where Project 2 built the evaluation logic, Project 3 gives it the one thing evaluation logic never has on its own: a way to act on what it finds. Built as four phases, closing specific, honestly-named gaps left open across Projects 1 and 2, not a new theme invented separately.

### Built: Phases 1 to 4

**Phase 1, Workflow 1: Three-Queue Routing, Made Real**
A PR verdict from an independent council of LLM judges routes to confident auto-merge, confident auto-reject with a structured failure tag fed into the regression suite, or a borderline human review queue via Slack and email, held open by a real Wait node. Only the flagged case waits, every other event keeps routing unaffected, a non-blocking design that matters at real scale.

**Phase 2, Workflow 2: Kill-Switch and Regression Alarm, Converged**
Two genuinely different trigger types, a Langfuse regression alarm watching for drift over time, and a kill-switch halt firing on a confirmed, high-severity red-team finding mapped to OWASP or MITRE ATLAS, converge into one shared decision gate rather than duplicating logic twice. The halt itself, a GitHub Action disabling automated merges repository-wide, fires immediately and independently, before any notification. A Continue On Fail branch guarantees the named accountable person is notified whether the halt succeeds or fails. Resuming requires a substantive, recorded human decision, the actual standard behind EU AI Act Article 14, checked directly, not a single approval click.

Full detail: [`project-3-governance-runtime/n8n-workflows/README.md`](./project-3-governance-runtime/n8n-workflows/README.md)

**Execution status:** both workflows built and reviewed end to end, including the immediate-halt fix and the failure-safe notification guarantee. Live production traffic pending deployment against a real repository.

### Built: Phases 3 to 4

**Phase 3, Pre-Committed Verdicts.** Closes the fourth Federico Blanco Sanchez-Llanos design contribution, a real gap Phase 2's honesty gating never answered: it checks whether a recorded score's source was genuine, but has no answer for whether a real, unfavorable score could have simply never been recorded in the first place. Commits a record of an evaluation's existence, case, rubric version, and judge model, before its outcome is known, to an append-only JSONL store, the same hash-chained pattern Project 1, Phase 8's audit log already proved, then reconciles committed intents against actual results, surfacing any intent with no result past a window as a named `MISSING_RESULT` finding rather than dropping it silently. Demonstrated against Project 2's five real Phase 3a test cases: all 5 real commitments reconciled correctly, and one clearly labeled synthetic case proved the `MISSING_RESULT` branch actually fires. Honest limitation: these commitments are constructed retroactively against results that already existed, since Phase 3a already ran before this phase was built, not a live pre-run capture. Full detail: [`project-3-governance-runtime/phase3-pre-committed-verdicts/README.md`](./project-3-governance-runtime/phase3-pre-committed-verdicts/README.md)

**Phase 4, Bird's-Eye-View Dashboard.** A named, honestly-flagged gap closed: one unified, read-only Streamlit view across pass/borderline/fail rates, judge alignment trend, regression alarm status, and a hash-verified verdict drill-down, rather than per-system traces alone. Streamlit was chosen over React, no existing frontend or JS tooling exists anywhere in this all-Python portfolio, and none of the four panels need more interactivity than Streamlit provides natively. Built against a local data store fed by real evidence, Phase 3a's real test outcomes, Phase 4a/4b's real calibration numbers, 06b's real saved regression output, and Phase 3's own real commitment records, rather than a live Langfuse API pull: no Langfuse credentials exist in this environment, and Project 2's Phase 06a already found 0 of 9 upstream sources ever pushed genuinely live to Langfuse. Two honest limitations render as visible badges directly inside the dashboard, not only in documentation: the regression panel is sourced from a saved notebook snapshot, not a live recomputation, and the judge alignment panel has exactly two real data points, not a continuous trend. No authentication, stated plainly rather than silently absent, acceptable for a personal portfolio demo. Full detail: [`project-3-governance-runtime/phase4-dashboard/README.md`](./project-3-governance-runtime/phase4-dashboard/README.md)

**Execution status, Phases 3 to 4:** both phases are real, tested Python, not notebooks. Verified by actually running the code: `pytest` passes 8/8 for Phase 3 and 5/5 for Phase 4, `demo.py`'s output and `data_store.py`'s output were inspected directly, and the dashboard was exercised in a live browser check, all four panels, both honesty badges, and the drill-down selector confirmed working against real data. Not yet connected to live Langfuse traces, since none currently exist in this project to connect to. All four phases depend on Phases 1 and 2's real infrastructure and real findings rather than starting new logic or fabricated data from scratch.

---

## Tech Stack

**Language:** Python, JavaScript (n8n workflow logic)
**Data & Visualization:** Pandas, Matplotlib, NumPy
**Evaluation, Project 1:** Gemini API (`gemini-flash-latest`), Google Colab
**Evaluation, Project 2:** Gemini (system under test), Claude (cross-model judge), RAGAS, DeepEval, Langfuse, Promptfoo
**Orchestration, Project 3:** n8n, GitHub Actions API, Slack API, Gmail API
**Dashboard, Project 3 Phase 4:** Streamlit
**Vector Search:** Chroma
**Agent Orchestration:** Pure Python for the production governance pipeline (Phase 8); a minimal, explicitly non-production LangGraph demonstration exists in Project 1, Phase 9 as a scoped technical exploration, not an adopted upgrade
**CI/CD:** GitHub Actions, Docker, pytest
**Documentation Generation:** docx (Node.js) for brand-styled capstone documents

## Running the Code

Project 1 and Project 2 notebooks require a Google Gemini API key (free tier available at aistudio.google.com) added to Colab secrets as `GOOGLE_API_KEY`. Project 2 additionally requires an Anthropic API key as `ANTHROPIC_API_KEY` for the cross-model judge. All notebooks include saved outputs, so results can be reviewed without re-running the code.

Project 3, Phases 1 to 2 are n8n JSON exports, importable directly into any n8n instance via Workflows → Import from File. Credentials for GitHub, Slack, and Gmail must be configured separately, none are stored in the exported files.

Project 3, Phases 3 to 4 are plain Python, no notebook or n8n instance required. From `project-3-governance-runtime/phase3-pre-committed-verdicts/`, run `pytest tests/` then `python demo.py`. From `project-3-governance-runtime/phase4-dashboard/`, run `python data_store.py` then `streamlit run app.py`, Phase 3's `demo.py` must be run first so the drill-down panel has real commitment records to show.

## Connect

Steve Onyeke | Founder, Afrispan Data Labs | AI Quality Analyst, Turing

LinkedIn | GitHub
