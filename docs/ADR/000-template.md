# ADR-000: [Short Title of the Decision]

## Status

> `Proposed` | `Accepted` | `Deprecated` | `Superseded by ADR-XXX`

## Context

What is the problem, requirement, or situation that makes this decision necessary?
Describe the forces at play — technical constraints, openHAB API limitations, device behavior, etc.

## Decision

What was decided?
State it clearly and directly: "We will use X because Y."

## Consequences

### Positive
- What becomes easier or better as a result?

### Negative
- What becomes harder, more complex, or is accepted as a trade-off?

## Diagram (optional)

Use a Mermaid diagram if it helps visualize the decision — e.g. class relationships, sequence flows, or component boundaries.

**Class diagram example:**
```mermaid
classDiagram
    class MyDeviceHandler {
        +initialize()
        +dispose()
        +handleCommand()
    }
    class MyDeviceConfig {
        +host: String
        +refreshInterval: int
    }
    MyDeviceHandler --> MyDeviceConfig : uses
```

**Sequence diagram example:**
```mermaid
sequenceDiagram
    participant H as ThingHandler
    participant S as Scheduler
    participant D as Device

    H->>S: scheduleWithFixedDelay(poll)
    S->>H: poll()
    H->>D: HTTP GET /status
    D-->>H: 200 OK
    H->>H: updateState(channel, value)
```

**Component diagram example:**
```mermaid
graph TD
    A[MyDeviceHandler] -->|uses| B[MyDeviceConfig]
    A -->|creates| C[MyDeviceDiscoveryService]
    A -->|HTTP| D[Device API]
```

---

*Replace this template content. Remove unused sections and diagrams.*
