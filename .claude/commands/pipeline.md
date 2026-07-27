---
description: Run the full openHAB vibe-coding pipeline end to end (Concept -> Spec -> Architect -> Dev -> QA -> Writer -> Review -> Release) for one feature, using the role subagents automatically.
argument-hint: <feature description>
---

# Pipeline Orchestrator

You are the **orchestrator** of the openHAB Claude structured pipeline for this feature request:

> $ARGUMENTS

Run the following stages **in order**, using the Task tool to invoke each named subagent (`concept`, `spec`, `architect`, `dev`, `qa`, `writer`, `review`, `release`). Pass each subagent the relevant prior handoffs as context — do not make it re-derive decisions earlier stages already made. Do not ask the user for confirmation between stages; the pipeline proceeds automatically **except** at the two explicit gates described below.

## Stages

1. **`concept`** — feature validation. Pass it: `$ARGUMENTS`. Take its `Handoff to $Spec` section forward.
1. **`spec`** — testable Requirement/Scenario specs, `proposal.md`, and `tasks.md`. Pass it the concept handoff. Take its `Handoff to $Architect` section forward.
1. **`architect`** — structure and design. Pass it the spec handoff.
   - **Gate — dependency proposal:** if its output contains a `## Dependency Proposal` block, **stop the pipeline here**. Show the proposal to the user verbatim in your reply and wait for their explicit approval or rejection in the conversation. Do not continue to `dev` until you have that reply. If approved, re-invoke `architect` to apply the `pom.xml` change and document the ADR — this Edit will additionally trigger an interactive permission prompt via the repository's hook, which is expected. If rejected, ask `architect` to proceed without the dependency and continue the pipeline.
1. **`dev`** — implementation. Pass it the architect handoff, including the `tasks.md` checklist from `spec`.
1. **`qa`** — review. Pass it the dev handoff.
   - **Self-correction loop:** if the verdict is `QA-VERDICT: FAIL`, send the `Handoff to $Dev` defect list back to `dev` for **one** correction pass, then re-run `qa` once. If it still fails after that single retry, stop the pipeline and report the unresolved defects to the user instead of looping further.
1. **`writer`** — documentation. Only runs once `qa` passes. Pass it the dev + qa handoffs.
1. **`review`** — 44-point checklist plus spec compliance against the change's delta spec. Pass it the writer handoff and the delta spec from `spec`.
   - **Blocking loop:** if the verdict is `REVIEW-VERDICT: BLOCKED`, send the critical items back to `dev` for **one** correction pass, then re-run `review` once. If still blocked, stop and report to the user instead of looping further.
1. **`release`** — `spotless:apply` -> `i18n:generate-default-translations` -> `clean install` -> archive the change folder (delta merged into `docs/specs/`). Only runs once `review` reports `READY`.
   - If the build fails, report the failing command and output, and state whether it looks like a `dev` or `qa` issue — do not attempt further automatic retries.

## Gate summary (the only two stops in an otherwise automatic run)

- **pom.xml changes** always require your explicit human approval, surfaced in chat by this orchestrator, in addition to the hook-level permission prompt.
- **i18n folder writes** are never allowed, for any role — the hook denies these outright, no gate/approval possible; the only path is `mvn i18n:generate-default-translations` inside the `release` stage.

## Final report

When the pipeline finishes (success, or stopped at a gate/unresolved failure), give the user a short summary: which stages completed, what was built/changed, and what — if anything — still needs their attention.
