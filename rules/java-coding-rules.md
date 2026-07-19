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

### Persistent state — use `StorageService`, not custom persistence

Any state that must survive across the Thing/binding lifecycle (restarts, OSGi bundle reloads) is persisted via [`org.openhab.core.storage.StorageService`](https://www.openhab.org/javadoc/latest/org/openhab/core/storage/package-summary) — never custom file I/O, in-memory-only maps, or ad-hoc serialization. Inject `StorageService` via the constructor (per the dependency-injection rule above), typically into the handler factory, which passes it on to the handler. Decide the storage key namespace (typically `thing.getUID().toString()`) as part of the handler design, and document the decision as an ADR when introducing `StorageService` usage to a binding for the first time.

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

---

### Never catch `Throwable`

Catch the specific exception type(s) you can meaningfully handle (e.g. `IOException`, `JsonSyntaxException`). Catching `Throwable` (or `Error`) also swallows `OutOfMemoryError`, `StackOverflowError`, etc., which must never be silently handled.

```java
// WRONG
try {
    doSomething();
} catch (Throwable t) {
    logger.warn("Failed: {}", t.getMessage());
}

// CORRECT
try {
    doSomething();
} catch (IOException | JsonSyntaxException e) {
    logger.warn("Failed: {}", e.getMessage());
}
```

If multiple unrelated exception types genuinely need the same handling, catch them explicitly with a multi-catch (`A | B`) rather than widening to `Exception`/`Throwable`.

---

### No `System.out` / `System.err` — use the logger

Never use `System.out.println(...)` or `System.err.println(...)`, including in tests. Use the SLF4J `logger` (production code) or, for test diagnostics, assertion messages / test logger — not console output.

```java
// WRONG
System.out.println("Result: " + result);

// CORRECT
logger.debug("Result: {}", result);
```

---

### Use `isEmpty()` instead of `size() == 0`

Replace `size() == 0`, `size() != 0`, `size() > 0`, and `size() < 1` with `isEmpty()` / `!isEmpty()`:

```java
// WRONG
if (list.size() == 0) { ... }
if (list.size() > 0) { ... }

// CORRECT
if (list.isEmpty()) { ... }
if (!list.isEmpty()) { ... }
```

---

### `@NonNullByDefault` applies to every type, including enums and interfaces

The `@NonNullByDefault` requirement above is not limited to top-level classes — it must also be added to **every enum, interface, record, and inner/nested type** (e.g. domain enums, repository/service interfaces, exception classes). When creating any new type, check it carries the annotation before considering the file done.

---

### Commons Math: only use supported `org.apache.commons.math3.optim.*` linear-optimization packages

When using Apache Commons Math's Simplex solver for linear programming, import only from the `org.apache.commons.math3.optim` / `org.apache.commons.math3.optim.linear` packages as approved in the project's dependency. If static analysis flags these imports as "should not be used", recheck against the `pom.xml`-approved Commons Math version/API and raise with `$Architect` — resolving it may require a dependency change (pom.xml is protected, human approval required).

---

### `StorageService` — lifecycle-bound persistence pattern

Obtain the `Storage<T>` instance in `initialize()` from the injected `StorageService`, and remove the entry in `handleRemoval()` — not in `dispose()`. `dispose()` runs on every disable/update/restart cycle; `handleRemoval()` only runs when the Thing is actually deleted, so that is the only place stored data should be discarded.

```java
private @Nullable Storage<MyState> storage;

@Override
public void initialize() {
    storage = storageService.getStorage(thing.getUID().toString(), MyState.class.getClassLoader());
    // ... read/restore state from storage as needed
    updateStatus(ThingStatus.UNKNOWN);
    scheduler.execute(this::connect);
}

@Override
public void handleRemoval() {
    Storage<MyState> storage = this.storage;
    if (storage != null) {
        storage.remove(thing.getUID().toString());
    }
    updateStatus(ThingStatus.REMOVED);
}
```

Do not remove the storage entry in `dispose()` — doing so would wipe persisted state on every binding restart or Thing update, not just on deletion.
