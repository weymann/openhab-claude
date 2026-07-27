#!/usr/bin/env python3
"""
PreToolUse guard hook for the openHAB Claude pipeline.

Enforces three rules from CLAUDE.md at the tool-call level, regardless of
which subagent ($Architect, $Dev, $QA, ...) is attempting the write:

1. pom.xml is protected: any Edit/Write/MultiEdit targeting a pom.xml
   requires explicit human approval -> permissionDecision "ask".
2. The i18n folder (src/main/resources/OH-INF/i18n/) is off-limits to
   direct edits: it may only be generated via
   `mvn i18n:generate-default-translations` -> permissionDecision "deny".
3. Archived changes (docs/changes/archive/) are immutable: once a change
   folder has been archived by $Release, no role may Edit/Write into it
   again -> permissionDecision "deny". $Release populates this folder via
   a shell `mv`, not via the Edit/Write tools, so this rule never blocks
   the archiving step itself.

Reads the PreToolUse hook payload from stdin and writes a decision to
stdout using Claude Code's hookSpecificOutput JSON schema. No output
(exit 0, empty stdout) means "no opinion" -> default allow.
"""
import json
import sys


def get_paths(tool_name: str, tool_input: dict) -> list[str]:
    """Extract every file path this tool call would touch."""
    paths = []
    if tool_name in ("Edit", "Write", "NotebookEdit"):
        p = tool_input.get("file_path") or tool_input.get("notebook_path")
        if p:
            paths.append(p)
    elif tool_name == "MultiEdit":
        p = tool_input.get("file_path")
        if p:
            paths.append(p)
    return paths


def decide(path: str):
    normalized = path.replace("\\", "/")

    if normalized.rstrip("/").split("/")[-1] == "pom.xml":
        return "ask", (
            "pom.xml is protected by CLAUDE.md: only $Architect may propose "
            "dependency changes, and every change needs explicit human "
            "approval before being applied. Confirm this change is expected "
            "and was proposed via the $Architect dependency-proposal process."
        )

    if "src/main/resources/OH-INF/i18n/" in normalized or normalized.endswith(
        "src/main/resources/OH-INF/i18n"
    ):
        return "deny", (
            "The i18n folder is off-limits per CLAUDE.md: translation files "
            "are generated exclusively via "
            "`mvn i18n:generate-default-translations`. Add/change keys in "
            "thing-types.xml or addon.xml instead."
        )

    if "docs/changes/archive/" in normalized:
        return "deny", (
            "docs/changes/archive/ is immutable per CLAUDE.md: archived "
            "changes are historical record and must never be edited after "
            "the fact. If the spec was wrong, open a new change instead."
        )

    return None, None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return  # malformed input -> no opinion, let it through

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    for path in get_paths(tool_name, tool_input):
        decision, reason = decide(path)
        if decision:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }))
            return

    # No match on any path touched by this call -> no opinion.


if __name__ == "__main__":
    main()
