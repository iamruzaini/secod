---
name: secod-react-native-expo
description: >-
  Help coding agents implement secure React Native and Expo features using version-supported APIs
  for SecureStore, linking, permissions, notifications, local persistence, native modules, and
  release builds. Use only when React Native or Expo is requested or detected.
license: Apache-2.0
compatibility: "Requires React Native or Expo; resolve react-native, expo SDK, router, native targets, and workflow from lockfiles and configuration."
metadata:
  secod-category: "mobile"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure React Native and Expo implementation

## Purpose

Translate portable mobile invariants into version-correct React Native and Expo code without
treating JavaScript bundle state, `EXPO_PUBLIC_` variables, navigation guards, or device storage as
a trusted backend boundary.

## When to use

Use for React Native, Expo, Expo Router, EAS Build/Update, Expo modules, native linking,
permissions, SecureStore, notifications, or mobile provider SDK integration. Do not activate for
React web applications without React Native or Expo.

## Context to inspect

Inspect `package.json` and lockfile, `app.json`/`app.config.*`, `eas.json`, Expo SDK and React Native
versions, router, config plugins, Android/iOS identifiers, session storage, links, permissions,
notifications, native modules, environment variables, build profiles, updates, and tests.

## Secure defaults

- Treat all bundled JavaScript and `EXPO_PUBLIC_` values as public; keep private provider credentials server-side.
- Use `expo-secure-store` only for small necessary native credentials and define logout/account-switch deletion.
- Prefer Expo Router verified Android App Links/iOS Universal Links; validate inbound URLs and reauthorize protected effects.
- Configure minimum permissions through app config/config plugins and request them at point of use.
- Keep notification payloads minimal and authorize notification-driven navigation/actions.
- Separate development, preview, and production identifiers, endpoints, credentials, and update channels.

## Implementation workflow

1. Resolve installed Expo SDK/React Native/router versions and whether native directories use CNG or direct maintenance.
2. Map component, native OS, Expo module, backend API, provider SDK, and EAS boundaries.
3. Implement storage/session and link handling with documented APIs supported by resolved versions.
4. Configure permissions and notifications narrowly; add denial, hostile-link, and forged-payload tests.
5. Verify development and production build/update configuration without exposing secrets to bundle.

## Implementation recipes

- [`references/expo-mobile-patterns.md`](references/expo-mobile-patterns.md) — SecureStore, sessions, local persistence, provider SDKs, links, permissions, and notifications.
- [`references/release-and-tests.md`](references/release-and-tests.md) — EAS/release boundaries and positive/negative tests.
- [`references/versions.md`](references/versions.md) — version resolution and API support boundary.

## Unsafe patterns to avoid

- Placing secrets in `EXPO_PUBLIC_`, app config `extra`, source, update bundles, or client-only provider SDK calls.
- Persisting tokens in AsyncStorage or a persisted state tree.
- Treating Expo Router protected routes as backend authorization.
- Sending tokens or sensitive records through links or notifications.
- Adding broad native permissions or cleartext transport solely to make development code work in release.

## Tests to add

Test native and web storage separation, logout/account switch, locked/unavailable SecureStore,
malformed links, unauthorized destinations, denied/revoked permissions, notification payload
tampering, build-profile separation, and production-mode artifacts. Use real development builds for
native behavior unavailable in Expo Go.

## Provider and deployment steps

Use exact provider adapter for Firebase, Supabase, Cognito, Clerk, AI, payments, storage, or
messaging SDK. Name required EAS environment, credentials, link association, push credentials,
entitlements, store declarations, and verification commands without claiming remote state.

## Official sources

Use [`references/sources.md`](references/sources.md). Start with Expo and React Native `llms.txt` for
discovery, then use direct versioned implementation pages.

## Completion handoff

State Expo/React Native/router versions, native targets, storage and session design, links,
permissions, notification behavior, release/update profiles, tests executed, provider adapter, and
external actions. Never invent Expo modules/config keys or certify application security.
