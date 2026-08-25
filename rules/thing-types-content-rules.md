# Thing Type & Config Description Content Rules

> This file collects content/wording conventions for `label` and `description` text in
> `thing-types.xml`, `addon.xml`, and config-description XML files.
> Loaded for `$Architect`, `$Dev`, and `$Generate` whenever writing or reviewing XML label/description text.

---

## `description` is UI help text, not documentation

`description` is shown to the end user in the openHAB UI (e.g. Main UI's channel/config tooltips).
It must read like a slightly more detailed label — not like a spec excerpt or an internal note.

- Length: one sentence, at most two short sentences.
- State what the value/channel *is* (and its unit, if relevant) — not how it behaves internally, not why it exists.
- Do not explain functionality, algorithms, state machines, or edge cases. That belongs in JavaDoc, the ADR, or the spec.
- Do not reference ADRs, `CONCEPT.md`, scenario names, or any other project document (e.g. "see docs/ADR/024-...",
  "per Scenario 2 (isLimitActive)"). The person reading the UI has no access to the repository.

### Example

Bad — too long, explains behavior, cites an ADR:

```text
Subject Key Identifier of the remote device this Entity lives on (40 hex characters). Optional - left blank, it is
auto-selected once the parent Bridge trusts exactly one device (nothing to choose between); with zero or more than
one trusted device, pick one manually. Offered as a selectable list of the parent Bridge's currently trusted SKIs
(docs/ADR/024-oh-device-oh-entity-rename.md) - free text entry remains possible for a SKI not yet trusted, but this
Thing stays offline until the parent Bridge actually trusts it (see the Bridge's Trusted SKIs config).
```

Good:

```text
Subject Key Identifier of the remote device this Entity lives on (40 hex characters). Optional if the parent Bridge
trusts exactly one device; otherwise pick one from the trusted list.
```

Bad — cites a scenario name and a doc section:

```text
The power limit value the paired Energy Guard has configured to apply if the connection is lost, per Scenario 2
(FailsafeConsumptionActivePowerLimit/FailsafeProductionActivePowerLimit) - see CONCEPT.md §5.4.3. Read-only: set
exclusively by the Energy Guard over EEBus, never from openHAB.
```

Good:

```text
Power limit applied automatically if the connection to the Energy Guard is lost. Read-only, set by the Energy Guard. (W)
```

---

## Where the longer explanation goes instead

Functional details, ADR references, and scenario/spec mappings belong in:

- JavaDoc on the corresponding Java field, handler, or DTO.
- The ADR itself (`docs/ADR/`).
- The spec (`docs/specs/`) or change proposal (`docs/changes/<change-id>/`).

`description` in XML stays end-user help text; it is never the place project documentation gets duplicated into.
