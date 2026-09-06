# Trigger case: secod-flutter

## Should trigger

```text
Add Flutter mobile session storage, app links, notification actions, and signed Android/iOS release flavors.
```

Expected: resolve Flutter/Dart/plugin versions, select mobile baseline, keep authorization on backend,
use platform-backed storage, verify links, minimize permissions, and test signed release behavior.

## Should not trigger

```text
Change a Dart command-line utility that has no Flutter or mobile platform target.
```

Expected: Flutter mobile skill excluded.
