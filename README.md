# openHAB Claude – AI-Powered Binding Development

> Vibe Coding for openHAB — build production-ready bindings faster with a structured AI development team at your side.

Developing an openHAB binding requires deep knowledge of Java, OSGi, openHAB APIs, coding guidelines, and PR standards.
This repository turns Claude AI into a **complete, opinionated development team** — ready to use, zero configuration.

- ✅ **Provides a complete AI development team** — Architect, Developer, QA, Writer, and PR Reviewer roles, each with a distinct focus and expertise
- ✅ **Enforces official openHAB coding guidelines** — automatically, on every response
- ✅ **Enforces the official PR review checklist** — 44-point review before every pull request
- ✅ **Language-aware** — chat in any language, all project files stay in English
- ✅ **Decision tracking built-in** — every architectural decision recorded as an ADR with optional Mermaid diagrams
- ✅ **Dependency governance** — new libraries require `$Architect` approval, automatic license analysis via Maven, human-in-the-loop confirmation before any `pom.xml` change
- ✅ **Extensible by design** — add your own coding rules alongside the official guidelines
- ✅ **Optional automated pipeline** — `/pipeline` (Claude Code only) runs Concept → Architect → Dev → QA → Writer → Review → Release end to end, with the same governance gates enforced by hooks
- ✅ **Works with Claude.ai Projects, Claude Code, and Open WebUI**

---

## Step 1: Set Up the Development Environment

→ https://www.openhab.org/docs/developer/

---

## Step 2: Create a New Binding

→ https://www.openhab.org/docs/developer/#develop-a-new-binding

---

## Step 3: Set Up a Claude Project

A Claude Project is a persistent workspace in Claude.ai.
Claude remembers the context — you don't have to re-explain rules and background with every message.

### 3.1 Create a Project

1. Go to https://claude.ai
2. Click **Projects** → **New Project** on the left
3. Give it a name, e.g. `openHAB MyNewBinding`

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

## Step 4: Start Vibe Coding

**Vibe Coding** means: you describe what you want — Claude thinks along, suggests, and writes code.
To keep things structured, activate a **role** by adding a `$Tag` at the start of your message.

```
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
| `$Architect` | System Designer | Structure, API design, class diagrams, dependencies |
| `$Dev` | Developer | Writing code, fixing bugs, refactoring |
| `$QA` | Quality Assurance | Edge cases, tests, security, threading |
| `$Writer` | Technical Writer | README, JavaDoc, explanations for the community |
| `$Review` | PR Reviewer | Full review against the official openHAB checklist |
| `$Release` | Release Preparer | `spotless:apply` → `i18n:generate-default-translations` → `clean install` |

> `$Review` only on explicit request — it runs through the complete 44-item checklist.

---

## Repository Structure

```text
openhab-claude/
├── README.md                ← This file
├── CLAUDE.md                ← Global rules for all roles (language, decisions, headers)
├── docs/
│   ├── ARCHITECTURE.md                 ← Repository architecture overview
│   ├── CONCEPT.md                      ← Vision, goals, target audience
│   └── ADR/                            ← Architecture Decision Records
├── rules/
│   ├── java-coding-rules.md            ← Java rules: headers, Java 21, architecture, dev rules
│   ├── testing-rules.md                ← Testing conventions and reusable test fixtures
│   ├── markdown-rules.md               ← markdownlint-compliant Markdown rules
│   ├── test-fixtures/                  ← Reusable mock/helper classes for unit tests
│   ├── openhab-coding-guidelines.md    ← Official openHAB guidelines
│   └── openhab-review-checklist.md     ← Official PR checklist (44 items)
└── skills/
    ├── architect/skill.md
    ├── concept/skill.md
    ├── dev/skill.md
    ├── qa/skill.md
    ├── release/skill.md
    ├── review/skill.md
    └── writer/skill.md
```

**Important:**
- `rules/` — loaded with every session. These are the rules that **always** apply.
- `skills/` — only loaded when you activate a role with a `$Tag`.

---

## Documenting Decisions

Every architecture or design decision is recorded as an ADR (Architecture Decision Record).
ADRs live inside the binding folder, not here:

```
org.openhab.binding.mynewbinding/
└── docs/ADR/
    ├── 001-thing-handler-structure.md
    ├── 002-http-client-choice.md
    └── ...
```

You don't need to trigger this manually — Claude creates the ADR as soon as a decision is made.

---

## Typical Workflow

```
1. $Concept   → Clarify and validate the feature
2. $Architect → Decide on structure and design (→ ADR)
3. $Dev       → Write code following rules/
4. $QA        → Review code, define test cases
5. $Writer    → Documentation and README
6. $Review    → Before the PR: run the full checklist
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

Claude Code invokes, in order: `concept`, `architect`, `dev`, `qa`, `writer`, `review`, `release`. Each subagent hands its output to the next one, so you don't need to copy context between stages yourself.

### Automatic safeguards

- QA failures trigger one automatic correction pass back to `dev`, then a re-test. Two consecutive failures stop the pipeline and report to you instead of looping.
- Review-checklist blockers follow the same one-retry pattern before stopping.
- Any `pom.xml` change pauses the pipeline and shows you the dependency proposal for approval, mirroring the manual `$Architect` process. A hook additionally enforces this at the tool level, regardless of which stage triggers the edit.
- Any write under `src/main/resources/OH-INF/i18n/` is blocked outright by the same hook. Only `mvn i18n:generate-default-translations`, run automatically during the `release` stage, may touch that folder.

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
