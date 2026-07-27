# openHAB PR Review Checklist

> Source: <https://github.com/openhab/openhab-addons/wiki/Review-Checklist>  
> Use: Only on explicit request (e.g. "review checklist", "PR review")

## Structure & Build

1. Proper bundle name in pom.xml (`"openHAB Add-ons :: Bundles :: ... Binding"`)
1. New bundle included in build (main pom.xml) and karaf feature (`src/main/feature` of the bundle)
1. EPLv2 license with NOTICE file present

## Documentation & i18n

1. All dependencies listed in NOTICE file
1. README based on [official template](https://github.com/openhab/openhab-core/blob/master/tools/archetype/binding/src/main/resources/archetype-resources/README.md), same sections present
1. README: new line after every sentence
1. README: section headers capitalized ("Thing Configuration", not "Thing configuration")
1. README: all thing type ids, channel ids, config parameter keys mentioned in appropriate sections
1. i18n: only original language provided (translations managed via Crowdin)
1. Copyright year in source file headers correct — auto-fix: `mvn -lp :<binding-artifactid> license:format`

## Thing & Channel Design

 1. Thing/Channel labels short (<25 chars, max 2-3 words) and capitalized
 1. Things and Channels have [semantic tags](https://next.openhab.org/docs/developer/bindings/thing-xml.html#tagging-conventions-for-commonly-confused-use-cases) where possible
 1. Thing config parameters: units specified where applicable (e.g. `unit="s"`)
 1. Thing config parameters: min/max values specified where applicable
 1. Thing config parameters: `context` tag added where applicable (e.g. `<context>network-address</context>`)
 1. Channel declarations use Units of Measure (e.g. `Number:Temperature`)
 1. Representation property specified in discovery results

## Handler & Runtime

 1. `handler.initialize()` returns fast and sets a valid Thing status
 1. All asynchronous futures created during `initialize` cleaned up in `dispose`
 1. REFRESH commands handled
 1. Lambdas used for runnables

## Logging

 1. Conservative use of log levels (mainly `debug`, unless bugs or misconfiguration)
 1. Don't log if a Thing goes offline — pass text to `updateStatus()` instead (framework logs it)
 1. Log stack traces only on severe errors (bug detection)

## Code Quality

 1. `@NonNullByDefault` added to every class (exception: classes with DTO suffix or in `dto` package)
 1. Non-static fields and variables use camelCase (no underscores or prefixes)
 1. Primitive types preferred over boxed types (e.g. `int` vs. `Integer`)
 1. Duplicate code refactored where possible
 1. Result of `getConfigAs()` and `getConfiguration()` cached
 1. All byte[]/String conversions specify Charset (including Stream→Reader/Writer conversions)
 1. Sockets and I/O streams used in try-with-resources where possible

## Error & Thread Handling

 1. Checked exceptions used: custom exceptions extend `Exception`
 1. `RuntimeException` not thrown on expected errors
 1. `Exception` not caught unless an external method throws it — catch `RuntimeException` for unexpected errors
 1. Any `IOException` catch also handles `InterruptedIOException`
 1. On `InterruptedException` or `InterruptedIOException`: return from method ASAP (unless in binding-managed thread)
 1. Created threads declared as daemon: `Thread.setDaemon(true)`
 1. Created threads named via `Thread.setName()` or constructor
 1. `synchronized` on Handler methods reviewed carefully (risk of deadlock with parent class)
 1. Cancelling a `Future`: no need to check if already cancelled

## Static Analysis

 1. Compiler warnings annotated with `@SuppressWarnings` where unavoidable
 1. Checkstyle: `target/code-analysis/report.html` checked
 1. Formatting: `mvn spotless:check -Dspotless.check.skip=false`
 1. JavaDoc: `mvn javadoc:javadoc`
