# Concept: openHAB Claude – AI-Powered Binding Development

## Vision

Building an openHAB binding requires deep knowledge of Java, OSGi, the openHAB API, official coding guidelines, and PR standards. Most developers — even experienced ones — hit friction at each of these layers.

**openHAB Claude** eliminates that friction by turning Claude AI into a complete, opinionated development team. You describe what you want to build. Claude thinks alongside you, enforces the rules automatically, and writes production-ready code.

---

## Problem Statement

| Pain Point | Without openHAB Claude |
|------------|------------------------|
| Guidelines | Developer must remember and apply 44-point PR checklist, coding guidelines, header conventions manually |
| Decisions | Architecture decisions are made informally, often forgotten or inconsistent across PRs |
| Dependencies | New libraries are added without license review or governance |
| Language drift | Comments, logs, and doc strings slip into non-English languages |
| i18n mistakes | Developers manually create `.properties` files that should be generated |
| Context loss | Each AI session starts from zero — rules, structure, and decisions must be re-explained |

---

## Solution

A structured AI context layer consisting of:

1. **Global rules** (`CLAUDE.md`) — loaded automatically, apply to every message
2. **Official guidelines** (`rules/`) — openHAB coding standards and PR checklist, always active
3. **Role system** (`skills/`) — six specialist personas activated on demand via `$Tag`
4. **Decision tracking** (ADRs) — every architectural choice recorded automatically
5. **Governance** — pom.xml and i18n changes are protected by explicit rules

---

## Target Audience

### Primary: openHAB binding developers
- Developers writing new bindings or maintaining existing ones
- Familiar with Java, but not necessarily with all openHAB-specific conventions
- Want faster, more consistent development without reading all the guidelines manually

### Secondary: openHAB community contributors
- Contributors preparing PRs who want to pass review on the first attempt
- Users validating a feature idea before investing development time

---

## Core Principles

**Opinionated over configurable.**
The rules are not options. They are enforced. This ensures consistency across all bindings developed with this setup.

**Context-aware over generic.**
Claude knows openHAB's Thing/Channel model, OSGi patterns, and the PR review checklist. It is not a generic coding assistant — it is specialized for this ecosystem.

**Human in the loop for risky changes.**
pom.xml changes and dependency additions require explicit human approval. The AI proposes; the human decides.

**Language discipline.**
Chat in any language. Everything inside the project stays English. Non-negotiable.

**Documentation as a first-class artifact.**
ADRs are created automatically with every architectural decision. Documentation is not an afterthought.

---

## Non-Goals

- This repository does **not** contain binding code.
- This repository does **not** generate the i18n `.properties` files — those are produced by `mvn i18n:generate-default-translations`.
- This is not a replacement for reading the [openHAB developer documentation](https://www.openhab.org/docs/developer/) — it is a productivity layer on top of it.

---

## Success Criteria

- A developer can start a new binding and reach a PR-ready state without manually consulting the coding guidelines.
- ADRs are created automatically for every non-trivial design decision.
- No i18n files are hand-edited.
- No `pom.xml` change is applied without human approval.
- All generated code passes the 44-point PR checklist on the first `$Review` run.
