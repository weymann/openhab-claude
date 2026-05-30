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
- For each new java file add the openHAB header.
- For each new java file add class description and author tag.
- Document each decision you or we make as an ADR inside the binding project: `org.openhab.binding.<name>/docs/ADR/`.
- **pom.xml is protected** — only `$Architect` may propose changes to `pom.xml`. No other role may modify it. Every dependency change requires explicit human approval before being applied (human in the loop).

## Role Activation
To activate a specific role, use the **$tag** at the beginning of your message (e.g., "$Architect: How should we structure the API?"). When a role is activated, load the corresponding instructions from the `skills/` directory.