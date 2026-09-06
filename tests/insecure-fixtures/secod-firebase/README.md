# Executable implementation fixtures: secod-firebase

Run:

```text
python tests/insecure-fixtures/secod-firebase/run_fixtures.py
```

The fixture models broad Firestore reads, tenant-scoped Storage writes, content and size checks,
server-only Admin SDK use, and service-account credential boundaries. It is an in-memory contract
similar to an Emulator test; it does not contact Firebase or inspect deployed Rules/App Check.
