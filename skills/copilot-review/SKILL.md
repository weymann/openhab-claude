# Role: $CopilotReview (openHAB GitHub/Copilot Review)

**Focus:** Establish which criteria a GitHub review of an openHAB pull request really applies — the GitHub Copilot code review bot or an AI-assisted maintainer review — and reproduce those criteria in the current session.

**Trigger:** Only run this skill when explicitly asked ("by which criteria does Copilot review", "which rules apply to my PR", "review the PR the way GitHub Copilot does").

## Tasks & Responsibilities

1. Identify which review track produced the feedback in the pull request.
1. Resolve every instruction source that track consumes — live, not from memory.
1. Report the criteria together with the file, setting, or endpoint that proves them.
1. On request, run the review against exactly that policy (Recipe B) and report the findings.

## Two Review Tracks

| Track | Recognition in the pull request | Source of criteria |
| --- | --- | --- |
| GitHub Copilot code review (bot) | Review or inline comment by `Copilot` / `copilot-pull-request-reviewer[bot]`; the review body starts with `## Pull request overview` | Custom instructions of the repository, read from the **head branch** of the PR |
| AI-assisted maintainer review | Review text contains one of the mandatory notices `_This is an initial AI-assisted review._`, `_This is an additional AI-assisted review._`, or `_This review was AI-assisted._` | `wborn/github-review-policy` (generic policy plus openHAB extension) |

Both tracks additionally consult the repository `AGENTS.md`.
Known openHAB maintainers using this workflow: `wborn`, `lsiepel`, `florian-h05`.

## What Copilot Reads

GitHub Copilot code review resolves its instructions from these sources:

1. Repository-wide: `.github/copilot-instructions.md`.
1. Path-specific: `.github/instructions/**/NAME.instructions.md`.
1. Agent instructions, also for code review: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `REVIEW.md` — the nearest `AGENTS.md` in the directory tree wins.
1. Agent skills (`.github/skills/<name>/SKILL.md`) and MCP servers.
1. Organization custom instructions, visible to organization owners only.

Practical consequences:

- Instructions are read from the **head branch of the PR**, not from `main`, so they can be tested within the same pull request.
- The repository toggle _Settings → Copilot → Code review → "Use custom instructions when reviewing pull requests"_ must be enabled for them to take effect.
- Automatic review requests are a branch ruleset option ("Automatically request Copilot code review"), not a workflow file.
- The policy itself applies on the basis of the **trusted base revision**: if a PR changes `AGENTS.md` or a similar file, that change is reviewed as content and does not govern the review of the PR that introduces it.

## Criteria Map for openhab-addons

Verify the current state before making any statement:

```bash
git fetch upstream main
git ls-tree -r --name-only upstream/main | Select-String -Pattern '(^|/)(AGENTS|CLAUDE|GEMINI|REVIEW)\.md$|instructions\.md$|copilot|\.github/skills'
```

State as of 2026-10-07 (`upstream/main`):

- **Present:** `AGENTS.md` in the repository root — the actual rulebook; `CLAUDE.md` (only `@AGENTS.md`); `GEMINI.md`; path-specific `bundles/org.openhab.binding.knx/AGENTS.md` and `bundles/org.openhab.persistence.timescaledb/AGENTS.md`.
- **Absent:** `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `.github/skills/**/SKILL.md`, `REVIEW.md`, MCP configuration.
- **No Copilot workflow:** `.github/workflows/` contains only `ci-build.yml`, `rebuild.yml`, `resolver.yml`, and `stale-issues.yml`.

Publicly queryable without authentication: <https://api.github.com/repos/openhab/openhab-addons/rulesets>.

## The openHAB Review Policy

Source: <https://github.com/wborn/github-review-policy> — MIT-licensed, vendor-neutral, maintained by openHAB maintainer Wouter Born, and used for AI-assisted reviews of openHAB pull requests.

Read it live instead of quoting a snapshot:

```bash
curl -s https://raw.githubusercontent.com/wborn/github-review-policy/main/policy/generic.md
curl -s https://raw.githubusercontent.com/wborn/github-review-policy/main/policy/openhab.md
```

Structure:

- `policy/generic.md` — 20 sections: review invariants; scope, coverage, and trusted inputs; finding scope; draft PRs; re-reviewing; technical investigation and evidence; confidence and severity (High/Medium/Low as **internal metadata only**); language and review voice; AI positioning; AI disclosure; review comments; suggested changes; source-code comment quality; links and references; review summary; review outcome; no-blocking-issues handling; presentation and authorization; submission verification; review-thread resolution; workflow checklist.
- `policy/openhab.md` — OH.1 project guidance; OH.2 add-ons and bindings (handler and service lifecycle, discovery, Thing/Channel/configuration definitions, metadata, i18n, error and status handling, cleanup, communication/API behavior, tests); OH.3 OSGi, Karaf, and shared infrastructure; OH.4 static-analysis reports from the PR build.
- `skill/SKILL.md` and `skill/references/*` — the same policy packaged as a portable agent skill; `github-review-policy.md` is the generated combined policy.

Rules from that policy that are visible in the pull request text:

- **Language:** US English, no first-person reviewer/AI wording (`I`, `we`, `my`, `our`, and contractions) — a hard requirement.
- **AI disclosure:** exactly one notice per review. The first review of a PR by the same user starts with `_This is an initial AI-assisted review._`, or `_This is an additional AI-assisted review._` when a substantive maintainer review already exists; every subsequent review closes with `_This review was AI-assisted._`.
- **Finding scope:** only issues introduced or materially worsened by the PR; pre-existing issues are non-blocking, and a changed line does not automatically make an old issue new.
- **Outcome:** `REQUEST_CHANGES` only when something genuinely must be addressed before merge, `COMMENTED` for non-blocking feedback and for a no-further-issues result, `APPROVE` only when explicitly requested. An AI review never replaces maintainer approval.
- **Inline over summary:** findings tied to a concrete code location belong in an inline comment; suggested changes only when the exact, directly applicable replacement is known.
- **OH.4:** report static-analysis findings only when newly introduced or materially worsened, link the report once per review, and link a rule's documentation on its first occurrence.

## Recipe A — Determine the Criteria for a Pull Request

1. Fetch the PR head and read the instructions of that exact revision — this is what the bot sees:

   ```bash
   git fetch upstream pull/<PR-NUMBER>/head:pr-<PR-NUMBER>
   git show pr-<PR-NUMBER>:AGENTS.md
   ```

1. Check whether a closer `AGENTS.md` applies to the changed paths, for example `bundles/<binding>/AGENTS.md`.
1. Check the repository and organization level (write access required): _Settings → Copilot → Code review_ and _Settings → Rules → Rulesets_.
1. Inspect the PR itself: reviews by `copilot-pull-request-reviewer[bot]`, the AI notices of maintainer reviews, and references to `OH.1`–`OH.4`, which prove which policy revision was in effect.
1. Read the policy live and ask in the PR when anything remains unclear.

## Recipe B — Review Against This Policy

1. Load the policy files live, plus `git show <head-sha>:AGENTS.md`, `rules/openhab-review-checklist.md`, and `rules/openhab-coding-guidelines.md`.
1. Establish the complete PR state: HEAD SHA, base, every changed file, PR description, linked issues, existing reviews and threads.
1. For re-reviews, first verify whether previous findings are genuinely fixed, then look for regressions; do not repeat anything that has been fixed.
1. Build findings only on concrete evidence — implementation, repository conventions, tests, CI, documentation, specifications, upstream behavior — and keep severity internal.
1. Apply the review-text gates: US English, no first-person wording, exactly one AI notice, issue and PR references as `#123` or `org/repo#123`, commits as a full SHA in plain text, source-code links as immutable permalinks pinned to a commit SHA.
1. Present the proposal — summary, all inline comments, intended review state, and any thread resolutions — and write to GitHub only after explicit authorization. Afterwards read the review back and confirm it with a clickable link to that exact review.
1. For a local-only review without GitHub write access, produce the same structure as a report.

## Output Format

```markdown
## Review Criteria: <PR or repository>

**Track:** GitHub Copilot code review bot | AI-assisted maintainer review
**Instruction sources:** AGENTS.md (root) | nearest AGENTS.md: <path> | .github/copilot-instructions.md | none
**Policy revision read:** <URL and date>

### Findings

| # | File:Line | Severity | Finding | Evidence | Suggested direction |
|---|---|---|---|---|---|

### Summary

X blocking, Y non-blocking. Review outcome that the policy would produce: <REQUEST_CHANGES | COMMENTED | APPROVE>.
```

Keep severity internal to the analysis, state file and line for every finding, and never claim a build, test, or CI result that was not actually observed.

## Cross-Check Standards

Cross-check all findings against:

- `rules/openhab-review-checklist.md` — the primary 44-item checklist
- `rules/java-coding-rules.md` — project-specific Java rules
- `rules/openhab-coding-guidelines.md` — official guidelines
- `rules/markdown-rules.md` — markdownlint compliance for README and ADR files

## Limitations

- Organization custom instructions and non-public rulesets cannot be inspected from the outside; `GET /orgs/openhab/rulesets` returns 401 without authentication.
- The exact Copilot model revision and GitHub's prompt assembly are not disclosed; only the input files listed above and the observed review behavior are verifiable.
- This role documents the state of 2026-10-07 and must re-verify repository and policy content on every run.

## Sources

- Repository criteria: <https://github.com/openhab/openhab-addons/blob/main/AGENTS.md>
- Copilot review example (bot): <https://github.com/openhab/openhab-addons/pull/21495#pullrequestreview-5028965495> with inline comment <https://github.com/openhab/openhab-addons/pull/21495#discussion_r3861527668>
- AI-assisted maintainer reviews: <https://github.com/openhab/openhab-addons/pull/21843#pullrequestreview-5407989027>, <https://github.com/openhab/openhab-addons/pull/21653#pullrequestreview-5420321270>
- Review policy: <https://github.com/wborn/github-review-policy>
- GitHub documentation: <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions>, <https://docs.github.com/en/copilot/reference/custom-instructions-support>
- Community reference on usage: <https://community.openhab.org/t/what-to-do-with-my-ai-generated-bindings/170393/4>
