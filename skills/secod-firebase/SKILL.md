---
name: secod-firebase
description: >-
  Help coding agents implement Firebase Auth, Firestore, Storage, Functions, Security
  Rules, Admin SDK, and App Check securely. Use when Firebase products, SDKs,
  firebase.json, rules files, or emulator tooling are part of current feature.
license: Apache-2.0
compatibility: "Requires Firebase; recipes target modular Web SDK, Admin SDK, Rules, and Emulator Suite."
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure Firebase implementation

## Purpose

Build Firebase features with explicit client/Admin boundaries, server authorization, deny-by-default
Rules, emulator tests, protected credentials, and product-specific App Check rollout.

## When to use

Use for Firebase Auth, Firestore, Realtime Database, Storage, Functions, Admin SDK, Rules, Emulator
Suite, or App Check. Do not select for unrelated Google Cloud services without Firebase use.

## Context to inspect

Resolve products, Web/Admin SDK versions, app/project/environment, client versus trusted runtime,
Auth/tenant model, Firestore collections, Storage paths, Rules files, Functions, emulator scripts,
credential source, and App Check-supported services.

## Secure defaults

- Client SDK uses public Firebase configuration and is constrained by tested Security Rules.
- Admin SDK exists only in trusted server/Function runtime with workload identity where available.
- Every Admin operation repeats application-level user, tenant, and resource authorization.
- Firestore/Storage Rules deny by default and constrain identity, ownership, tenant, fields, paths,
  queries, file type, and size as relevant.
- Rules tests include unauthenticated and cross-tenant denials.
- App Check is added for supported products using monitor-then-enforce rollout; never treat it as authorization.

## Implementation workflow

1. Separate client and privileged Firebase operations.
2. Model user, tenant, resource, collection, object path, and trusted backend boundaries.
3. Implement Rules and backend authorization with feature code.
4. Add Emulator Suite tests using `@firebase/rules-unit-testing`.
5. Add App Check only for supported products and document exact external enforcement step.

## Implementation recipes

- [Auth and sessions](references/auth-sessions.md) — trusted identity and session boundaries.
- [Firestore Rules](references/firestore-rules.md) — tenant-safe document access and field constraints.
- [Storage Rules](references/storage-rules.md) — owner/tenant paths, type limits, and size limits.
- [Admin SDK boundary](references/admin-sdk-boundary.md) — privileged server initialization and authorization.
- [Emulator tests](references/emulator-tests.md) — allowed and denied Rules tests.

## Unsafe patterns to avoid

- Shipping service-account credentials or Admin SDK to browser/mobile code.
- Using Admin SDK as shortcut around missing Rules or authorization.
- Broad `allow read, write: if request.auth != null` for tenant data.
- Testing only allowed Rules paths.
- Enabling App Check blindly without metrics, supported-client readiness, and recovery plan.

## Tests to add

Test owner/member success; unauthenticated and cross-tenant denial; forbidden fields/paths; invalid
queries; oversized/wrong-type uploads; Admin endpoint authorization; emulator rule loading; and App
Check-aware backend behavior where applicable.

## Provider and deployment steps

Name exact Firebase app/product, Rules deployment, service identity, App Check provider, metrics,
enforcement target, and verification command/console path. If inaccessible, state only uninspected setting.

## Official sources

Use [`references/sources.md`](references/sources.md). Firebase `docs/llms.txt` is a discovery index;
direct product pages support implementation.

## Completion handoff

State client/Admin split, Rules and backend checks, emulator tests run, credentials used by category
only, and exact Firebase deployment/App Check action remaining. No findings report or certification.
