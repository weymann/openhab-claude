# openHAB Coding Guidelines

> Source: <https://www.openhab.org/docs/developer/guidelines.html>

The following guidelines apply to all (Java) code of the openHAB project.
They must be followed to ensure a consistent code base for easy readability and maintainability.
Exceptions can certainly be made, but they should be discussed and approved by a project maintainer upfront.

This list also serves as a checklist for code reviews on pull requests.

---

## A. Directory and File Layout

```text
|- doc                    Images and other assets used in the README.md
|- src/main
|---- feature
|-------- feature.xml     Your OSGi feature file
|---- java                Your Java code
|-------- org/openhab/[...]
|- src/main/resources/OH-INF
|---- addon
|-------- addon.xml       Binding name, description and other meta data
|---- config              Configuration description files when not in things files
|-------- *.xml
|---- i18n                Your localized binding texts
|-------- *_<local>.properties
|---- thing               One or more xml files with thing descriptions
|-------- *.xml
|- src/test
|---- java                Unit tests
|-------- org/openhab/[...]
|---- resources           Resource files used in unit tests
|-------- [...]
|- NOTICE                 License information (3rd party content)
|- pom.xml                Build system file: dependencies
|- README.md              Binding description
```

- Every Java file must have a license header. Run `mvn license:format` on the root of the repo to automatically add missing headers.

---

## B. Code Formatting Rules & Style

### Naming Convention

| Element | Convention |
|---|---|
| Thing type id | `lower-case-hyphen` |
| Channel type id | `lower-case-hyphen` |
| Channel group id | `lower-case-hyphen` |
| Channel id | `lower-case-hyphen` |
| Thing property | `camelCase` |
| Config parameter | `camelCase` |
| Profile URI | `lower-case-hyphen` |
| Profile type id for transformations | `UPPER_CASE` |
| XML files in src/*/resources | `lower-case-hyphen.xml` |

### Code Format

Rules are enforced via [Spotless Maven Plugin](https://github.com/diffplug/spotless).

- Check: `mvn spotless:check` (or `mvn spotless:check -Dspotless.check.skip=false`)
- Fix: `mvn spotless:apply`

Code style files: <https://github.com/openhab/static-code-analysis/tree/main/codestyle/src/main/resources>

#### Java Code

Uses Eclipse Java Formatter definitions.

- **Eclipse IDE**: preconfigured via [openHAB Eclipse IDE setup](https://www.openhab.org/docs/developer/ide/eclipse)
- **Eclipse standalone**: import [openhab_codestyle.xml](https://raw.githubusercontent.com/openhab/static-code-analysis/main/codestyle/src/main/resources/openhab_codestyle.xml) and [openhab.importorder](https://raw.githubusercontent.com/openhab/static-code-analysis/main/codestyle/src/main/resources/openhab.importorder)
- **IntelliJ**: use [Eclipse Code Formatter plugin](https://plugins.jetbrains.com/plugin/6546-eclipse-code-formatter) with the same files

#### XML Files

- `pom.xml`: 2 space indentation
- Other XML files: 1 tab indentation
- Line length: 120 characters

### Java Coding Style

- Follow [Java naming conventions](https://java.about.com/od/javasyntax/a/nameconventions.htm):
  - Variables: `lowerCamelCase`
  - Constants: `ALL_UPPER_CASE`
- Use generics where applicable:

```java
public static <T> boolean isEqual(GenericsType<T> g1, GenericsType<T> g2) {
    return g1.get().equals(g2.get());
}
```

- Code **must not** show any warnings. Use `@SuppressWarnings` only when unavoidable.
- Classes are generally organized within an `internal` package:

```java
org.openhab.binding.coolbinding.internal
org.openhab.binding.coolbinding.internal.handler
org.openhab.binding.coolbinding.internal.discovery
```

- Every class (except DTOs) must be annotated with `@NonNullByDefault`. See [Null Annotations](#null-annotations).
- Use OSGi Declarative Services annotations:

```java
@Component(service=MyCoolService.class)
public class MyCoolService {
    @Reference
    private @NonNullByDefault({}) ItemRegistry itemRegistry;
}
```

### Markdown Format

Rules defined in [.markdownlint.yaml](https://github.com/openhab/openhab-docs/blob/main/.github/.markdownlint.yaml), enforced automatically when a README.md is part of a change.

Check locally: `mvn clean install -P check-markdown`

---

## C. Documentation

JavaDoc is **required** for every:

- class
- interface
- enumeration (except inner classes and enums)
- constant, field and method with visibility of default, protected or public

An `@author` tag is required for every author who made a substantial contribution. New `@author` tags go below older ones. DTOs (data-transfer-objects that map from JSON/XML) do not require JavaDoc.

---

## D. Language Levels and Libraries

1. Target: **Java 21** (long-term support release)
1. Target: **OSGi Core Release 8** / **OSGi Compendium Release 8** — do not use newer features
1. Use **SLF4J** for logging

See [Default Libraries](#default-libraries) for available third-party libraries.

---

## E. Runtime Behavior

1. Overridden methods must return fast. Schedule expensive operations as jobs.
1. **Do not create threads.** Use existing schedulers. For jobs without a fixed rate, prefer `scheduleWithFixedDelay` over `scheduleAtFixedRate`.
1. Bundles must cleanly start and stop without exceptions. Test with `stop <bundle-id>` / `start <bundle-id>` from the console.
1. Bundles must not require substantial CPU time.

---

## F. Logging

### Logger Setup

Loggers should be non-static, `final`, and named `logger`:

```java
class MyCoolClass {
    private final Logger logger = LoggerFactory.getLogger(MyCoolClass.class);
}
```

### Parameterized Logging

Always use parameterized logging (not string concatenation):

```java
logger.debug("Current value is {} and int is {}", someValue, someInt);
```

### Exception Logging

```java
try {
    doSomething();
} catch (IOException e) {
    logger.warn("Explain what went wrong. Argument: {}.", someVariable, e);
}
```

For configuration errors, use `e.getMessage()` — no stack trace needed.

### DON'Ts

```java
// DON'T: trace entry/exit
logger.trace("Enter myfun");
doSomething();
logger.trace("Leave myfun");

// DON'T: log instead of updating framework state
logger.debug("And now the thing goes online");
updateState(ThingState.ONLINE); // do this, not the log above
```

### Log Level Guidelines

| Level | When to use |
|---|---|
| `error` | System cannot function, immediate action required, or irrecoverable bug to report |
| `warn` | Something seems wrong but system functions normally; recoverable situations in non-normal code paths |
| `info` | Sparingly — newly started components, user files loaded |
| `debug` | Unexpected behavior details; temporary problems like connection issues (reflect in Thing status too) |
| `trace` | Verbose output, e.g. large payloads when debugging external API changes |

**Important:** Bindings should **NOT** log error/warn for dropped connections — that's normal/expected behavior. Update the Thing status instead. All Thing status events are already logged by the framework.

---

## G. Other Code Attributions

Compatible licenses for copied code: Apache, Eclipse v1, MIT, BSD. Stackoverflow snippets are automatically MIT licensed.

- Do not remove author attributions or modify license headers in copied files.
- Add filename, author and license to the `NOTICE` file (except for short snippets).

---

## Guideline Details

### Static Code Analysis

The Maven build includes [static code analysis tooling](https://github.com/openhab/static-code-analysis).

- Per-bundle report: `path/to/bundle/target/code-analysis/report.html`
- Full build report: `target/summary_report.html`
- Priority 1 (error) → Maven build fails
- Priority 2 (warning) / Priority 3 (info) → listed on console

### Null Annotations

Uses [Eclipse JDT null annotations](https://wiki.eclipse.org/JDT_Core/Null_Analysis).

All classes (except DTOs) must have `@NonNullByDefault`:

```java
@NonNullByDefault
public class MyClass() {}
```

Nullable fields:

```java
private @Nullable MyType myField;
```

Using a nullable field (requires local copy for thread safety):

```java
private void myFunction() {
    final MyType myField = this.myField;
    if (myField != null) {
        myField.doSomething();
    }
}
```

Nullable return types:

```java
private @Nullable MyReturnType myMethod() {};
```

OSGi service references (OSGi guarantees non-null, compiler doesn't know):

```java
@Reference
private @NonNullByDefault({}) MyService injectedService;
```

### Default Libraries

#### XML Processing

- `com.thoughtworks.xstream`
- `com.thoughtworks.xstream.annotations`
- `com.thoughtworks.xstream.converters`
- `com.thoughtworks.xstream.io`
- `com.thoughtworks.xstream.io.xml`

#### JSON Processing

- `com.google.gson.*`

#### HTTP Operations

- `org.eclipse.jetty.client.*`
- `org.eclipse.jetty.client.api.*`
- `org.eclipse.jetty.http.*`
- `org.eclipse.jetty.util.*`

> **Note:** Obtain `HttpClient` instances via `HttpClientFactory` service. Use the shared instance unless specific configuration is required.

#### WebSocket Operations

- `org.eclipse.jetty.websocket.client`
- `org.eclipse.jetty.websocket.api`

> **Note:** Obtain `WebSocketClient` instances via `WebSocketClientFactory` service.

#### Server Sent Events (SSE)

- `javax.ws.rs.client`
- `javax.ws.rs.core`
- `javax.ws.rs.sse`
