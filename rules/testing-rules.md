# Testing Rules

> This file collects testing conventions and reusable test fixtures.
> Loaded for `$QA` and `$Dev` whenever writing or reviewing unit tests.

---

## Test fixtures — reuse reference mocks from `rules/test-fixtures/`

Reusable test helper classes (mocks, fakes, base test classes) live in `rules/test-fixtures/`.
When writing unit tests (`$Dev`, `$QA`), check this folder first before writing a new mock from scratch.

Available fixtures:

- **`CallbackMock.java`** — implements `ThingHandlerCallback`. Captures channel state updates (`stateMap`), trigger events (`triggerMap`), and thing status (`statusInfo`), with blocking helpers `waitForStatus(...)` / `waitForOnline()` / `getState(...)`. Use this as the callback in `ThingHandler` unit tests instead of a hand-rolled mock.
- **`FileReader.java`** — reads a file (e.g. a JSON HTTP response fixture) into a `String` via `readFileInString(String fileName)`. Use this to load canned API responses from `src/test/resources/` in unit tests instead of inlining JSON strings in test code. Also implements `ResourceProvider.getResourceFile(String)` for `src/main/resources` lookups — adapt or drop that method if the target binding doesn't define a `ResourceProvider` interface.

When adding a new fixture to this folder:

- Keep the openHAB license header and `@author` tag.
- Adjust the `package` declaration to match the target binding (e.g. `org.openhab.binding.<name>.internal.mock`).
- Document the fixture in this list with a one-line description of what it does and when to use it.

---

## JSON HTTP response fixtures — `src/test/resources/`

Canned JSON HTTP responses used in unit tests live under `src/test/resources/` of the target binding (not `src/main/resources/`).
Load them with `FileReader.readFileInString(...)` and feed the result into the JSON deserializer (e.g. Gson) under test.

Naming convention: `<endpoint-or-scenario>.json` (e.g. `current-weather-response.json`, `device-list-empty.json`).

---

## Arrange-Act-Assert structure

Every test method follows the Arrange-Act-Assert pattern, with the three phases visually separated by blank lines (or comments for longer tests):

```java
@Test
void whenApiReturnsEmptyListThenThingGoesOffline() {
    // Arrange
    CallbackMock callback = new CallbackMock();
    ApiClient client = mock(ApiClient.class);
    when(client.getDevices()).thenReturn(List.of());

    // Act
    handler.initialize();

    // Assert
    callback.waitForStatus(ThingStatus.OFFLINE);
}
```

---

## One behavior per test, descriptive names

Each test method verifies exactly one behavior. Test names describe the expected outcome, not the implementation, using a `whenXThenY` camelCase name — no underscore. Checkstyle's `MethodNameCheck` (`^[a-z][a-zA-Z0-9]*$`) rejects underscores in identifiers, including test method names; capitalization alone (`when...Then...`) keeps the name readable without one:

```java
// CORRECT
void whenApiReturnsEmptyListThenThingGoesOffline()
void whenTemperatureChannelLinkedThenStateIsUpdatedInCelsius()
void whenHttpClientThrowsTimeoutThenThingStatusIsCommunicationError()

// WRONG — underscore violates MethodNameCheck
void whenApiReturnsEmptyList_thenThingGoesOffline()

// WRONG — describes implementation, not behavior; tests too much at once
void testHandler()
void testInitializeAndUpdateAndDispose()
```

If a test name needs "and" to describe what it does, split it into multiple tests.

---

## No sleep-based waits

Never use `Thread.sleep(...)` to wait for asynchronous state changes in tests. Use polling with a timeout instead — see `CallbackMock.waitForStatus(...)` / `waitForOnline()` for the established pattern in this project.

```java
// WRONG
handler.initialize();
Thread.sleep(2000);
assertEquals(ThingStatus.ONLINE, thing.getStatus());

// CORRECT
handler.initialize();
callback.waitForOnline();
assertEquals(ThingStatus.ONLINE, thing.getStatus());
```

`Awaitility` (`org.awaitility.Awaitility`) is an acceptable alternative if already a test dependency — but introducing it as a _new_ dependency requires `$Architect` + human approval (pom.xml is protected).

---

## Mandatory edge-case checklist for API clients

Every test class for an HTTP/API client (`*ApiClient`, `*Connection`, etc.) must cover at minimum:

- Happy path — valid response, correctly deserialized.
- Empty response — empty body, empty array/list, or `null` fields.
- HTTP error responses — at least one 4xx (e.g. 401/404) and one 5xx case.
- Malformed JSON — deserialization failure is handled gracefully, not an uncaught exception.
- Timeout / connection failure — mapped to a sensible `ThingStatus` (e.g. `COMMUNICATION_ERROR`), not left as an unhandled exception.

---

## Parameterized tests for mappings and enums

Use `@ParameterizedTest` with `@CsvSource`, `@EnumSource`, or `@MethodSource` for any test that checks a mapping table — e.g. API status codes to `ThingStatus`, raw values to `State` types, or unit conversions. Avoid copy-pasted near-identical test methods.

```java
@ParameterizedTest
@CsvSource({
        "ONLINE, ONLINE",
        "OFFLINE, OFFLINE",
        "UNKNOWN, UNINITIALIZED"
})
void apiStatusMapsToThingStatus(String apiStatus, ThingStatus expected) {
    assertEquals(expected, StatusMapper.map(apiStatus));
}
```

---

## `@SuppressWarnings("null")` on `@NonNullByDefault` test classes using Mockito

Mockito (`mock`, `when`, `ArgumentMatchers`, `ArgumentCaptor`) and several JDK classes used in tests (e.g. `HttpClient`, `HttpResponse`) are not designed with null type annotations in mind. Combined with a `@NonNullByDefault` test class, this produces "unsafe interpretation of method return type as `@NonNull`" compiler advisories at nearly every mocked call — noise, not a real null-safety issue.

Add a class-level `@SuppressWarnings("null")` (merge into an existing `@SuppressWarnings({...})` if the class already has one, e.g. `"unchecked"` for raw Mockito generics) rather than annotating individual call sites, and note why in the class Javadoc:

```java
/**
 * Unit tests for {@link MyHandler}.
 *
 * <p>
 * {@code @SuppressWarnings("null")}: Mockito is not designed with null type annotations in mind, so combining it
 * with this {@code @NonNullByDefault} test class produces "unsafe interpretation" compiler advisories with no
 * null-safety benefit.
 *
 * @author ...
 */
@NonNullByDefault
@SuppressWarnings("null")
class MyHandlerTest {
```

Do not add a defensive `if (x == null)` check to silence this class of warning at a single call site instead — if the compiler already treats the value as `@NonNull` (which is what triggers this advisory), the check becomes unreachable and the compiler flags it as dead code instead, which is worse (a real warning, not just an info-level advisory).

---

## Minimum coverage expectation per new class

- Every new `*Handler` class needs at least one happy-path test (initialize → ONLINE) and one error-path test (initialize → OFFLINE/error status).
- Every new `*ApiClient` / `*Connection` class needs the full edge-case checklist above.
- Every new mapping/converter (status mapping, unit conversion, DTO-to-state mapping) needs a parameterized test covering all enum values or representative input classes.
