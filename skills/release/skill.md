# Role: $Release (Release Preparer)

**Focus:** Prepare the binding for a clean, passing build before committing or opening a PR.

## What This Command Does

Run the following three Maven commands **in sequence** from the binding's root directory.
Stop immediately if any step fails and report the error.

1. **Format code:**

   ```shell
   mvn spotless:apply
   ```

   Applies all code formatting rules (Spotless). Must complete without errors before proceeding.

1. **Generate i18n translations:**

   ```shell
   mvn i18n:generate-default-translations
   ```

   Generates or updates the default `.properties` file under `src/main/resources/OH-INF/i18n/`. This Maven goal preserves custom keys such as hand-written status description texts (`@text/<key>`) and discovery result labels, as long as it runs in its default mode (never pass `-Di18n.generation.mode=REGENERATE_FILES`, which deletes the file first). Never edit locale files (`<binding>_xx.properties`) by hand.

1. **Full build:**

   ```shell
   mvn clean install
   ```

   Compiles, runs tests, and packages the binding. A `BUILD SUCCESS` here means the binding is release-ready.

## Output

After all three steps succeed, report:

- ✅ `spotless:apply` — code formatted
- ✅ `i18n:generate-default-translations` — default translation file generated
- ✅ `clean install` — build successful

If any step fails, report the failing command, paste the relevant error lines, and stop.
Do not proceed to the next step after a failure.

## When to Use

Use `$Release` before every commit that will be pushed for review,
or any time you want to verify the binding is in a clean, buildable state.
