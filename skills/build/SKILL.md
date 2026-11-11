---
name: build
description: Build and test the binding from the user's connected Windows folder in the cloud container (Java 21, Maven), including Spotless and static analysis.
---

# Binding in der Cloud-Umgebung bauen

Geprüft am Binding `org.openhab.binding.e3dc` (openHAB 5.3.0-SNAPSHOT). Das Rezept gilt für jedes Binding unter `bundles/`.

## Wichtig vorab

- Gebaut wird mit dem **Bash-Tool in der Cloud-Umgebung**, nicht mit `device_bash`. Die Geräte-VM hat kein Maven und nur Java 11.
- Java 21 und Maven 3.9.x sind in der Cloud-Umgebung vorinstalliert (`/opt/maven`). Nichts installieren, mit `java -version` und `mvn -v` prüfen.
- Jede Sitzung startet frisch: `~/.m2` ist leer, der erste Build lädt alle Abhängigkeiten (einige Minuten).
- Der Klon von `openhab-addons` ist ein Wegwerf-Klon. Nie committen oder pushen. Die echten Änderungen liegen im Ordner des Nutzers.

## Schritte

1. **Maven-Repositories** in `~/.m2/settings.xml` eintragen (Profil `openhab`, aktiv), damit das Parent-POM `org.openhab.addons.reactor.bundles:<version>-SNAPSHOT` aufgelöst wird: Release `https://openhab.jfrog.io/artifactory/libs-release` und Snapshot `https://openhab.jfrog.io/artifactory/libs-snapshot`, jeweils für Repositories und Plugin-Repositories.
2. **Repo-Rahmen holen** (der Build erwartet die Struktur von `openhab-addons`): `git clone --depth 1 --filter=blob:none --sparse https://github.com/openhab/openhab-addons.git addons`, dann `git sparse-checkout set --no-cone /.github /tools /.mvn /pom.xml /bundles/pom.xml`. Ohne `.mvn` im Wurzelverzeichnis zeigt der Markdownlint-Pfad ins Modul und der Build bricht ab.
3. **Quellen des Nutzers holen**: auf dem Gerät im Binding-Ordner ein Archiv in einen vorhandenen Unterordner (zum Beispiel `tmp/`) packen, ohne `target`, `tmp` und `tools`. Per `device_stage_files` in die Cloud-Umgebung holen und nach `addons/bundles/<binding>/` entpacken.
4. **Dateien, die Tests lesen**, einzeln nachholen. Vorher mit `grep -rn "Path.of" src/test` prüfen, welche Pfade Tests brauchen. Beim e3dc-Binding ist das nur `tools/rscp/rscp_tags.tsv`. Die Skripte in `tools/` nicht ausführen und nicht kopieren.
5. **Formatieren**: im Modulordner `mvn -B spotless:apply`.
6. **Bauen und testen**: `mvn -B clean install` im Modulordner. Ausgabe in eine Logdatei leiten und mit `grep -E "ERROR|Tests run:|BUILD"` auswerten. Dauer: erster Lauf einige Minuten, danach etwa eine Minute.
7. **Spotless-Änderungen zurückschreiben**: Original und gebaute Kopie mit `diff -rq --strip-trailing-cr` vergleichen. Geänderte Quelldateien nach `/mnt/user-data/outputs/` kopieren und mit `device_commit_files` an ihren Pfad im Nutzerordner schreiben, damit sein lokales `spotless:check` sauber bleibt. `src/main/history/dependencies.xml` wird vom Build erzeugt und nicht zurückgeschrieben.
8. **Fertiges JAR** liegt in `target/`. Nur auf Wunsch an den Nutzer schicken.

## Typische Fehler

- `markdownlint.yaml` nicht gefunden: `.mvn` fehlt im Repo-Wurzelverzeichnis (Schritt 2).
- Test mit `NoSuchFileException` unter `tools/`: die Datei fehlt in der Kopie (Schritt 4).
- Static-Analysis-Fehler `Invalid content was found starting with element ...` in Thing-XML: Reihenfolge der Elemente prüfen. In `bridge-type` und `thing-type` steht `<channel-groups>` vor `<config-description>`.
- Channel-Typ-Tests: neue Item-Typen wie `Number:Time` und `Number:DataAmount` in der erlaubten Liste ergänzen, `advanced="true"` am `channel-type` erlauben.

## Aufräumen

Temporäre Archive im Nutzerordner (zum Beispiel `tmp/claude-build-*.tgz`) dem Nutzer nennen. Löschen geht nur mit seiner Freigabe (`device_request_delete_permission`).
