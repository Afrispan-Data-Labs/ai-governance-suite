# Production LLM Evaluation Suite

Project 2 of the python-ai-governance repository. Evaluates whether the
governance system built in Project 1 actually holds up under production
conditions, using Gemini (`gemini-flash-latest`) as the system under test
and Claude (`claude-sonnet-4-6`) as the cross-model evaluator and judge
throughout, a structural implementation of Project 1's same-family
observer bias finding, not just a stated principle.

## Phases

| Phase | Notebook | Focus |
|---|---|---|
| 1 | `01_environment_and_baseline.ipynb` | Toolchain setup, traced baseline RAG pipeline |
| 2a | `02a_ragas_gemini_judge.ipynb` | RAGAS evaluation, Gemini as judge (same-family baseline) |
| 2b | `02b_ragas_claude_judge.ipynb` | RAGAS evaluation, Claude as judge (cross-model) |
| 3a | `03a_deepeval_rag_metrics.ipynb` | DeepEval RAG regression suite, three-queue routing |
| 3b | `03b_deepeval_governance_metrics.ipynb` | G-Eval governance metrics, agentic layer, adversarial cases |
| 4a | `04a_ragas_aspect_critic.ipynb` | AspectCritic evaluation, signed compliance artifacts |
| 4b | `04b_judge_alignment.ipynb` | Judge alignment calibration against human-labeled examples |
| 5a | `05a_promptfoo_owasp_llm.ipynb` | Red-teaming, OWASP LLM Top 10 (2025) |
| 5b | `05b_promptfoo_owasp_agentic.ipynb` | Red-teaming, OWASP Agentic Top 10 (2026), crescendo/multilingual |
| 5c | `05c_mitre_atlas_mapping.ipynb` | MITRE ATLAS v5.4.0 technique mapping, NIST AI RMF report card |
| 6a | `06a_langfuse_custom_scores.ipynb` | Wiring scores into Langfuse, per-source honesty gating |
| 6b | `06b_regression_alarm.ipynb` | Regression alarm, production-sampled trace dataset |
| 7 | `07_synthesis_and_launch.ipynb` | This document |

## Evaluation Suite Status

Every phase of this evaluation suite (Phases 1 through 6b) has a complete,
structurally verified implementation: real tool integrations (RAGAS,
DeepEval, Langfuse, Promptfoo), real bug fixes against actual upstream
package issues (see Known Issues Resolved below), and real architectural
decisions (three-queue routing, cross-model judge independence, signed
compliance artifacts, per-source honesty gating).

Full live evaluation runs are the next scheduled step, pending Gemini and
Claude API billing. The evaluation logic itself does not require further
development to reach that point, it requires execution.

Two phases (5c's MITRE ATLAS mapping and 6a's Langfuse wiring logic) contain
components that are genuinely real and functional today, independent of API
billing: the ATLAS technique mapping is a deterministic lookup table, and
6a's per-source honesty gating logic is real, working code regardless of
whether the scores flowing through it are live or historical. The CI/CD
pipeline is a third: the GitHub Actions workflow has been confirmed running
end to end on live infrastructure, dependencies installing, the test suite
executing, and results publishing successfully as a check run, independent
of whether the underlying tests themselves have API credentials yet.

## Known Issues Resolved

**RAGAS 0.4.x broken Vertex AI import.** `ragas/llms/base.py` in RAGAS 0.4.x
imports `ChatVertexAI` from a location removed after LangChain relocated
that class to `langchain-google-vertexai`. This breaks `import ragas` for
anyone, regardless of whether Vertex AI is used. Resolved by pinning to
`ragas==0.3.9` and, since a stale in-memory import can survive a naive
`pip install` alone, adding a placeholder module shim so the broken import
resolves without pulling in `langchain-google-vertexai`'s own conflicting
protobuf version.

**Gemini embedding model deprecation.** `models/embedding-001` returns a
404 as of this build; the current model is `models/text-embedding-004`.
Caught via a live API error, not assumed from documentation.

**Promptfoo Node.js version requirement.** Promptfoo 0.121.19 requires
Node `^20.20.0` or `>=22.22.0`. Colab's preinstalled Node (v20.19.0) sits
just under this. Resolved with an explicit version check and conditional
upgrade via NodeSource before install.

**Promptfoo CLI command correction.** An initial draft assumed a
`promptfoo eval --dry-run` flag for config validation. No such flag
exists. The correct, documented command is `promptfoo validate config`.

**Crescendo scoring false positive.** A substring check for `"5 million"`
incorrectly matched inside the correct figure `"35 million"`, since the
former is literally a character sequence inside the latter. A plain
`in` string check has no concept of numeric meaning. Fixed by checking
for `"eur 5 million"` specifically, and documented as a concrete example
of why a red-team suite's own scoring logic needs as much scrutiny as
the system it evaluates.

**Structural-absence vs. active-defense distinction.** Several OWASP red-team
categories (denial of service, plugin exploitation, excessive agency, model
theft, and their agentic equivalents) showed as "detected" only because the
baseline pipeline has no capability those attacks target in the first place,
no tool use, no write access, no persistent memory. This is reported
explicitly as an absent attack surface, not counted as active defense, since
conflating the two would overstate the system's real security posture.

## Design Contributions

Three architectural requirements in this project emerged from a LinkedIn
exchange with **Federico Blanco Sanchez-Llanos** (Enforcement Infrastructure
Capital and Compute), cited here in the same way Volodymyr Hlynskyi's
Authority vs Judgment insight was cited in Project 1's capstone.

**Three-queue routing (Phase 3).** Borderline compliance scores route to
human review, not an automatic pass or fail. Confident failures route to
a governance layer; confident passes route to a quality layer. The
principle: uncertainty needs a different owner than a confident miss. The
routing decision itself is logged as its own named event, separate from
the underlying score.

**Signed compliance artifacts (Phase 4).** Compliance verdicts are exported
as artifacts bound to a SHA-256 hash of their specific inputs (prompt,
retrieved documents, rubric), built independently with Python's
`cryptography`/`hashlib` libraries, with no dependency on an external
signing vendor. The critical limitation, stated as clearly as the
mechanism itself: a self-issued hash proves the entry was not altered
after signing. It does not prove that an independent party recomputing
from the same inputs would reach the same verdict.

**Integrity-of-record vs. fidelity-of-judgment (Phase 6).** A hash-chained
or hash-bound log proves tamper-evidence, that a record was not changed
after it was written. It does not prove fidelity of judgment, that the
verdict itself was correct or independently reproducible. Phase 6a's
per-source honesty gating is a direct application of this distinction:
a notebook being technically capable of a live run is never conflated
with the data flowing through it being genuine. Naming this gap plainly
is treated as the governance contribution itself, not a weakness to
obscure.

## Production Deployment Architecture

This section describes how the evaluation suite is wired into CI/CD, extending the notebook-based work above into something a production deployment pipeline can actually run against.

**Status: BUILDING, CI pipeline confirmed live.** Every component below
exists as a real, working file in this repository, and the pipeline itself
has now executed successfully end to end on GitHub Actions, not just
locally. What remains pending funded API credits is narrower and specific:
the 5 tests inside the suite that require a live model call. The pipeline
that runs them, installs them, and reports their result is proven working
today.

**Trigger.** `.github/workflows/deepeval-regression.yml` runs on every pull request touching `project-2-llm-evaluation-suite/`, and can be triggered manually via `workflow_dispatch`. It installs dependencies from `project-2-llm-evaluation-suite/requirements.txt` and runs `project-2-llm-evaluation-suite/tests/test_governance_suite.py` via `deepeval test run`, reporting results as a PR status check.

**Container.** `project-2-llm-evaluation-suite/Dockerfile` packages the full evaluation environment: Node 22.x (installed explicitly, since Promptfoo 0.121.19 requires `^20.20.0` or `>=22.22.0`, above what most base images ship), RAGAS pinned to `0.3.9` (documented workaround for a real upstream import bug), DeepEval, Langfuse, and Promptfoo. API keys and Langfuse credentials are injected as environment variables at container runtime, never baked into the image.

**Merge gate.** `tests/test_governance_suite.py` is not a copy-paste of notebook cells, it is a standalone, pytest-native reimplementation of Phase 03a/03b's real logic: the same `REGULATORY_DOCS` knowledge base, the same `PASS_THRESHOLD`/`FAIL_THRESHOLD` three-queue routing (design addition: Federico Blanco Sanchez-Llanos, Enforcement Infrastructure Capital and Compute, see Design Contributions above), and a real `ClaudeJudge` class implementing DeepEval's documented `DeepEvalBaseLLM` interface, so Claude genuinely judges Gemini's output in this file too, not just in the notebooks. `assert_test`/`assert` failures inside it fail the pytest run, which fails the GitHub Actions check, which blocks the merge.

**Verified today, independent of API billing, on two separate occasions.**
First, locally: the suite's 3 pure-logic routing tests
(`test_routing_pass_threshold`, `test_routing_fail_threshold`,
`test_routing_borderline_zone`) were executed via `pytest` and pass. The 5
API-dependent tests were confirmed to skip cleanly, with an explicit reason,
rather than crash or false-pass, when `GOOGLE_API_KEY`/`ANTHROPIC_API_KEY`
are absent. Second, on live GitHub Actions infrastructure: the same behavior
was reproduced end to end in CI, including a real permissions bug found and
fixed along the way, the result-publishing step initially failed with a 403
Forbidden error because GitHub's default workflow token is read-only unless
explicitly granted write access. Adding an explicit `permissions` block
(`checks: write`, `pull-requests: write`, `contents: read`) resolved it,
confirmed by a fully green run immediately after. This is real, checked
behavior on two independent systems, not an assumption about how either one
would behave.

**What is not yet built.** No scheduled nightly run against production-sampled
traffic exists yet, only the pull-request and manual `workflow_dispatch`
triggers, both confirmed working. The Docker image has not yet been built
or pushed to a registry. The 5 API-dependent tests have never executed
against live models, that remains the one thing genuinely blocked on funded
API credits, not on the CI infrastructure itself.

**First two weeks, IRL Production.** Wiring this existing tooling into Talabat's actual pipeline is a bounded integration task: point the workflow at the real repository, swap in real secrets, and align with the team on where this gate sits relative to their existing checks. The evaluation methodology, the routing design, and the CI scaffolding already exist and are verified. The production wiring is the one remaining connection.
