# Flutter mobile patterns

## Storage and backend

- Use `shared_preferences` only for non-sensitive preferences. Its persistence is not secure credential storage.
- For persistent credentials, select a maintained package that uses Android Keystore and Apple Keychain, inspect locked version and native options, and test unavailable/corrupt storage plus logout deletion.
- Keep secrets off-device. Values in Dart source, assets, generated config, and `--dart-define` can be recovered from application artifacts.
- Authenticate and authorize every backend request from server-owned identity and object/tenant policy. Router guards and widget visibility are UX only.

## Links, permissions, and notifications

- Configure verified HTTPS app/universal links for owned domains and allowlist parsed destinations.
- Never include credentials or sensitive records in link parameters; reauthorize protected routes.
- Declare/request minimum permission and model denied, permanently denied, restricted, and revoked states using APIs supported by locked plugin/platform versions.
- Put minimal content in push payloads and authorize every resulting fetch or mutation.

## Plugins and platform channels

- Treat MethodChannel/EventChannel input from either side as untrusted: validate method, schema, size, and lifecycle state.
- Review plugin ownership, maintenance, native permissions, data collection, and transitive native dependencies before adoption.
- Resolve exact provider plugin version and route to provider adapter. Public mobile configuration still requires provider policy and API restrictions; server/Admin credentials never belong in Flutter app.
