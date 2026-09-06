# Links, permissions, notifications, and release builds

## Deep links

- Prefer Android App Links and iOS Universal Links with owned HTTPS domains and association files.
- Allowlist scheme, host, path, and accepted parameters. Reject ambiguous encodings, unexpected redirects, and unsupported actions.
- Never place access tokens, passwords, personal data, or privileged commands in URLs.
- Treat every inbound link as navigation intent only. Reauthenticate or reauthorize protected actions against backend state.
- Test installed/not-installed behavior, cold/warm launch, logged-out state, wrong tenant, expired links, and hostile query values.

## Permissions

- Declare only capabilities current feature needs and request dangerous permissions at point of use.
- Explain purpose in user-facing context before OS prompt when useful.
- Handle denied, permanently denied, restricted, revoked, and partial-access states without bypassing policy.
- Prefer privacy-preserving system pickers and scoped access over broad photo, contact, location, or storage permissions.

## Notifications

- Ask permission in context; do not assume authorization remains granted.
- Put opaque identifiers and minimal display text in payloads. Fetch sensitive content after authentication.
- Validate notification action and object authorization before navigation or mutation.
- Bind push tokens to current account/device installation, rotate them, and remove stale/logout mappings.
- Keep APNs/FCM server credentials on backend or provider service, never in app.

## Release build

- Separate debug, preview, and production identifiers/endpoints.
- Ensure release build has no cleartext exceptions, debug tools, test credentials, verbose logs, or developer menus.
- Protect signing material outside repository and use official store signing/credential workflows.
- Test production-mode artifact, link associations, permissions, notification routing, backup/restore, logout, and account switching.
