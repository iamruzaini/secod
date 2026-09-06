---
name: secod-flutter
description: >-
  Help coding agents implement secure Flutter mobile features with version-supported Dart/plugin
  APIs, protected device storage, verified deep links, minimal permissions, safe notifications,
  backend trust boundaries, and hardened Android/iOS release builds.
license: Apache-2.0
compatibility: "Requires a Flutter project; resolve Flutter/Dart SDK constraints, lockfile packages, platform targets, and flavors before choosing APIs."
metadata:
  secod-category: "mobile"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure Flutter implementation

## Purpose

Translate portable mobile invariants into version-correct Flutter/Dart, plugin, Android, and iOS
implementation while keeping client code, local state, and navigation outside backend trust.

## When to use

Use for Flutter mobile code, Dart packages/plugins, local persistence, deep links, permissions,
notifications, platform channels, provider SDKs, flavors, or Android/iOS release builds. Do not
activate for unrelated Dart server or Flutter web-only work unless mobile targets are in scope.

## Context to inspect

Inspect Flutter/Dart versions, `pubspec.yaml`, `pubspec.lock`, Android/iOS deployment targets,
flavors, manifests/entitlements, router, storage plugins, links, permissions, notifications,
platform channels, provider SDKs, build signing, obfuscation, logs, and tests.

## Secure defaults

- Treat compiled Dart, assets, defines, device storage, route state, and platform-channel input as untrusted/client-visible.
- Keep secrets and authorization on backend; use platform-backed secure storage through a maintained compatible plugin only when persistence is necessary.
- Keep `shared_preferences`, files, and SQLite free of credentials unless application encryption and key lifecycle are explicitly designed.
- Prefer verified Android App Links and iOS Universal Links; validate routes and reauthorize protected effects.
- Minimize permissions and notification payloads; handle denial/revocation and fetch sensitive content after authentication.
- Build signed release artifacts with production transport/config; treat obfuscation only as reverse-engineering friction, never secret protection.

## Implementation workflow

1. Resolve Flutter/Dart and locked plugin versions plus Android/iOS targets.
2. Map widget/router, Dart service, platform channel/plugin, OS storage, backend, and provider boundaries.
3. Choose storage and link design; implement server authorization independent of client navigation.
4. Add minimal permission and notification flows with explicit denied/error states.
5. Configure flavors and release signing without committing keys; test production-mode behavior.

## Implementation recipes

- [`references/flutter-mobile-patterns.md`](references/flutter-mobile-patterns.md) — storage, backend, provider SDK, links, permissions, notifications, and platform channels.
- [`references/release-and-tests.md`](references/release-and-tests.md) — release configuration, obfuscation boundary, and tests.
- [`references/versions.md`](references/versions.md) — Flutter/Dart/plugin version resolution.

## Unsafe patterns to avoid

- Embedding secrets in Dart source, assets, `--dart-define`, generated config, or obfuscated binaries.
- Storing tokens in `shared_preferences` or unencrypted SQLite/files.
- Trusting router guards, biometric success, plugin output, device IDs, or platform-channel messages as backend authorization.
- Using custom schemes for sensitive data or broad permissions when verified/scoped alternatives exist.
- Shipping debug signing, cleartext transport exceptions, DevTools endpoints, verbose logs, or test backends.

## Tests to add

Add Dart unit/widget tests for parsing and state decisions, integration tests for storage/session and
links, backend tests for authorization, platform tests for permissions/notifications, and signed
release-mode checks on Android/iOS. Include wrong account/tenant, hostile links, denied permissions,
forged notifications, storage corruption, logout, upgrade, and offline expiry.

## Provider and deployment steps

Select exact Firebase, Google, AWS, Supabase, auth, payment, AI, messaging, or storage adapter.
Record provider mobile configuration restrictions, Android/iOS association files, APNs/FCM
credentials, entitlements, permission descriptions, signing, flavors, and store actions remaining.

## Official sources

Use [`references/sources.md`](references/sources.md). Flutter `llms.txt` aids discovery; direct
Flutter and native-platform pages support decisions. Package APIs require their official package
documentation and locked version.

## Completion handoff

State Flutter/Dart/plugin versions, targets/flavors, storage and link decisions, permissions,
notifications, provider boundary, release artifact tests, and external actions. Never imply
obfuscation hides secrets, invent plugin APIs, or certify application security.
