---
name: secod-identity-access
description: Enforce authentication and authorization at the backend; validate every credential, authenticator, session, share link and token lifecycle; deny by default across user, tenant, owner and admin boundaries; prevent IDOR/BOLA, mass assignment, privilege escalation and account takeover. Triggers include any login/signup/recovery/MFA/OAuth route, session or JWT verification code, API-key issuance, share-link generation, role or tenant checks, and third-party auth SDK detection; package presence alone is Candidate.
---

# SECOD Identity Access Security

## Mission

Prove that every authentication decision, authorization decision, session lifecycle event,
credential validation, share link, and token check is enforced server-side with deny-by-default
semantics across user, tenant, owner, and admin boundaries.

Repository-only review cannot prove provider-side session policy, deployed revocation behavior,
dashboard security settings, active attack resistance, or that recovery channels behave securely
in production. `secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls: backend authentication enforcement and enumeration resistance; password policy
and KDF selection; MFA enrollment/use/recovery; passkeys/WebAuthn validation; password-reset and
account-recovery flows; session issuance/expiry/rotation/inventory/revocation including refresh
token rotation and reuse detection; JWT/token signature and claim validation; application-issued
API-key lifecycle; share-link/capability authorization; OAuth/OIDC redirect/state/nonce/PKCE
handling; account linking; default/shared account hygiene; BOLA/IDOR, function/property
authorization, mass assignment, tenant isolation, account-takeover and privilege-escalation
verification.

Excluded controls (owned elsewhere): provider-side tenant/project configuration and RLS
(`secod-supabase`, family routers); auth-provider dashboard settings and SDK-specific token
validation (`secod-auth-provider-integrations` plus Clerk/Auth0/WorkOS/Better Auth/Cognito/
Entra/Supabase Auth adapters); browser cookie flags/CSP/CORS (`secod-web-app-security`);
bearer tokens reaching client bundles (`secod-web-app-security`, `secod-secrets-config`);
rate-limit implementation details (`secod-abuse-limits`); KDF/crypto primitive selection depth
(`secod-crypto-data-protection`); audit-log plumbing (`secod-observability-response`);
launch verdicts (`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-auth-provider-integrations` and its provider adapters when a
supported third-party auth SDK/config/hosted domain/webhook is detected; `secod-supabase-auth`
with `secod-supabase`; `secod-web-app-security` for browser-side token exposure; hosting/cloud
adapters when platform IAM substitutes application identity.

## Required inputs

Repository: auth middleware/guards and their route coverage; login/signup/recovery/MFA handlers;
session creation/storage/invalidation code; JWT/JWKS verification code; API-key generation and
storage schema; share-link issuance/validation; OAuth callback/state handling; role/tenant
checks on data access; database schema for users/credentials/sessions/keys; test coverage of
negative cases.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
provider-side session lifetime/idle timeout/single-session settings; deployed JWKS rotation
state; actual MFA enrollment rates; recovery email/SMS deliverability behavior; dashboard
allowed-origins/redirect registrations; whether deployed instances run the reviewed code.

Human-supplied evidence: authorized provider dashboard exports, environment-separated session
policy values, incident/compromise response procedures.

## Applicability and discovery

Always applicable: any application with user accounts.

Signal groups:

- Package/SDK: `bcrypt`/`argon2`/`scrypt`, jose/jwt/jsonwebtoken libraries, WebAuthn/@simplewebauthn,
  OAuth client libraries, `@clerk/*`, `auth0`, `@workos-inc/*`, `better-auth`, `next-auth`,
  `@supabase/ssr`.
- Environment variables: names such as `JWT_SECRET`, `SESSION_SECRET`, `*_CLIENT_ID`,
  `WORKOS_API_KEY`, `BETTER_AUTH_SECRET` — names only, never values.
- Routes/webhooks: `/login`, `/signup`, `/logout`, `/callback`, `/refresh`, `/recovery`,
  `/mfa`, `/share/*`, invitation acceptance, webhook endpoints for provider events.
- Configuration: session store config, cookie settings in code, JWKS URLs, issuer/audience
  constants, password policy constants.
- Deployment/provider evidence: provider-hosted login domains, dashboard policy exports,
  deployment-correlated session behavior.

Classification follows `secod-core`: `Candidate` = package/variable name without corroborating
code; `Likely` = handler exists, deployed/provider state unverified; `Active` = repository
behavior correlates with deployed/runtime/dashboard evidence.

Maintain separate development/preview/staging/production inventories. Conflicting or shared
session-policy signals across environments keep affected controls `Not verified`.

## Review workflow

1. Inventory environments and trust boundaries: every authenticated route, every boundary where
   identity claims cross (browser→backend, provider→backend, service→service). Parallelizable
   once inventories exist.
2. Correlate active features: which credential types are live, which providers Active vs Likely,
   where sessions/tokens/API-keys/share-links are created and consumed. Parallelizable after
   step 1 completes there.
3. Verify applicable controls below against evidence.
4. Run safe negative tests: local reasoning/code-path tracing of tampered-token, expired-session,
   cross-tenant-access, replayed-verifier cases. No live attacks against real accounts.
5. Classify evidence, emit findings, route provider-specific gaps to adapters, hand off to
   `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-identity-N` and require catalog approval before promotion.

### `PROVISIONAL-identity-1` — Server-side deny-by-default authorization

**Applicability:** Every state-changing or sensitive read endpoint. Protects confidentiality,
integrity, and tenant isolation.

**Inspect and verify:** Every route handler resolves identity server-side from trusted context
(verified session/token), then authorizes the specific resource/action/tenant before data access;
default-deny when identity resolution fails; ownership filters applied at query level; function-
level and property-level (mass assignment) allowlists on writable fields; admin surfaces enforce
role server-side, never UI-only. Trace one read and one write path per resource end-to-end.

**Unsafe evidence:** Authorization derived from client-sent user ID/role/tenant claim without
server verification; hidden routes treated as access control; `is_admin` checked only in UI;
ORM updates accepting arbitrary fields.

**Required negative test:** Request object A's resource while authenticated as user B must be
denied at the server with no data leakage in error/response. Mass-assignment probe adding
`role`/`owner_id` fields to an update payload must be ignored or rejected.

**Passing / Not verified:** Pass requires traced enforcement for every inventoried sensitive
route. Any route whose guard cannot be located keeps it `Not verified` (`Fix before launch`
when the route touches private data).

**Related skill routing:** Provider-delegated identity → `secod-auth-provider-integrations` +
adapter; DB-level enforcement → `secod-supabase`, cloud data-service adapters.

### `PROVISIONAL-identity-2` — Password authentication quality

**Applicability:** Any password login/signup/change flow. Protects against credential guessing,
stuffing, and offline cracking.

**Inspect and verify:** KDF is Argon2id/bcrypt/scrypt with per-user salt and current-parameter
evidence; strength policy enforces length (minimum 8 with MFA, 15 without per NIST SP 800-63B
as codified in the OWASP Authentication Cheat Sheet), allows all characters and paste, blocks
common/breached passwords via blocklist checks, does not mandate periodic rotation, rotates on
compromise; login/reset responses resist account enumeration (uniform timing/messages);
throttling/lockout applied per account and per source; new-device/IP login notifications present.

**Unsafe evidence:** MD5/SHA-family password hashing; composition rules replacing length+
blocklist; "user exists" distinctions between login and reset responses; lockout absent.

**Required negative test:** Reset flow probed with existing vs nonexistent email must produce
indistinguishable responses; login with breached-list password must be rejected at signup.

**Passing / Not verified:** Pass requires KDF parameters verifiable from code/config plus
enumeration/throttle logic traced. Deployed rate-limit effectiveness stays with
`secod-abuse-limits`.

**Related skill routing:** `secod-crypto-data-protection` (KDF parameter depth),
`secod-abuse-limits` (throttling implementation), `secod-email-messaging` (recovery delivery).

### `PROVISIONAL-identity-3` — MFA and step-up re-authentication

**Applicability:** Any account with MFA capability or any high-risk action. Protects against
credential-only compromise.

**Inspect and verify:** Enrollment requires authenticated session; factor change/reset requires
recent authentication or explicitly justified high-assurance recovery; previous factor/session
notified on changes; recovery-code single-use with safe hashed storage; TOTP secrets stored
encrypted-at-rest; SMS/PSTN documented as phishing-prone and prohibited as sole high-value
factor without explicit acceptance; sensitive actions (email change, password change, key
creation, payout setup) require step-up re-authentication.

**Unsafe evidence:** MFA bypassable by re-running flow without second factor; recovery codes
stored plaintext; SMS as only factor on admin accounts; email change without re-authentication.

**Required negative test:** Attempting factor removal without recent-auth challenge must fail;
using a recovery code twice must fail the second use.

**Passing / Not verified:** Pass requires flow traces for enroll/change/recover plus step-up
coverage on sensitive actions. Provider-managed MFA settings unverifiable from repo stay
`Not verified`, routed to the auth adapter for dashboard evidence.

**Related skill routing:** `secod-auth-provider-integrations` + adapters; `secod-email-messaging`
(factor-change notification delivery).

### `PROVISIONAL-identity-4` — Passkeys/WebAuthn

**Applicability:** Any WebAuthn/passkey registration or authentication surface.

**Inspect and verify:** Challenges server-generated, high-entropy, single-use, short-lived;
origin and RP-ID validated on every ceremony against fixed expected values; user verification
required for high-risk actions; attestation policy deliberate (not blindly required nor blindly
accepted); public key, signature, sign-count/cloned-detector, transports validated per
WebAuthn L3 semantics using a maintained library/platform API; credential elimination and
account recovery do not weaken remaining credentials; synced-passkey implications documented;
hardware-backed key stores (TPM/Secure Enclave) noted where attestation asserts them.

**Unsafe evidence:** Client-generated challenges accepted; origin/RP-ID taken from request;
sign-count ignored everywhere; passkey reset achievable with email-only proof while passwords
require more.

**Required negative test:** Replayed challenge must fail; ceremony from wrong origin/RP-ID must
fail; registration response with altered publicKey must fail signature verification.

**Passing / Not verified:** Pass requires both ceremonies traced through library calls with
fixed origin/RP-ID constants. Authenticator-model trust properties stay assumptions unless
attestation evidence supplied.

**Related skill routing:** `secod-auth0`/`secod-clerk`/`secod-workos`/`secod-better-auth`/
`secod-supabase-auth`/`secod-aws-cognito` adapters when provider-managed.

### `PROVISIONAL-identity-5` — Recovery and password-reset flows

**Applicability:** Every reset/recovery path. Protects against account takeover via recovery.

**Inspect and verify:** Reset tokens high-entropy CSPRNG, single-use, short-lived (minutes),
hashed at rest; consumed before password change applies; all sessions invalidated on use;
enumeration-safe responses and timing; recovery channel binding verified (signed action links
with server-side token validation, not token-in-URL-only reliance); re-authentication required
to change recovery email/phone; notification to old contact on recovery-contact change.

**Unsafe evidence:** Long-lived or multi-use reset tokens; tokens stored unhashed; reset link
accepting the answer "which email exists" via response or timing distinctions; recovery email change without
re-authentication.

**Required negative test:** Used reset token replayed must fail; reset for unknown account must
be indistinguishable from known account.

**Passing / Not verified:** Pass requires token lifecycle traced generation→storage→consumption
plus invalidation evidence. Email/SMS delivery behavior stays `Not verified` without supplied
evidence (`secod-email-messaging` owns delivery).

**Related skill routing:** `secod-email-messaging`, `secod-crypto-data-protection` (token
storage), provider adapters for hosted recovery.

### `PROVISIONAL-identity-6` — Session lifecycle

**Applicability:** Every session/cookie-based authentication. Protects against fixation, theft,
and stale access.

**Inspect and verify:** Session IDs CSPRNG, ≥128 bits entropy, server-side strict validation
(never accept client-chosen values); fixation prevented by regeneration at every privilege
change including login; idle and absolute expiry both enforced server-side; logout destroys
server state, not only client cookie; user-visible device/session inventory with per-device and
all-session revocation; refresh-token rotation with reuse detection and family revocation where
refresh tokens exist; invalidation propagates after password reset, factor change, role change,
ownership change, compromise. Tokens never in URLs or web storage — HttpOnly Secure SameSite
cookies or BFF pattern per RFC 10017.

**Unsafe evidence:** JWT-as-session with no server-side revocation list for privileged users;
session ID accepted from query parameter; localStorage token storage; logout clearing cookie
only; refresh tokens non-rotating with no reuse detection.

**Required negative test:** Pre-login session ID reused post-login must be rejected (fixation);
revoked session ID must fail on next request including concurrent contexts; reused rotated
refresh token must revoke the whole family.

**Passing / Not verified:** Pass requires issuance/validation/expiry/revocation code traces plus
store schema showing hashed verifiers where applicable. Provider-side maximum-lifetime settings
stay `Not verified` until adapter supplies dashboard evidence.

**Related skill routing:** Cookie attributes → `secod-web-app-security`; provider session
policy → auth adapters; `secod-observability-response` (session revocation events).

### `PROVISIONAL-identity-7` — JWT and bearer-token validation

**Applicability:** Any JWT/JWS verification path (local sessions, service-to-service, provider
tokens).

**Inspect and verify:** Algorithm allowlist pinned (reject `none` and algorithm-confusion);
signature verified against fixed configured JWKS/discovery origin — never a token-supplied URL;
expected issuer, audience, expiry, not-before, subject, and required custom claims checked;
`kid` cache with bounded refresh on unknown key plus rotation handling; type confusion guarded
(ID token never accepted as API credential); clock-skew bounded; token class verified against
intended resource.

**Unsafe evidence:** `jwt.decode()` without verification anywhere in request path; JWKS URL from
token header/claim; audience check absent on multi-service deployment; `alg` taken from token.

**Required negative test:** Token signed with `alg: none` or wrong-key must reject; expired
token must reject; valid-audience-mismatch token must reject even with valid signature.

**Passing / Not verified:** Pass requires verification code trace against fixed trust anchors
with claim checks enumerated. Deployed rotation behavior needs runtime/provider evidence else
`Not verified`.

**Related skill routing:** Provider token classes → `secod-auth-provider-integrations` +
adapters; `secod-web-app-security` (token exposure in browser).

### `PROVISIONAL-identity-8` — API keys and share links

**Applicability:** Application-issued API keys, share links, capability URLs.

**Inspect and verify:** Keys generated with sufficient entropy, displayed once, stored as keyed
hash/HMAC with non-secret prefix identifier for lookup; bound to user/tenant/resources/scopes;
expiry where appropriate; rotation and immediate revocation supported; creation/use/revocation
audit events; per-key limits enforced. Share links: authorization scope explicit, expiry set,
rotation/revocation supported, verifier hashed at rest when server-validated; capability URLs
short-lived by design; no long-lived bearer verifier in any URL.

**Unsafe evidence:** Plaintext key lookup by equality; keys without tenant binding; share links
without expiry; capability token in URL surviving beyond designed lifetime.

**Required negative test:** Revoked key rejected on next call; expired share link rejected;
guessed/enumerated verifier fails (entropy check); cross-tenant key reuse denied.

**Passing / Not verified:** Pass requires generation/storage/validation/revocation traces.
Effectiveness of per-key limits → `secod-abuse-limits`.

**Related skill routing:** `secod-abuse-limits`, `secod-data-files` (share links over stored
objects), `secod-observability-response` (audit events).

### `PROVISIONAL-identity-9` — OAuth/OIDC and account linking

**Applicability:** Any OAuth/OIDC login, social login, or account-linking flow.

**Inspect and verify:** Authorization Code + PKCE for browser/public clients; exact redirect URI
allowlists (no wildcard/request-derived); `state` single-use, bound to session, validated before
exchange; nonce validated for OIDC id-token flows; implicit/password grants prohibited;
authorization-server metadata fixed configured origins; scopes minimized; refresh-token handling
per RFC 9700/RFC 10017 (sender-constrained or rotation+reuse-detection). Account linking:
authenticated, user-initiated, recent re-authentication; verified provider identity match; no
blind email-only merges; audit history retained; unlink/recovery cannot lock out or hijack.

**Unsafe evidence:** State optional/skipped; redirect URI built from request parameter; linking
accounts solely on matching email; PKCE omitted "because confidential client".

**Required negative test:** Replayed `state`/code must fail; forged callback with attacker
state must not bind accounts; linking second provider sharing only an email with an existing
account must require explicit verified flow, not auto-merge.

**Passing / Not verified:** Pass requires flow trace with fixed endpoints/constants and
linking-policy code evidence. Provider-side app registration values need dashboard evidence
else `Not verified` via adapter.

**Related skill routing:** `secod-auth-provider-integrations` + adapters own provider-profile
depth; `secod-web-security` overlap for browser edge cases routed there.

### `PROVISIONAL-identity-10` — Default/shared account hygiene

**Applicability:** Every deployed environment. Protects against well-known-credential entry.

**Inspect and verify:** No active well-known usernames (admin/root/vendor defaults) on deployed
auth surface; bootstrap/break-glass credentials rotated after initial setup with MFA enforced on
every privileged account; demo/test accounts removed or disabled in production; shared team
logins replaced by named identities.

**Unsafe evidence:** Default admin/admin-class credentials reachable in production; seed scripts
creating documented passwords executed against production; shared mailbox as sole 2FA target.

**Required negative test:** Attempting documented vendor defaults against deployed login must
fail; seeded test account must be disabled/unreachable.

**Passing / Not verified:** Pass requires account inventory evidence (dashboard export or DB
schema review) showing no defaults. Repository alone cannot prove deployed absence → `Not
verified` without that evidence.

**Related skill routing:** `secod-secrets-config` (default credential replacement), cloud
routers (IAM root/MFA), `secod-observability-response` (privileged-account monitoring).

## Exceptional and failure conditions

- Identity/session store unreachable: authorization must fail closed; review verifies fallback
  paths deny rather than degrade to anonymous-allowed.
- Partial revocation (some instances still accept revoked token): model assumes compromise;
  finding severity reflects propagation lag evidence.
- Recovery channel failure (email/SMS undeliverable): recovery must not fall back to weaker
  verification without explicit acceptance; delivery behavior `Not verified` without evidence.
- OAuth provider outage during callback: in-flight flows must fail safely, never auto-link
  partial identities.
- Concurrent session operations (logout vs refresh race): reuse-detection logic must not
  lock out legitimate fresh rotations; race handling traced.
- Never invent provider session lifetimes, retry schedules, or revocation guarantees; record as
  assumptions requiring provider documentation.
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-auth-provider-integrations` plus exact adapter (Clerk, Auth0, WorkOS,
Better Auth, Supabase Auth, Cognito, Entra) when detected; `secod-supabase-auth` with
`secod-supabase`; hosting/cloud adapters when platform IAM substitutes application identity.

If `secod-core` is missing/unresolved/malformed: mark inventory-dependent controls `Not
verified`, name the missing owner, never reconstruct inventories, never issue launch readiness.
If an applicable adapter is missing while its SDK is Active: affected provider controls stay
`Not verified`; core application controls are still evaluated.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: enforcement traces for every sensitive route; credential/session/
  token lifecycles fully traced; negative tests reasoned through code paths with expected deny
  outcomes; no default-account exposure evidence gaps.
- `Fix before launch`: any sensitive route lacking located guard; enumeration-distinct responses;
  non-hashed reset-token/key storage; missing tenant checks on private data; plaintext-equivalent
  session store.
- `Recommended hardening`: step-up coverage gaps on lower-risk actions; missing device inventory
  UI; SMS-only MFA on non-admin tiers.
- `Not verified`: provider dashboard policy, deployed JWKS/rotation state, recovery delivery
  behavior, deployed account inventory — each with the exact evidence needed named.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (credential types, providers by class, session
mechanisms per environment); test results; requested external evidence (dashboard exports,
provider docs confirmations, account inventories, by owner); `Not verified` items with next
verification step; launch blockers. Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; none execute code locally.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-identity-access/README.md` | Documentation-only plan | All controls |
| Cross-tenant object read as user B | Documentation-only case | -1 |
| Enumeration-distinct reset responses | Documentation-only case | -2, -5 |
| Factor removal without recent-auth challenge | Documentation-only case | -3 |
| Replayed WebAuthn challenge / wrong RP-ID | Documentation-only case | -4 |
| Fixation: pre-auth session ID survives login | Documentation-only case | -6 |
| Rotated refresh token reuse without family revocation | Documentation-only case | -6 |
| `alg:none` / token-supplied JWKS URL accepted | Documentation-only case | -7 |
| Revoked API key still authenticating | Documentation-only case | -8 |
| Blind email-only account merge | Documentation-only case | -9 |
| Documented default credentials working on deployed login | Documentation-only case | -10 |

Reasoning-based verification against described cases only. Never claim Markdown fixture plans
executed as code. Never run destructive, production-changing, user-creating, payment-creating,
refunding, key-rotating, dashboard-changing, or account-changing tests without explicit
authorization.

## References

- [`references/sources.md`](sources.md) — source register: RFC 10017 browser-based OAuth BCP,
  RFC 9700 OAuth security BCP, OWASP Authentication and Session Management cheat sheets.
