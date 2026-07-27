# Architecture Overview: openHAB Claude – AI-Powered Binding Development

## Purpose

This repository is not a binding itself — it is an **AI development environment** that turns Claude into a structured, opinionated development team for building openHAB bindings. It provides roles, rules, and conventions that Claude loads as context, enabling consistent, guideline-compliant code generation across sessions.

---

## Repository Structure

```text
openhab-claude/
├── CLAUDE.md                     ← Global rules enforced across all roles
├── README.md                     ← Setup guide and role overview
├── docs/
│   ├── ARCHITECTURE.md           ← This file
│   ├── CONCEPT.md                ← Vision, goals, and target audience
│   └── ADR/                      ← Architecture Decision Records
│       └── 000-template.md
├── rules/
│   ├── java-coding-rules.md      ← Project-specific Java rules (extends official guidelines)
│   ├── openhab-coding-guidelines.md  ← Official openHAB coding guidelines
│   └── openhab-review-checklist.md   ← Official PR review checklist (44 items)
└── skills/
    ├── architect/skill.md
    ├── concept/skill.md
    ├── dev/skill.md
    ├── qa/skill.md
    ├── review/skill.md
    └── writer/skill.md
```

---

## Context Loading Strategy

Claude loads context in two tiers:

| Tier | Files | When Loaded |
|------|-------|-------------|
| **Always** | `CLAUDE.md`, `rules/` | Every session, every message |
| **On demand** | `skills/<role>/skill.md` | When user activates a role via `$Tag` |

This two-tier model keeps the base context lean while providing deep role-specific expertise when needed.

---

## Role System

Each role is a separate skill file under `skills/`. A role is activated by prefixing the message with its tag:

| Tag | File | Responsibility |
|-----|------|----------------|
| `$Concept` | `skills/concept/skill.md` | Feature validation, UX, big picture |
| `$Architect` | `skills/architect/skill.md` | Structure, API design, ADRs, pom.xml governance |
| `$Dev` | `skills/dev/skill.md` | Code generation, refactoring, bug fixes |
| `$QA` | `skills/qa/skill.md` | Edge cases, threading, test strategy |
| `$Writer` | `skills/writer/skill.md` | README, JavaDoc, community documentation |
| `$Review` | `skills/review/skill.md` | Full 44-point PR checklist review |

Roles can be combined in a single session. There is no enforced sequencing — the workflow is advisory.

---

## Governance Rules (enforced via CLAUDE.md)

### Language

- Chat language mirrors the user.
- All project artifacts (code, comments, docs, XML, logs) are **English-only**.

### pom.xml Protection

- Only `$Architect` may propose `pom.xml` changes.
- Every dependency change requires explicit human approval before being applied.

### i18n Protection

- Files under `src/main/resources/OH-INF/i18n/` are **never created or edited manually**.
- Translation properties are generated exclusively via `mvn i18n:generate-default-translations`.
- i18n keys are defined in XML source files (`thing-types.xml`, `addon.xml`) only.

### Decision Tracking

- Every architectural or design decision is recorded as an ADR in `docs/ADR/` inside the binding project.
- ADR numbering is sequential. Template: `docs/ADR/000-template.md`.

### Java File Standards

- Every new Java file includes the openHAB license header.
- Every new Java file includes a class-level JavaDoc with `@author`.

---

## Compatibility

| Platform | Notes |
|----------|-------|
| Claude.ai Projects | Primary target. Upload `openhab-claude/` and the binding folder as Project Knowledge. |
| Claude Code (CLI) | Works via `CLAUDE.md` auto-loading. |
| Open WebUI | Upload `rules/` as a Knowledge collection; paste `CLAUDE.md` as system prompt. |

---

## ADR Index

| # | Title | Status |
|---|-------|--------|
| — | _(no ADRs yet — created per binding project, not here)_ | — |
