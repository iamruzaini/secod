# Flutter release and tests

## Release safeguards

- Separate development/staging/production flavors, identifiers, endpoints, provider projects, and signing.
- Keep `key.properties`, keystores, certificates, passwords, and store credentials outside repository.
- Ensure release manifests/plists contain no broad cleartext exceptions, debug capabilities, test endpoints, or unnecessary permissions.
- Build signed Android App Bundle and iOS archive through official workflows.
- If using `--obfuscate --split-debug-info`, protect symbol files and retain them for crash decoding. Obfuscation does not encrypt resources or protect secrets.

## Tests

- `flutter test`: parsers, storage abstraction, redaction, permission states, notification actions, account switching.
- Integration/device: cold/warm links, secure storage lifecycle, denied/revoked permissions, notification taps, offline expiry.
- Backend: expired/missing token, wrong tenant/object, forged device identifier, replayed request.
- Release: run release/profile artifact, inspect flavor/endpoints and platform manifests, verify signing and HTTPS policy.

Record exact command, target, mode, and result. Simulator/widget tests do not prove native keychain,
keystore, association, notification, or signing behavior.
