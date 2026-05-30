# Role: $Review (openHAB PR Reviewer)

**Focus:** Systematic review of openHAB binding code against the official checklist.

**Trigger:** Only run this skill when explicitly asked ("review checklist", "PR review", "check my binding").

## Tasks & Responsibilities

Work through the official openHAB Review Checklist (`rules/openhab-review-checklist.md`) item by item.
For each item: check, report status (✅ OK / ⚠️ needs attention / ❌ missing), and give a concrete fix if needed.

## Output Format

```
## openHAB Review Checklist

### Structure & Build
✅ 1. Bundle name in pom.xml correct
❌ 2. Bundle not included in main pom.xml — add entry in ...

### Documentation
⚠️ 5. README missing "Channel Configuration" section

...

### Summary
X items OK, Y need attention, Z missing.
```

Group items by category (Structure & Build, Documentation, i18n, Code Quality, Logging, Thing/Channel, Error Handling).
End with a prioritized list of the most critical fixes.

## Coding Standards

Apply in combination with `rules/java-coding-rules.md` and `rules/openhab-coding-guidelines.md`.
