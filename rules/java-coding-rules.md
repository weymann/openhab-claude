# Custom Java Coding Rules

> This file extends the official openHAB coding guidelines with project-specific rules.
> Add your own rules here whenever you find patterns that Claude should always follow in your codebase.
> Testing conventions and reusable test fixtures live in `rules/testing-rules.md`.

### License header — required on every Java file

Every new Java file must start with this exact license header:

```java
/*
 * Copyright (c) 2010-{CURRENT_YEAR} Contributors to the openHAB project
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

Replace `{CURRENT_YEAR}` with the actual current year when creating the file (e.g. `2026`).

The header must appear before the `package` declaration. No blank line between the header and `package`.

---

### Java 21 — prefer modern language features

This project targets **Java 21**. Prefer modern language features over older patterns whenever they improve readability and safety:

```java
// Records for simple immutable data carriers
public record WeatherData(double temperature, double humidity) {}

// Pattern matching for instanceof — no explicit cast needed
if (command instanceof QuantityType<?> quantity) {
    double value = quantity.doubleValue();
}

// Switch expressions with pattern matching
String description = switch (status) {
    case ONLINE -> "Device is reachable";
    case OFFLINE -> "Device is unreachable";
    case CONFIGURATION_ERROR -> "Check configuration";
    default -> "Unknown status";
};

// Text blocks for multi-line strings (e.g. JSON, SQL, HTTP bodies)
String json = """
        {
          "key": "value"
        }
        """;

// var for local variables when the type is obvious from the right-hand side
var client = new HttpClient();
```

Guidelines:

- Use **records** for immutable DTOs / value objects (e.g. API response models) instead of plain classes with only getters.
- Use **pattern matching for `instanceof`** to eliminate redundant casts.
- Use **switch expressions** (`->` syntax) instead of classic `switch` statements with `break`, especially for enum handling.
- Use **text blocks** for embedded JSON, SQL, or other multi-line string literals.
- Use **`var`** for local variable declarations where the type is clear from context; do not use it when it would reduce readability (e.g. `var result = compute();` is fine, `var x = 5;` should stay `int x = 5;` if clarity matters).
- **Sealed classes/interfaces** may be used to model a fixed set of related types (e.g. command hierarchies), but only when the openHAB pattern doesn't already dictate a different structure.
- **Virtual threads** are not used for openHAB scheduler/thread-pool tasks unless explicitly approved by `$Architect` — openHAB's threading model (`ScheduledExecutorService` via `ThreadPoolManager`) remains the default.

> ⚠️ Java 21 deviates from the common openHAB baseline (often Java 17). Confirm the binding's `pom.xml` `maven.compiler.release` / `release` property targets 21 — this is `pom.xml`-protected and requires `$Architect` + human approval (see global rules).

---

### Null checks — NEVER throw NullPointerException explicitly

Always use `IllegalArgumentException` with a descriptive message when validating null arguments:

```java
// CORRECT
if (itemName == null) {
    throw new IllegalArgumentException("itemName is null");
}

// WRONG — PMD rule "AvoidThrowingNullPointerException" will fail the build
if (itemName == null) {
    throw new NullPointerException("...");
}
```

The message format must be: `"<paramName> is null"` (e.g. `"itemName is null"`, `"slots is null"`).

---

### @NonNullByDefault — required on every class/interface/enum

Every new class, interface, record, or enum must be annotated:

```java
import org.eclipse.jdt.annotation.NonNullByDefault;

@NonNullByDefault
public final class MyClass { ... }
```

This makes all fields, parameters, and return types non-null by default and satisfies the openHAB static analysis requirement.

---

### Javadoc for thrown exceptions

When a method throws `IllegalArgumentException` for a null argument, document it with `@throws`:

```java
* @throws IllegalArgumentException if {@code itemName} is {@code null} or blank
```

---

## Architecture Rules ($Architect)

### Single Responsibility per class

Every class has one clear, nameable purpose. If a class name contains "and", or is a generic `*Manager`/`*Helper`/`*Util`, treat it as a signal to split responsibilities.

---

### Dependency injection over `new` in business logic

Inject dependencies (HTTP clients, schedulers, providers) via the constructor rather than constructing them inline in business logic. This keeps classes testable and mockable without static/global state.

```java
// CORRECT — dependency passed in, easy to mock in tests
public MyApiClient(HttpClient httpClient, Gson gson) {
    this.httpClient = httpClient;
    this.gson = gson;
}

// AVOID — hidden dependency, hard to test
public MyApiClient() {
    this.httpClient = new HttpClient();
    this.gson = new Gson();
}
```

---

### Package-by-feature

Organize packages by feature/responsibility, not by technical layer:

```text
internal/
├── discovery/
├── handler/
├── api/
└── config/
```

Avoid generic catch-all packages such as `internal/models`, `internal/utils`, or `internal/common` — place classes next to the feature that uses them.

---

### Consistent naming conventions per layer

| Suffix | Purpose |
|--------|---------|
| `*Client` / `*Connection` | API / network communication |
| `*Handler` | Thing handler (extends `BaseThingHandler`) |
| `*Configuration` | Config POJO bound to `thing-types.xml` parameters |
| `*Dto` / `*Response` | API response models (deserialization targets) |
| `*Mapper` / `*Converter` | Translates between API models and openHAB types (`State`, `ThingStatus`, etc.) |

---

### Document the error escalation strategy

Each binding documents, as an ADR, how errors propagate:

- Which exceptions are logged and swallowed (recoverable, e.g. transient network blip).
- Which exceptions are translated into a `ThingStatus` (e.g. `COMMUNICATION_ERROR`, `CONFIGURATION_ERROR`).
- Which exceptions are rethrown / fail fast (programming errors, invalid configuration at startup).

---

## Developer Rules ($Dev)

### No magic numbers or strings

Extract repeated literals — timeouts, retry counts, channel IDs, config keys — into named constants:

```java
// CORRECT
private static final int TIMEOUT_SECONDS = 30;
private static final String CHANNEL_TEMPERATURE = "temperature";

// WRONG
client.setTimeout(30);
updateState("temperature", value);
```

---

### Prefer immutability

Mark fields `final` where possible. When returning collections that callers must not mutate, return an unmodifiable view or a defensive copy (`List.copyOf(...)`, `Map.copyOf(...)`).

---

### Logging level convention

| Level | Use for |
|-------|---------|
| `trace` | Raw payloads, full request/response bodies |
| `debug` | Control flow, state transitions, decisions |
| `warn`  | Recoverable errors, retries, degraded operation |
| `error` | Unexpected/fatal conditions only |

Never log secrets, tokens, passwords, or other credentials — not even at `trace` level.

---

### Try-with-resources for all `Closeable` resources

```java
try (InputStream in = connection.getInputStream()) {
    // ...
}
```

Applies to HTTP responses, streams, and any other `AutoCloseable`/`Closeable` resource.

---

### Keep methods short

If a method doesn't fit on one screen, extract private helper methods with descriptive names. Long methods are a sign that multiple responsibilities are mixed together.

---

### No empty catch blocks

Every `catch` block does something observable — at minimum a `logger.debug(...)` / `logger.warn(...)` explaining why the exception is considered safe to ignore.

```java
// WRONG
try {
    doSomething();
} catch (IOException e) {
}

// CORRECT
try {
    doSomething();
} catch (IOException e) {
    logger.debug("Ignoring transient I/O error during poll: {}", e.getMessage());
}
```

---

### `@Nullable` / `Optional` consistency

With `@NonNullByDefault` active, use `@Nullable` for fields/parameters/return types that may legitimately be absent (per openHAB convention). Use `Optional<T>` only for method return types where "absence" is a normal, expected outcome (not for fields or parameters). Do not mix both styles for the same kind of value within a class.
