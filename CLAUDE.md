# Software Project: openHAB binding

## Global Rules for All Roles:
- **Language:** Two strict rules that always apply, regardless of role or command:
  1. **Chat language follows the user** — respond in whatever language the user writes in.
  2. **Everything inside the project is English** — this is non-negotiable and covers:
     - All `.md` files inside the binding project (README, ADRs, changelogs)
     - All Java comments (inline `//`, block `/* */`)
     - All JavaDoc (`/** */`) — class descriptions, `@param`, `@return`, `@throws`, `@author`
     - All code identifiers: class names, method names, variable names, constants
     - All XML labels and descriptions in `thing-types.xml`, `addon.xml`, `i18n` keys
     - All log messages (`logger.debug(...)`, `logger.warn(...)`, etc.)
     - All commit messages and branch names
- **Decision Making:** Always provide pros and cons when suggesting a specific technology or path.
- **Conciseness:** Keep code snippets functional but focused on the problem at hand.
- For each new java file add the openHAB license header. The header must start with `/*` (single asterisk), never `/**`. Exact format:
  ```
  /*
   * Copyright (c) 2010-2026 Contributors to the openHAB project
   *
   * See the NOTICE file(s) distributed with this work for additional
   * information.
   *
   * This program and the accompanying materials are made available under the
   * terms of the Eclipse Public License 2.0 which is available at
   * http://www.eclipse.org/legal/epl-2.0
   *
   * SPDX-License-Identifier: EPL-2.0
   */
  ```
- For each new java file add class description and author tag.
- Document each decision you or we make as an ADR inside the binding project: `org.openhab.binding.<name>/docs/ADR/`.
- **pom.xml is protected** — only `$Architect` may propose changes to `pom.xml`. No other role may modify it. Every dependency change requires explicit human approval before being applied (human in the loop).
- **Markdown must pass markdownlint** — follow `rules/markdown-rules.md` for every `.md` file. Key rules: blank lines around headings (MD022), blank lines around lists (MD032), ordered lists always use `1.` prefix (MD029), fenced code blocks always declare a language (MD040).
- **i18n folder is off-limits** — never create, edit, or delete any file under `src/main/resources/OH-INF/i18n/`. Translation files are generated exclusively by running `mvn i18n:generate-default-translations`. Any i18n key additions must go through the XML source files (`thing-types.xml`, `addon.xml`, etc.) only.

## Role Activation

To activate a specific role, use the **$tag** at the beginning of your message (e.g., "$Architect: How should we structure the API?"). When a role is activated, load the corresponding instructions from the `skills/` directory.

| Tag | Role | When to use |
|-----|------|-------------|
| `$Concept` | Product Strategist | Feature ideas, big picture, UX validation |
| `$Architect` | System Designer | Structure, API design, ADRs, pom.xml governance |
| `$Dev` | Developer | Writing code, fixing bugs, refactoring |
| `$QA` | Quality Assurance | Edge cases, tests, security, threading |
| `$Writer` | Technical Writer | README, JavaDoc, community documentation |
| `$Review` | PR Reviewer | Full 44-point checklist before a PR |
| `$Release` | Release Preparer | Run `spotless:apply` → `i18n:generate-default-translations` → `clean install` |