<!-- SECOD template for mobile, React Native/Expo, Flutter, and device/backend boundaries. -->

---
name: <secod-mobile-skill>
description: >-
  Help AI coding agents implement secure <mobile capability> across device,
  application, operating-system, and backend boundaries. Use when <mobile triggers>.
license: Apache-2.0
compatibility: "Requires <native|React Native/Expo|Flutter> project; recipes state supported versions and platforms."
metadata:
  secod-category: "mobile"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# Secure <mobile capability> implementation

## Purpose

Help agents build mobile features with safe device storage, backend enforcement, transport, deep-link, permission, and platform behavior. Treat the installed application and device as untrusted relative to privileged backend operations.

## When to use

Use for:

- native iOS or Android code;
- React Native/Expo or Flutter features;
- device credentials, biometrics, push notifications, deep links, local files, or mobile networking;
- mobile use of provider SDKs.

Do not activate solely because a responsive website is viewed on a phone.

## Context to inspect

- Mobile framework, platform targets, minimum OS versions, and build profiles.
- Device, app sandbox, operating system, backend, and third-party trust boundaries.
- Authentication/session lifecycle and token storage.
- Local persistence, backups, screenshots, clipboard, logs, and notifications.
- Deep links, universal/app links, intents, WebViews, and external navigation.
- Permissions and sensitive platform APIs.
- Backend APIs and provider SDKs used by the mobile feature.

## Mobile security invariants

- No privileged server credential or irreversible authorization decision lives in the app bundle.
- Sensitive tokens use platform-protected storage appropriate to their lifetime and threat model.
- Backend authorization does not trust device-side roles, flags, prices, tenant IDs, or completion state.
- External URLs, deep links, intents, and WebView bridges are allowlisted and validated.
- Permissions are minimal, purpose-bound, and requested near use.
- Sensitive information does not leak through logs, notifications, screenshots, clipboard, backups, or crash reports.

## Secure defaults

- Keep privileged effects behind authenticated, authorized backend APIs.
- Prefer short-lived tokens with revocation/rotation behavior over durable bearer secrets.
- Store only data needed offline and define its expiry, deletion, and backup behavior.
- Use platform trust stores and supported TLS behavior; avoid custom certificate validation unless a reviewed requirement exists.
- Validate all backend responses and untrusted local/external inputs before use.
- Use platform-native link verification and constrain WebView capabilities.

## Implementation workflow

1. Map device-to-backend and app-to-OS data flows.
2. Classify local data and credentials by sensitivity and lifetime.
3. Select the platform/framework recipe matching supported versions.
4. Implement device controls and backend authorization together.
5. Add unit, platform, integration, and backend abuse tests.
6. Verify build-time secret handling and release configuration.
7. Provide exact store/platform/provider setup steps still required.

## Implementation recipes

- [`references/<platform>-secure-storage.md`](references/<platform>-secure-storage.md) — <versions and credential type>.
- [`references/<framework>-deep-links.md`](references/<framework>-deep-links.md) — <link model and platforms>.
- [`references/<framework>-backend-session.md`](references/<framework>-backend-session.md) — <auth/session model>.

Recipes must separate device-side risk reduction from server-side security enforcement.

## Unsafe patterns to avoid

- Embedding server API keys or provider administration credentials in the app.
- Treating obfuscation, hidden UI, or local flags as authorization.
- Storing session tokens in generic unencrypted preferences.
- Accepting arbitrary deep-link destinations or WebView messages.
- Placing secrets in build-time “public” environment variables.
- Logging tokens, precise location, personal data, or sensitive notification content.

## Tests to add

- Backend rejects tampered identity, role, tenant, price, and ownership claims.
- Session expiry, refresh, revocation, logout, reinstall, and device-change behavior.
- Deep-link and external-navigation allowlist bypass attempts.
- Locked-device and background-state handling for sensitive data.
- Permission denial and partial-grant behavior.
- Offline queue duplicate/replay and synchronization conflict behavior.
- Release build contains no privileged credential or development endpoint.

## Provider and deployment steps

Include entitlements, associated domains, intent filters, backup policy, transport policy, notification settings, signing/build profiles, and provider console settings only when the feature needs them. State what was and was not verified.

## Official sources

Use [`references/sources.md`](references/sources.md). Prefer Apple, Android, React Native, Expo, Flutter, and selected provider documentation. Include official documentation homepages, official `llms.txt` endpoints when published, and direct platform pages supporting each recipe.

## Completion handoff

State device and backend protections implemented, platforms/versions covered, tests run, release configuration required, and any narrow unverified external setting.
