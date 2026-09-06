---
name: secod-mobile-app-security
description: >-
  Help coding agents implement portable mobile security boundaries for device storage, deep links,
  permissions, notifications, offline data, release builds, and backend/provider access. Use for
  native, React Native, Expo, or Flutter mobile features; pair with the exact framework adapter.
license: Apache-2.0
compatibility: "Requires a mobile application; inspect platform targets, framework, lockfiles, and release configuration before choosing APIs."
metadata:
  secod-category: "mobile"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure mobile application implementation

## Purpose

Keep mobile clients outside the trusted computing boundary while implementing secure device
storage, verified links, minimal permissions, safe notifications, bounded local persistence, and
release configuration.

## When to use

Use for Android/iOS application features, mobile sessions, local or offline data, deep links,
permissions, push notifications, WebViews, native provider SDKs, or mobile release changes. Do not
activate for backend-only work with no mobile client behavior.

## Context to inspect

Resolve framework and version, Android/iOS targets, application identifiers, release variants,
session design, local data classes, link domains, permissions, notification payloads, backend APIs,
provider SDKs, logging/crash reporting, backup behavior, and nearby tests.

## Secure defaults

- Treat application binary, device state, local storage, link payloads, and notification data as attacker-readable or attacker-controlled.
- Keep provider secrets and authorization decisions on trusted backend or provider policy boundaries.
- Store only small necessary credentials in platform-backed secure storage; keep ordinary caches free of secrets and sensitive logs.
- Prefer verified HTTPS App Links and Universal Links; parse allowlisted routes and reauthorize every protected destination.
- Request the smallest permission at point of use and support denial, revocation, and restricted states.
- Put identifiers, not sensitive content or bearer tokens, in notifications and deep links.
- Keep debug trust exceptions, test endpoints, diagnostics, and signing material out of release builds.

## Implementation workflow

1. Map device, app process, OS services, backend, provider SDK, and persistent-data boundaries.
2. Classify each local value and choose memory, ordinary app storage, or platform-backed secure storage.
3. Implement verified-link parsing and backend authorization after navigation.
4. Minimize permissions and notification data; handle denied and revoked access.
5. Route privileged provider operations through backend adapters unless official mobile SDK design explicitly permits client use.
6. Harden release configuration and add device/simulator plus backend negative tests.

## Implementation recipes

- [`references/mobile-boundaries-storage.md`](references/mobile-boundaries-storage.md) — device trust, sessions, storage, offline data, WebViews, and provider SDK boundaries.
- [`references/links-permissions-notifications-release.md`](references/links-permissions-notifications-release.md) — verified links, permissions, notifications, and release safeguards.

## Unsafe patterns to avoid

- Embedding private API keys, service-account credentials, signing secrets, or unrestricted provider credentials in application bundles.
- Storing access or refresh tokens in unencrypted preferences, databases, Redux snapshots, logs, or crash reports.
- Trusting route parameters, device claims, hidden screens, biometric success, or notification payloads as backend authorization.
- Requesting broad permissions at startup or retaining sensitive offline data without expiry and logout deletion.
- Shipping cleartext-network exceptions, debug menus, verbose logs, or development signing configuration.

## Tests to add

Test clean install, upgrade, logout, account switch, token expiry, storage failure, denied/revoked
permissions, malformed and hostile links, protected-route reauthorization, forged notifications,
offline data expiry, screenshot/clipboard handling where required, and release configuration on real
Android and iOS builds when available.

## Provider and deployment steps

Select `secod-react-native-expo` or `secod-flutter` for framework APIs and exact provider adapters
for SDK behavior. Record link-association files, notification credentials, entitlements, permission
descriptions, signing, backup/data-safety declarations, and store configuration that remain external.

## Official sources

Use [`references/sources.md`](references/sources.md). Framework `llms.txt` files aid discovery;
direct Android, Apple, and framework pages support implementation decisions.

## Completion handoff

State mobile targets, framework/version, device/backend boundary, storage and link choices,
permissions, notification data, release tests, provider adapters, and exact external actions. Never
claim device or store configuration was inspected without access or certify application security.
