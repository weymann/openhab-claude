# Custom Java Coding Rules

> This file extends the official openHAB coding guidelines with project-specific rules.
> Add your own rules here whenever you find patterns that Claude should always follow in your codebase.
> The three rules below serve as examples.

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

### @NonNullByDefault — required on every class/interface/enum
Every new class, interface, record, or enum must be annotated:
```java
import org.eclipse.jdt.annotation.NonNullByDefault;

@NonNullByDefault
public final class MyClass { ... }
```
This makes all fields, parameters, and return types non-null by default and satisfies the openHAB static analysis requirement.

### Javadoc for thrown exceptions
When a method throws `IllegalArgumentException` for a null argument, document it with `@throws`:
```java
* @throws IllegalArgumentException if {@code itemName} is {@code null} or blank
```
