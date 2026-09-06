# Expo release and test recipe

## Build and update separation

- Give development, preview, and production profiles distinct application identifiers/endpoints where isolation is required.
- Keep private EAS/build credentials outside committed source and never expose them through `EXPO_PUBLIC_` variables.
- Ensure production profile excludes debug menus, test endpoints, cleartext transport exceptions, and verbose sensitive logging.
- Treat over-the-air updates as production code delivery: constrain channels/runtime compatibility and test rollback/recovery.
- Verify config-plugin output in generated native projects when security behavior depends on manifests, entitlements, or permissions.

## Tests

- Unit: URL parser allowlist, session expiry/deletion, redaction, permission state branching, notification action validation.
- Integration: backend rejects missing/expired session, wrong tenant, forged device identifiers, and unauthorized object IDs.
- Device/development build: cold/warm links, denied/revoked permissions, notification tap, secure storage across lock/reinstall/upgrade as supported.
- Release: inspect production artifact/config, run production-mode app, and confirm environment/update-channel separation.

Expo Go cannot prove custom native configuration or every production permission/notification path.
State which behavior ran in Expo Go, development build, simulator/emulator, physical device, or
release artifact.
