# Flutter version boundary

1. Read Flutter/Dart SDK constraints from `pubspec.yaml` and actual tool version when available.
2. Resolve plugin versions from `pubspec.lock`; inspect imported APIs and platform target requirements.
3. Use direct Flutter documentation matching stable SDK behavior and official package docs matching locked plugin version.
4. Check Android Gradle/Kotlin and iOS deployment/plugin requirements before changing native files.
5. Ask one narrow question only when unresolved version or plugin choice changes security design.

Flutter documentation reviewed on 2026-09-06 states pages generally reflect Flutter 3.47.2. Treat
that as documentation context, not proof project uses that version. `llms.txt` is discovery only.
