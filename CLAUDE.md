# CLAUDE.md

This file is read automatically at the start of every Claude Code session in this repository. It exists so context does not have to be re-explained each time. Read this in full before making any changes.

## What This Repository Is

`python-ai-governance` is Steve Onyeke's AI governance portfolio, the technical foundation of Afrispan Data Labs, an AI deployment assurance practice for SMEs, built first for Ghana and West Africa. It spans three connected projects:

- **Project 1**: nine phases proving core governance principles, executed against real Gemini API calls. Complete.
- **Project 2**: a thirteen-notebook production evaluation suite plus a live CI/CD layer. Architecture complete and pytest-verified; most notebooks run in simulated mode pending funded API billing.
- **Project 3**: the evaluation logic from Project 2 wired into live orchestration infrastructure that actually acts on what it finds, not just scores it. Phases 1 and 2 built and reviewed end to end. **This is the active work.**

Full narrative detail for Projects 1 and 2 lives in `docs/PROJECT_HISTORY.md`. Read it before touching anything in `phase1-foundations/` through `phase9-portfolio-launch/` or `project-2-llm-evaluation-suite/`. The actionable spec for the current work, Project 3 Phases 3 and 4, lives in `project-3-governance-runtime/PHASE_3_4_SPEC.md`. Read that before writing any new code.

## Repository Structure

```
phase1-foundations/            Project 1, Phase 1
phase2-data-handling/          Project 1, Phase 2
phase3-llm-evaluation/         Project 1, Phase 3
phase4-red-teaming/            Project 1, Phase 4
phase5-bias-auditing/          Project 1, Phase 5
phase6-function-calling/       Project 1, Phase 6
phase7-rag-observer-agent/     Project 1, Phase 7
phase8-multi-agent-governance/ Project 1, Phase 8 (the real kill-switch)
phase9-portfolio-launch/       Project 1, Phase 9 (FRIA, Conformity Report, Cross-Border Framework)
project-2-llm-evaluation-suite/ Project 2, all 13 notebooks plus CI/CD (Dockerfile, GitHub Actions, pytest)
project-3-governance-runtime/n8n-workflows/  Project 3, current work
.github/workflows/             deepeval-regression.yml, the real, verified CI pipeline
docs/PROJECT_HISTORY.md        Full Project 1 and 2 detail, read on demand
README.md                      Public-facing summary, keep in sync with actual repo state
```

## Non-Negotiable Rules

**No em dashes, anywhere.** In code comments, in documentation, in commit messages, in anything generated for this repo. Use commas, colons, or restructured sentences instead. This has been enforced consistently across every artifact in this project and any new file must match.

**Status tagging is honest, always, no exceptions.** Every deliverable in this repo uses one of these conventions and any new work must too:
- `PROVEN` / `BUILDING` / `PLANNED` for Afrispan-facing claims, never blurred.
- `SIMULATED_OUTPUT = True/False` as an explicit flag in every Project 2 notebook, real execution never silently implied.
- `NOT_ASSESSED` for an untested obligation in the Conformity Report, never silently omitted.
- A missing field is tagged `MISSING`, never filled with a plausible-sounding guess.

If a new Project 3 phase has a real gap, name it directly in code comments and in any generated documentation. Do not imply something works before it has been verified to work.

**Verify before asserting.** This portfolio's credibility comes from catching its own mistakes in the open. Real examples already in this repo's history: a RAGAS 0.4.x import bug traced to a specific upstream issue, a crescendo red-team substring bug that flagged a correct figure as compromised, a GitHub Actions 403 Forbidden error diagnosed to a specific permissions default. When building Phase 3 or Phase 4, run the code and check the actual output before describing it as working. Do not describe a function as tested if it has not been run.

**Never fabricate a metric, a citation, or a design credit.** Federico Blanco Sanchez-Llanos, Enforcement Infrastructure Capital and Compute, is credited by name for three real, specific design contributions already in this repo: three-queue routing, the signed-artifact mechanism, and the integrity-of-record versus fidelity-of-judgment distinction. A fourth, pre-committed verdicts, is the subject of Phase 3's build. Do not invent additional attributions.

## The Five Governance Principles This Repo Exists to Prove

1. **An AI system cannot audit itself.** Structural fix: a different model family must judge, decided architecturally, not by prompt.
2. **Surface pattern-matching fails at the edges, in every form it takes.** Every fix that closes one failure mode has introduced a new, more subtle one. Expect this pattern to hold in Phase 3 and 4 work too, do not assume a fix is complete without checking for what it might have broken.
3. **Monitoring is not governing.** Detection without a mechanism to act on it is a dashboard. This is the exact principle Project 3 exists to close.
4. **Authority is not judgment.** A human override requires a documented, substantive position, not a reflexive click. The real benchmark is Phase 8's kill-switch demonstration: 4 minutes 33 seconds between breach detection and a recorded abort decision.
5. **Disagreement between a judge and a human is diagnostic, not noise.** A rubric gap, not a judge failure, is usually the real cause. Do not tune a threshold to make a disagreement go quiet.

## Scope Boundary, Read This Before Assuming Anything

This repository and everything in it is **portfolio continuation work**. It is explicitly meant to build on Project 1 and Project 2's real codebase, extending the same repo, the same story, the same GitHub profile.

This is a **different task** from a hypothetical future request to build a real, production AI governance system for an actual employer (for example, if Steve is later asked to design a Claude Code instruction set for a real company's production environment). That future task, if it ever comes up, would need to be a clean-start, ground-up build against that company's real systems, not a continuation of this repo, and would be scoped in an entirely separate conversation with entirely separate instructions. Do not conflate the two. Nothing in this repository should be treated as, or repackaged into, a client deliverable without being told explicitly that is the task.

## Working Style

- State assumptions explicitly rather than silently picking one when a requirement is ambiguous, then proceed.
- When something is genuinely uncertain (an exact API contract, a specific number not yet verified), say so directly rather than filling the gap with a plausible-sounding guess.
- Prefer real, working, tested increments over large speculative builds. Every phase in this repo's history was built and verified in small, checkable steps, not written wholesale and assumed correct.
- Match the existing code style in whatever phase or notebook is being extended rather than imposing a new convention.
