# openHAB PR Review Checklist

> Source: https://github.com/openhab/openhab-addons/wiki/Review-Checklist  
> Use: Only on explicit request (e.g. "review checklist", "PR review")

## Structure & Build
1. Proper bundle name in pom.xml (`"openHAB Add-ons :: Bundles :: ... Binding"`)
2. New bundle included in build (main pom.xml) and karaf feature (`src/main/feature` of the bundle)
3. EPLv2 license with NOTICE file present

## Documentation & i18n
4. All dependencies listed in NOTICE file
5. README based on [official template](https://github.com/openhab/openhab-core/blob/master/tools/archetype/binding/src/main/resources/archetype-resources/README.md), same sections present
6. README: new line after every sentence
7. README: section headers capitalized ("Thing Configuration", not "Thing configuration")
8. README: all thing type ids, channel ids, config parameter keys mentioned in appropriate sections
9. i18n: only original language provided (translations managed via Crowdin)
10. Copyright year in source file headers correct — auto-fix: `mvn -lp :<binding-artifactid> license:format`

## Thing & Channel Design
11. Thing/Channel labels short (<25 chars, max 2-3 words) and capitalized
12. Things and Channels have [semantic tags](https://next.openhab.org/docs/developer/bindings/thing-xml.html#tagging-conventions-for-commonly-confused-use-cases) where possible
13. Thing config parameters: units specified where applicable (e.g. `unit="s"`)
14. Thing config parameters: min/max values specified where applicable
15. Thing config parameters: `context` tag added where applicable (e.g. `<context>network-address</context>`)
16. Channel declarations use Units of Measure (e.g. `Number:Temperature`)
17. Representation property specified in discovery results

## Handler & Runtime
18. `handler.initialize()` returns fast and sets a valid Thing status
19. All asynchronous futures created during `initialize` cleaned up in `dispose`
20. REFRESH commands handled
21. Lambdas used for runnables

## Logging
22. Conservative use of log levels (mainly `debug`, unless bugs or misconfiguration)
23. Don't log if a Thing goes offline — pass text to `updateStatus()` instead (framework logs it)
24. Log stack traces only on severe errors (bug detection)

## Code Quality
25. `@NonNullByDefault` added to every class (exception: classes with DTO suffix or in `dto` package)
26. Non-static fields and variables use camelCase (no underscores or prefixes)
27. Primitive types preferred over boxed types (e.g. `int` vs. `Integer`)
28. Duplicate code refactored where possible
29. Result of `getConfigAs()` and `getConfiguration()` cached
30. All byte[]/String conversions specify Charset (including Stream→Reader/Writer conversions)
31. Sockets and I/O streams used in try-with-resources where possible

## Error & Thread Handling
32. Checked exceptions used: custom exceptions extend `Exception`
33. `RuntimeException` not thrown on expected errors
34. `Exception` not caught unless an external method throws it — catch `RuntimeException` for unexpected errors
35. Any `IOException` catch also handles `InterruptedIOException`
36. On `InterruptedException` or `InterruptedIOException`: return from method ASAP (unless in binding-managed thread)
37. Created threads declared as daemon: `Thread.setDaemon(true)`
38. Created threads named via `Thread.setName()` or constructor
39. `synchronized` on Handler methods reviewed carefully (risk of deadlock with parent class)
40. Cancelling a `Future`: no need to check if already cancelled

## Static Analysis
41. Compiler warnings annotated with `@SuppressWarnings` where unavoidable
42. Checkstyle: `target/code-analysis/report.html` checked
43. Formatting: `mvn spotless:check -Dspotless.check.skip=false`
44. JavaDoc: `mvn javadoc:javadoc`
