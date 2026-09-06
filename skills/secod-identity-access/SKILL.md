---
name: secod-identity-access
description: >-
  Help coding agents implement authentication, sessions, server-side authorization,
  ownership, roles, and tenant isolation. Use when building login, account, admin,
  API-key, invitation, recovery, OAuth, or protected-resource features.
license: Apache-2.0
metadata:
  secod-category: "generalized"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure identity and access implementation

## Purpose

Implement identity and authorization at trusted boundaries. Provider adapters supply exact SDK
calls; this skill owns portable session, resource, role, ownership, and tenant invariants.

## When to use

Use for authentication, protected reads/mutations, roles, tenants, admin actions, invitations,
recovery, MFA/passkeys, OAuth callbacks, API keys, capability links, and account lifecycle.
Do not activate for public data with no identity-dependent behavior.

## Context to inspect

Identify identity provider, session/token type, trusted backend boundary, user and tenant keys,
roles, resource ownership, privilege changes, expiry/revocation path, and nearby authorization tests.

## Secure defaults

- Authenticate and authorize every protected server operation.
- Derive user, tenant, role, price, and ownership from trusted state; never accept authority from UI.
- Deny when identity or policy context is absent.
- Rotate sessions after authentication or privilege change; use secure cookie/token storage.
- Scope API keys and capability links narrowly with expiry and revocation.
- Return minimal account data and avoid identity secrets in logs.

## Implementation workflow

1. Map caller, credential, protected resource, tenant, and privileged effect.
2. Use provider adapter to validate credential/session at backend.
3. Load authoritative membership/ownership and enforce action-specific policy near data/effect.
4. Constrain writable fields; handle expiry, revocation, logout, and account recovery.
5. Add authorized, unauthenticated, unauthorized, cross-tenant, and privilege-change tests.

## Implementation recipes

- [`references/server-authorization.md`](references/server-authorization.md) — resource and tenant
  authorization pattern for server handlers and services.

## Unsafe patterns to avoid

- UI visibility, middleware, or route guards as sole authorization.
- Trusting client-supplied user IDs, tenant IDs, roles, or ownership.
- Decoding tokens without validating signature, issuer, audience, purpose, and time claims.
- Mass-assigning account or role fields from request bodies.

## Tests to add

Test allowed owner/member behavior; missing login; wrong role; wrong tenant; resource enumeration;
session expiry/revocation; privilege changes; forbidden fields; and redacted errors/logs.

## Provider and deployment steps

Provider adapters own callback URLs, issuers, audiences, cookie domains, MFA, and key rotation.
Name exact inaccessible setting and verification step without claiming it was inspected.

## Official sources

Use [`references/sources.md`](references/sources.md), then exact provider documentation selected by
`secod-core`.

## Completion handoff

State enforcement boundary, identity and tenant source, protected actions, tests run, and exact
provider action remaining. Never claim whole application is secure.
