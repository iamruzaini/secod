# Trigger case: secod-firebase

## Should trigger

```text
Add Firebase Auth, tenant Firestore documents, Storage uploads, and App Check to this app.
```

Expected: separate client/Admin SDK authority, write Firestore and Storage Rules, add Emulator Suite
tests, integrate App Check with staged enforcement, and protect service-account credentials.

## Should not trigger

```text
Add authentication using Supabase; Firebase is not installed or referenced.
```

Expected: Firebase excluded.
