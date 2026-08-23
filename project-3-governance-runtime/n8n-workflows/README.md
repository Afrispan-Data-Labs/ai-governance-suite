# n8n Governance Workflows

Two production n8n workflows that turn Project 2's evaluation logic into infrastructure that actually acts on what it finds, not just scores it. Built on the principle that evaluation logic which never triggers a real action isn't governance, it's a dashboard.

## Workflow 1: Three-Queue Routing

Routes every pull request verdict from an independent council of LLM judges into one of three outcomes, non-blocking, so no single case slows down the rest of the pipeline.

- **Confident pass** → auto-merges immediately via GitHub Action, zero human involvement.
- **Confident fail** → PR is closed and tagged with a structured failure record, fed into the regression suite as a permanent test case so the same failure mode can't silently reopen.
- **Borderline** → routes to a human reviewer via Slack and email. A Wait node holds that specific case open until a decision is recorded. Every other PR keeps routing in parallel, unaffected.

The judge council itself runs on the DeepEval and RAGAS scoring logic built in Project 2.

## Workflow 2: Kill-Switch and Regression Alarm

Converges two genuinely different trigger types into one shared human-decision gate, rather than duplicating the same logic twice.

- **Regression alarm**, sourced from Langfuse, fires when evaluation metrics drift over time, judge alignment or faithfulness degrading gradually.
- **Kill-switch halt** fires on a confirmed, high-severity single event, an adversarial payload mapped to OWASP or MITRE ATLAS actually succeeding against a defense it was supposed to fail.

Both triggers disable automatic merging repository-wide first, immediately, independent of any notification. Whether that halt action succeeds or fails, the named accountable person is notified either way, via a Continue On Fail branch, so a failed halt can never also mean a missed alert.

Resuming requires a substantive, recorded human decision, not a single approval click, the standard behind EU AI Act Article 14. The workflow checks for genuine interaction before re-enabling automated merges.

## How This Connects to Projects 1 and 2

Neither workflow contains its own evaluation logic. They orchestrate decisions already produced elsewhere in this repository:

| Mechanism | Source |
|---|---|
| Judge council verdicts | DeepEval, RAGAS |
| Regression detection | Langfuse tracing |
| Adversarial findings | Promptfoo, mapped to OWASP and MITRE ATLAS |
| Human oversight standard | EU AI Act Article 14 |

n8n's role is narrow and deliberate: hold a pause open, guarantee notification, and require a real decision before resuming. It does not compute scores, and it does not decide anything on its own.

## Status

Both workflows are built and reviewed end to end, including the immediate-halt fix and the Continue On Fail notification guarantee. Live production traffic is pending deployment against a real repository.

## Files

- `three-queue-routing.json`
- `kill-switch-regression-alarm.json`
