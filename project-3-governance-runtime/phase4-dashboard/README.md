# Phase 4: Bird's-Eye-View Dashboard

Status: PROVEN. Verified 2026-08-27: `pytest tests/` passed 5/5, `python data_store.py` produced real output (routing rates PASS 2/BORDERLINE 1/FAIL 2, regression counts OK 1/WARNING 1/ALARM 5, 6 hash-verified verdicts), and `streamlit run app.py` was exercised in a live browser check, all four panels, both in-app honesty badges, and the drill-down selector confirmed working against the real store.

## What this closes

A real, honestly-named gap from the Talabat interview preparation work: no single view exists across the systems this evaluation architecture governs. Per-system tracing exists, but nothing aggregates across systems into one place a non-technical reader could scan. Full spec: [`../PHASE_3_4_SPEC.md`](../PHASE_3_4_SPEC.md).

## Tech choice: Streamlit, not React

Streamlit is the lower-effort option, and there is no existing frontend or JS tooling anywhere in this portfolio to build on, every other piece of this repo is Python. None of the four required panels (bar chart, two metrics, a table, a selectbox-driven drill-down) need more interactivity than Streamlit provides natively. A React app would mean introducing an entirely new toolchain (npm, a build step, component structure) for capability this dashboard does not actually require.

## Data source: local store, not live Langfuse

Before starting, two things were checked and found not to hold:
1. No Langfuse credentials exist in this environment (no `.env`, no `LANGFUSE_*` env vars).
2. Even with credentials, Project 2's Phase 06a already found 0/9 upstream sources ever pushed genuinely live to Langfuse, everything ran `SIMULATED_OUTPUT = True` in Colab.

`data_store.py` builds a local JSON store instead, fed by four real sources, using the spec's own allowance for "a store fed by" Langfuse rather than a live API pull:

| Panel | Real source |
|---|---|
| Pass/borderline/fail rates | Phase 3a's 5 real test-case outcomes, same source Phase 3's `demo.py` uses |
| Judge alignment trend | Phase 4a/4b's two real numbers: pre-calibration 83.3% (5/6), post-calibration 100% (6/6) |
| Regression alarm status | 06b's real saved notebook output: 5 real ALARM cases, 1 real OK case, 1 synthetic WARNING case, same real/synthetic split 06b itself documented |
| Verdict drill-down | Phase 3's own real `commitments.jsonl`, each entry independently hash-verifiable |

`data_store.py` stands in for what would eventually be an n8n scheduled poller once a live source (real Langfuse traces) exists. Building that n8n workflow now would have nothing real to poll, so it stays deferred, same call made in Phase 3. No visualization logic lives in n8n, per the spec's explicit constraint.

## Honest limitations, visible in the dashboard itself, not only here

Two of the panels above carry a real caveat serious enough that it is not enough to state once in this README. Each renders as a visible `st.info` badge directly on its panel in `app.py`, the same principle as this repo's `SIMULATED_OUTPUT` tags:

- **Regression Alarm Status** panel: "Sourced from 06b's saved notebook output, not a live recomputation. That notebook ran in Colab and is not reproducible in this local environment without Drive access."
- **Judge Alignment Trend** panel: "Only two real calibration points exist in this project's history, pre-calibration and post-calibration. This is not a continuous time series. There has only ever been one calibration event."

Additional limitations:
- No auth or access control, per the spec's own stated open question. Acceptable for a personal portfolio demo, not for anything shown more widely. Stated here and as a caption in the app itself.
- The **Verdict Drill-Down** panel depends on Phase 3's `demo.py` having been run at least once locally, since `data/commitments.jsonl` is not committed to git (same convention as Phase 3's own generated output). If it is missing, the panel says so explicitly rather than showing nothing unexplained.

## Files

- `data_store.py`: aggregates the four real sources into `data/dashboard_store.json`.
- `app.py`: Streamlit app, read-only, renders the store, computes nothing.
- `tests/test_data_store.py`: pure-logic tests on the aggregation, no Streamlit/UI testing, no API keys required.

## Running it

```
python data_store.py
streamlit run app.py
```
