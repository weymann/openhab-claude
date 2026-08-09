# openHAB Claude – AI-Powered Binding Development

> Spec-Driven Development for openHAB — build production-ready bindings faster with a structured AI development team at your side.

Developing an openHAB binding requires deep knowledge of Java, OSGi, openHAB APIs, coding guidelines, and PR standards.
This repository turns Claude AI into a **complete, opinionated development team** — ready to use, zero configuration.

- ✅ **Provides a complete AI development team** — Requirements Engineer, Architect, Developer, QA, Writer, and PR Reviewer roles, each with a distinct focus and expertise
- ✅ **Spec-driven** — every feature gets a testable Requirement/Scenario spec and change proposal before design or code, checked again by `$Review` before release
- ✅ **Enforces official openHAB coding guidelines** — automatically, on every response
- ✅ **Enforces the official PR review checklist** — 44-point review before every pull request
- ✅ **Language-aware** — chat in any language, all project files stay in English
- ✅ **Decision tracking built-in** — every architectural decision recorded as an ADR with optional Mermaid diagrams
- ✅ **Dependency governance** — new libraries require `$Architect` approval, automatic license analysis via Maven, human-in-the-loop confirmation before any `pom.xml` change
- ✅ **Extensible by design** — add your own coding rules alongside the official guidelines
- ✅ **Optional automated pipeline** — `/pipeline` (Claude Code only) runs Concept → Spec → Architect → Dev → QA → Writer → Review → Release end to end, with the same governance gates enforced by hooks
- ✅ **Works with Claude.ai Projects, Claude Code, and Open WebUI**

---

## Step 1: Set Up the Development Environment

→ <https://www.openhab.org/docs/developer/>

---

## Step 2: Create a New Binding

→ <https://www.openhab.org/docs/developer/#develop-a-new-binding>

---

## Step 3: Set Up a Claude Project

A Claude Project is a persistent workspace in Claude.ai.
Claude remembers the context — you don't have to re-explain rules and background with every message.

### 3.1 Create a Project

1. Go to <https://claude.ai>
1. Click **Projects** → **New Project** on the left
1. Give it a name, e.g. `openHAB MyNewBinding`

### 3.2 Add Two Folders as Context

Under **Project Knowledge**, add both folders:

**Folder 1: `openhab-claude`** (this repository)
→ contains all roles, rules, and checklists
→ Claude knows the ground rules

**Folder 2: your binding folder**, e.g.:
`openhab-addons/bundles/org.openhab.binding.mynewbinding`
→ Claude knows your current code

> **Tip:** Re-upload the binding folder after larger changes so Claude works with the latest state.

### 3.3 What Claude Now Knows

- Global rules from `CLAUDE.md`
- Coding standards from `rules/`
- Roles from `skills/`
- Your current binding code

---

## Step 4: Start Spec-Driven Development

**Spec-Driven Development** means: you describe what you want, `$Spec` turns it into a testable Requirement/Scenario specification, and only then does `$Architect`/`$Dev` design and write the code.
To keep things structured, activate a **role** by adding a `$Tag` at the start of your message.

```text
$Dev: Write a method that sets the Thing status to ONLINE.
$Architect: How should we structure the configuration parameters?
$QA: What can go wrong with the HTTP connection?
```

Claude then acts as a specialist in that role — with the matching focus and tone.

---

## The Roles

| Tag | Role | When to use |
|---|---|---|
| `$Concept` | Product Strategist | Feature ideas, "Does this make sense?", big picture |
| `$Spec` | Requirements Engineer | Turn an approved idea into a testable Requirement/Scenario spec and task checklist, before design or code |
| `$Architect` | System Designer | Structure, API design, class diagrams, dependencies |
| `$Generate` | Catalogue-to-Binding Generator | Turn a schema-valid Modbus catalogue JSON into thing-types.xml + register-map Java scaffolding |
| `$Dev` | Developer | Writing code, fixing bugs, refactoring |
| `$QA` | Quality Assurance | Edge cases, tests, security, threading |
| `$Writer` | Technical Writer | README, JavaDoc, explanations for the community |
| `$Review` | PR Reviewer | Full checklist review, plus a spec-compliance check against the change's scenarios |
| `$Release` | Release Preparer | `spotless:apply` → `i18n:generate-default-translations` → `clean install`, then archive the completed change |
| `$UIDev` | UI Widget Author | openHAB Main UI widget YAML (F7/Vue 3), JEXL expressions, charts/overlays |

> `$Review` only on explicit request — it runs through the complete 44-item checklist. `$UIDev` and `$Generate` are used standalone, on demand — neither is part of the `/pipeline` sequence below.

---

## Repository Structure

```text
openhab-claude/
├── README.md                ← This file
├── CLAUDE.md                ← Global rules for all roles (language, decisions, headers)
├── docs/
│   ├── ARCHITECTURE.md                 ← Repository architecture overview
│   ├── CONCEPT.md                      ← Vision, goals, target audience
│   ├── ADR/                            ← Architecture Decision Records (template)
│   ├── specs/000-template.md           ← Requirement/Scenario spec template
│   └── changes/000-template/           ← proposal.md, tasks.md, specs/ delta template
├── rules/
│   ├── java-coding-rules.md            ← Java rules: headers, Java 21, architecture, dev rules
│   ├── testing-rules.md                ← Testing conventions and reusable test fixtures
│   ├── markdown-rules.md               ← markdownlint-compliant Markdown rules
│   ├── thing-types-content-rules.md    ← label/description wording for thing-types.xml, addon.xml
│   ├── test-fixtures/                  ← Reusable mock/helper classes for unit tests
│   ├── openhab-coding-guidelines.md    ← Official openHAB guidelines
│   └── openhab-review-checklist.md     ← Official PR checklist (44 items)
└── skills/
    ├── concept/skill.md
    ├── spec/SKILL.md
    ├── architect/SKILL.md
    ├── generate/skill.md
    ├── dev/skill.md
    ├── qa/SKILL.md
    ├── writer/skill.md
    ├── review/skill.md
    ├── release/skill.md
    └── uidev/SKILL.md
```

**Important:**

- `rules/` — loaded with every session. These are the rules that **always** apply.
- `skills/` — only loaded when you activate a role with a `$Tag`.

---

## Documenting Decisions

Every architecture or design decision is recorded as an ADR (Architecture Decision Record).
ADRs live inside the binding folder, not here:

```text
org.openhab.binding.mynewbinding/
└── docs/ADR/
    ├── 001-thing-handler-structure.md
    ├── 002-http-client-choice.md
    └── ...
```

You don't need to trigger this manually — Claude creates the ADR as soon as a decision is made.

---

## Spec-Driven Workflow

Before `$Architect`/`$Dev` start on a feature, `$Spec` turns the approved `$Concept` idea into a testable specification — inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec), reduced to the parts that don't duplicate what already exists here (no separate `design.md` — technical rationale stays in the ADR).

```text
org.openhab.binding.mynewbinding/docs/
├── specs/                        ← source of truth: how the binding currently behaves
│   └── <domain>/spec.md          ← Requirement / Scenario (Given/When/Then), RFC 2119 keywords
├── changes/<change-id>/          ← work in progress, one folder per feature
│   ├── proposal.md               ← why + scope (in/out)
│   ├── tasks.md                  ← implementation checklist for $Dev
│   └── specs/<domain>/spec.md    ← delta: ADDED / MODIFIED / REMOVED Requirements
└── changes/archive/              ← moved here by $Release, deltas merged into specs/
```

`$QA` maps test cases to scenarios, and `$Review` checks spec compliance in addition to the 44-point checklist. Templates: `docs/specs/000-template.md` and `docs/changes/000-template/`. Full convention in `skills/spec/SKILL.md`.

---

## Typical Workflow

```text
1. $Concept   → Clarify and validate the feature
2. $Spec      → Write the Requirement/Scenario spec, proposal, and task checklist
3. $Architect → Decide on structure and design (→ ADR)
4. $Dev       → Write code following rules/ and the tasks.md checklist
5. $QA        → Review code, define test cases mapped to scenarios
6. $Writer    → Documentation and README
7. $Review    → Before the PR: run the full checklist plus spec compliance
```

You can switch or combine roles at any time. No rigid process — just a clear orientation.

---

## Automated Pipeline (Claude Code Only)

Beyond manually tagging roles, this repository also ships a Claude Code subagent pipeline that runs the full workflow above automatically. Hooks keep the `pom.xml` and i18n protections in place no matter which role is acting, so automation does not bypass the governance rules in `CLAUDE.md`.

### Setup

Claude Code loads `.claude/agents`, `.claude/commands`, and `.claude/settings.json` relative to the project root it is started in. Since this repository is the rules framework and not a binding project itself, copy or symlink its `.claude/` folder into your actual binding project root before using it:

```bash
cp -r openhab-claude/.claude your-binding-project/.claude
```

Or, to keep it in sync with future updates to this repository:

```bash
ln -s ../openhab-claude/.claude your-binding-project/.claude
```

### Usage

Run the full pipeline for one feature from Claude Code:

```text
/pipeline Add support for polling battery level every 5 minutes
```

Claude Code invokes, in order: `concept`, `spec`, `architect`, `dev`, `qa`, `writer`, `review`, `release`. Each subagent hands its output to the next one, so you don't need to copy context between stages yourself.

### Automatic safeguards

- QA failures trigger one automatic correction pass back to `dev`, then a re-test. Two consecutive failures stop the pipeline and report to you instead of looping.
- Review-checklist blockers (including unsatisfied spec scenarios) follow the same one-retry pattern before stopping.
- Any `pom.xml` change pauses the pipeline and shows you the dependency proposal for approval, mirroring the manual `$Architect` process. A hook additionally enforces this at the tool level, regardless of which stage triggers the edit.
- Any write under `src/main/resources/OH-INF/i18n/` is blocked outright by the same hook. Only `mvn i18n:generate-default-translations`, run automatically during the `release` stage, may touch that folder.
- Once `clean install` succeeds, `release` archives the change folder and merges its delta spec into `docs/specs/` — see [Spec-Driven Workflow](#spec-driven-workflow). Once archived, the same hook blocks any further Edit/Write under `docs/changes/archive/` — archived changes are immutable history.

### Manual roles still work

`/pipeline` is additive, not a replacement. You can still tag individual roles (`$Dev: ...`, `$QA: ...`) for one-off work without running the whole pipeline — see [The Roles](#the-roles) above.

---

## Compatibility

Works with **Claude.ai Projects**, **Claude Code**, and **Open WebUI**.
For Open WebUI: upload the `rules/` files as a Knowledge collection and paste the contents of `CLAUDE.md` as the system prompt.

---

## Further Reading

- [openHAB Developer Guide](https://www.openhab.org/docs/developer/)
- [Bindings Developer Guide](https://www.openhab.org/docs/developer/bindings/)
- [Coding Guidelines](https://www.openhab.org/docs/developer/guidelines)
- [PR Review Checklist](https://github.com/openhab/openhab-addons/wiki/Review-Checklist)
- [Eclipse IDE Setup](https://www.openhab.org/docs/developer/ide/eclipse)
- [openHAB Community Forum](https://community.openhab.org)
