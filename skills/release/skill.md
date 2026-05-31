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

   Generates all `.properties` files under `src/main/resources/OH-INF/i18n/`.
   Never edit these files manually — this command is the only source of truth.

1. **Full build:**

   ```shell
   mvn clean install
   ```

   Compiles, runs tests, and packages the binding. A `BUILD SUCCESS` here means the binding is release-ready.

## Output

After all three steps succeed, report:

- ✅ `spotless:apply` — code formatted
- ✅ `i18n:generate-default-translations` — translation files generated
- ✅ `clean install` — build successful

If any step fails, report the failing command, paste the relevant error lines, and stop.
Do not proceed to the next step after a failure.

## When to Use

Use `$Release` before every commit that will be pushed for review,
or any time you want to verify the binding is in a clean, buildable state.
