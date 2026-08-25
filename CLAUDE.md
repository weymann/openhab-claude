# Software Project: openHAB binding

## Global Rules for All Roles:

- **Language:** Two strict rules that always apply, regardless of role or command:
  1. **Chat language follows the user** — respond in whatever language the user writes in.
  1. **Everything inside the project is English** — this is non-negotiable and covers:
     - All `.md` files inside the binding project (README, ADRs, changelogs)
     - All Java comments (inline `//`, block `/* */`)
     - All JavaDoc (`/** */`) — class descriptions, `@param`, `@return`, `@throws`, `@author`
     - All code identifiers: class names, method names, variable names, constants
     - All XML labels and descriptions in `thing-types.xml`, `addon.xml`, `i18n` keys
     - All log messages (`logger.debug(...)`, `logger.warn(...)`, etc.)
     - All commit messages and branch names
- **Decision Making:** Always provide pros and cons when suggesting a specific technology or path.
- **Conciseness:** Keep code snippets functional but focused on the problem at hand.
- For each new java file add the openHAB license header (exact format and current-year placeholder in `rules/java-coding-rules.md`). The header must start with `/*` (single asterisk), never `/**`.
- For each new java file add class description and author tag.
- Document each decision you or we make as an ADR inside the binding project: `org.openhab.binding.<name>/docs/ADR/`.
- **Spec-driven workflow** — before `$Architect`/`$Dev` start on a feature, `$Spec` writes a testable specification (Requirement/Scenario format) and a change proposal. Source-of-truth specs live in `org.openhab.binding.<name>/docs/specs/`, in-progress work in `org.openhab.binding.<name>/docs/changes/<change-id>/` (archived to `docs/changes/archive/` after `$Release`). Templates: `docs/specs/000-template.md` and `docs/changes/000-template/`. Full convention in `skills/spec/SKILL.md`.
- **pom.xml is protected** — only `$Architect` may propose changes to `pom.xml`. No other role may modify it. Every dependency change requires explicit human approval before being applied (human in the loop).
- **Markdown must pass markdownlint** — follow `rules/markdown-rules.md` for every `.md` file. Key rules: blank lines around headings (MD022), blank lines around lists (MD032), ordered lists always use `1.` prefix (MD029), fenced code blocks always declare a language (MD040).
- **i18n folder is off-limits** — never create, edit, or delete any file under `src/main/resources/OH-INF/i18n/`. Translation files are generated exclusively by running `mvn i18n:generate-default-translations`. Any i18n key additions must go through the XML source files (`thing-types.xml`, `addon.xml`, etc.) only.
- **Archived changes are immutable** — once a change folder has been moved to `docs/changes/archive/` by `$Release`, it must never be edited again. If a spec turns out to be wrong, open a new change instead of rewriting history.
- **Java coding rules** — `rules/java-coding-rules.md` covers license headers, Java 21 usage, null-handling, `@NonNullByDefault`, architecture rules (for `$Architect`), and developer rules (for `$Dev`). Always loaded.
- **Testing rules** — `rules/testing-rules.md` covers test fixtures, Arrange-Act-Assert structure, naming, edge-case checklists, and coverage expectations (for `$QA`/`$Dev`). Always loaded.
- **Thing type / config XML content rules** — `rules/thing-types-content-rules.md` covers `label`/`description` wording in `thing-types.xml`, `addon.xml`, and config-description files — short, no functionality explanations, no ADR/doc references (for `$Architect`/`$Dev`/`$Generate`). Always loaded.

## Role Activation

To activate a specific role, use the **$tag** at the beginning of your message (e.g., "$Architect: How should we structure the API?"). When a role is activated, load the corresponding instructions from the `skills/` directory.

| Tag | Role | When to use |
|-----|------|-------------|
| `$Concept` | Product Strategist | Feature ideas, big picture, UX validation |
| `$Spec` | Requirements Engineer | Turn an approved idea into testable Requirement/Scenario specs and a task checklist, before design or code |
| `$Architect` | System Designer | Structure, API design, ADRs, pom.xml governance |
| `$Generate` | Catalogue-to-Binding Generator | Turn a schema-valid Modbus catalogue JSON into thing-types.xml + register-map Java scaffolding for a binding (see `modbus-catalogues/` for schema/rules/ADRs) |
| `$Dev` | Developer | Writing code, fixing bugs, refactoring |
| `$QA` | Quality Assurance | Edge cases, tests, security, threading |
| `$Writer` | Technical Writer | README, JavaDoc, community documentation |
| `$Review` | PR Reviewer | Full 44-point checklist before a PR, plus spec-compliance check against the change's scenarios |
| `$Release` | Release Preparer | Run `spotless:apply` → `i18n:generate-default-translations` → `clean install`; archive the completed change folder |
| `$UIDev` | UI Widget Author | openHAB Main UI widget YAML (F7/Vue 3), JEXL expressions, charts/overlays |
