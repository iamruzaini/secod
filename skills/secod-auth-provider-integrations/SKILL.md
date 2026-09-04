---
name: secod-auth-provider-integrations
description: Review third-party authentication provider integrations for launch safety. Select an explicit version-qualified provider profile; verify every provider credential server-side against fixed issuer/audience/JWKS trust anchors; separate token purposes; bind redirects/state/nonce/PKCE; keep session cookies, CSRF checks and provider secrets intact across environments; design session revocation; map provider subjects to local tenants; gate account linking and authenticator migration; reconcile signed webhooks and directory-sync events. Apply when Clerk, Auth0, WorkOS, Better Auth, Supabase Auth or another supported third-party authentication SDK, hosted/custom auth domain, callback or redirect configuration, auth-provider webhook, SSO/SCIM/directory setup, passkey/MFA setting or provider environment variable is detected. Package presence alone is Candidate.
---

# Auth Provider Integrations Security

## Mission

Prove that every third-party authentication provider integration establishes identity through
server-side validation against fixed, allowlisted trust anchors, and that provider-driven
session, account-linking, migration and lifecycle events can neither escalate privileges nor
cross tenant or environment boundaries.

Repository-only review cannot prove provider Dashboard configuration, deployed tenant/project
state, live JWKS rotation behavior, webhook delivery semantics, or that reviewed code is what
production runs. `secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls: provider-profile selection and version qualification (`PROVISIONAL-AUTHPROV-01`
through `-11` below): provider inventory and environment separation; server-side token
verification against fixed trust anchors; token-purpose separation; OAuth flow selection;
redirect/logout/post-login binding; session-cookie, CSRF-check and provider-secret hygiene;
session-strategy and revocation design; provider-subject-to-tenant mapping; account
linking/merging/authenticator-migration gating; webhook signature verification and
directory-sync/event reconciliation.

Excluded controls and their owners:

- Application authorization primitives, session issuance/expiry depth, password/MFA/passkey
  flows independent of a provider — `secod-identity-access`.
- Browser cookie flags, token exposure in client bundles, CORS/CSP — `secod-web-app-security`,
  `secod-secrets-config`.
- Supabase database/Storage/Realtime/Edge Function RLS and data controls — `secod-supabase`;
  Supabase Auth feature depth — `secod-supabase-auth`.
- Provider-specific Dashboard/SDK depth beyond the profile baseline — `secod-clerk`,
  `secod-auth0`, `secod-workos`, `secod-better-auth`, `secod-aws-cognito`, and other adapters.
- Rate-limit implementation effectiveness — `secod-abuse-limits`.
- Generic webhook transport plumbing and queue failure handling — `secod-inputs-apis`,
  `secod-failure-safety`.
- Launch verdicts — `secod-ship-check`.

Direct dependencies (from `secod/catalog.json`): `secod-core`, `secod-identity-access`.

Conditional routes (real routes only): `secod-clerk`, `secod-auth0`, `secod-workos`,
`secod-better-auth` when the matching provider SDK/config/domain/webhook is Active;
`secod-supabase-auth` together with `secod-supabase` when Supabase Auth signals are Active;
`secod-aws-cognito` when Cognito User Pools are detected (it depends on this skill).

## Required inputs

Repository: lockfiles/package manifests for exact provider SDK versions; auth middleware,
callback handlers, token-verification code, session/cookie configuration; webhook route
handlers; environment-variable usage by name; deployment definitions and CI evidence; tests
covering negative cases.

Environment: development/preview/staging/production inventory of provider tenant/instance/
project IDs, application/client IDs, allowed origins, callback/logout/post-login URLs, enabled
connections, custom/hosted auth domains.

Commonly unavailable repository-only (require supplied evidence, else `Not verified`):
provider Dashboard session/MFA/authenticator/administrator settings; Management API/API-key
scopes; enabled SSO/SCIM connections and directory mappings; deployed signing-key/JWKS state;
webhook endpoint registration and secret rotation state; whether deployed instances run the
reviewed code.

Human-supplied evidence: authorized Dashboard exports, Management API reads, webhook delivery
logs, session-policy values per environment, incident-response procedures for provider outages.

Never read, print, or request secret values; variable names and redacted shapes only.

## Applicability and discovery

Signal groups:

- Package/SDK: `@clerk/*`/`clerk`, `@auth0/*`/`auth0`/`auth0-spa-js`/`express-oauth2-jwt-bearer`,
  `@workos-inc/*`, `better-auth`, `@supabase/supabase-js`, `@supabase/ssr`, provider CLI/SDK
  imports such as `supabase.auth.*`.
- Environment variables (names only): `SUPABASE_*`, `AUTH0_*`, `WORKOS_API_KEY`,
  `WORKOS_CLIENT_ID`, `BETTER_AUTH_SECRET`/`BETTER_AUTH_*`, `CLERK_*`.
- Routes/webhooks: `/callback`, `/login`, `/logout`, post-login redirects, provider webhook
  endpoints (Clerk/Svix, WorkOS Events, Auth0 hooks/actions, Better Auth hooks, Supabase Auth
  Hooks), SSO/SCIM/directory endpoints.
- Configuration: issuer constants, JWKS/discovery URLs, `trustedOrigins`/allowed-origin lists,
  cookie settings, PKCE/state options, custom or hosted auth domains.
- Deployment/provider evidence: hosted login domains reachable in configuration, Dashboard
  exports, deployment-correlated provider behavior.

Classification follows `secod-core`: package, example variable name, dormant file, or weak
signal only = `Candidate`; code/configuration exists but deployed/provider state unverified =
`Likely`; repository behavior correlates with deployed/runtime/Dashboard/Management-API/provider
evidence = `Active`.

Maintain separate development/preview/staging/production inventories. Conflicting or shared
environment signals (same tenant, callback set, secret, or database across environments) are
`Not verified` for every affected control.

## Review workflow

1. Inventory environments and trust boundaries: which providers are present, which tenant/
   project each environment points at, where provider credentials and callbacks flow.
   Parallelizable once discovery exists; no state changes.
2. Correlate active features and flows: sign-in methods live per provider, webhooks subscribed,
   directory sync enabled, account-linking/migration paths reachable. Parallelizable within one
   environment after step 1.
3. Verify applicable controls below against evidence, selecting the explicit provider profile
   first (`PROVISIONAL-AUTHPROV-01`).
4. Run safe negative tests: local reasoning/code-path tracing only — tampered tokens, foreign
   issuers, replayed states, cross-tenant claims, forged webhook signatures. No live attacks,
   no provider Dashboard changes, no test-user creation without explicit authorization.
5. Classify evidence, emit findings, route provider-specific gaps to the owning adapter, hand
   off to `secod-ship-check`.

Steps 1–2 may run in parallel across environments because evidence is independent and no state
changes; steps 3–5 are sequential per control.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-AUTHPROV-N` and require catalog approval before promotion.

### `PROVISIONAL-AUTHPROV-01` — Explicit, version-qualified provider profile

**Applicability:** Every detected third-party auth provider. Protects against reviewing an
unsupported integration under invented assumptions.

**Inspect and verify:** Identify each provider and its exact SDK/configuration versions from
lockfiles; select the matching profile from the profile table below; declare the profile and
versions in the report. Profiles must use current official documentation and may add
provider-specific requirements; they never weaken this baseline. When no supported,
version-qualified profile exists, report the affected provider's controls `Not verified` and
request the direct official source needed to build one.

**Unsafe evidence:** A profile guessed from package presence; version ranges unresolved;
provider-specific behavior asserted without a current official source.

**Required negative test:** For an unsupported-version case (SDK major older than the profile's
supported range), confirm the report marks profile-dependent controls `Not verified` instead of
passing them.

**Passing / Not verified:** Pass requires declared profile plus exact versions plus a retained
official source per applicable provider. Missing versions or missing source = `Not verified`.

**Related skill routing:** Deep provider verification — `secod-clerk`, `secod-auth0`,
`secod-workos`, `secod-better-auth`, `secod-supabase-auth` (with `secod-supabase`),
`secod-aws-cognito`.

Profile baseline (each profile adds requirements; none relax this skill):

| Profile | Adapter owner | Profile additionally verifies |
| --- | --- | --- |
| Clerk | `secod-clerk` | Dashboard session limits; active-session listing/revocation; organization claims incl. per-tab active-organization tokens |
| Auth0 | `secod-auth0` | RS256/JWKS cache behavior; refresh-token rotation; Management API scope least privilege |
| WorkOS | `secod-workos` | One-time refresh tokens; staging/production isolation; SSO organization mapping; Events API/webhook reconciliation |
| Supabase Auth | `secod-supabase-auth` | Publishable/secret/service-role authority boundaries; asymmetric signing-key/JWKS rotation; session and refresh-token-reuse policy; SSR/redirect configuration; MFA AAL2 enforcement; Auth Hook least privilege; RLS tenant authorization |
| Better Auth | `secod-better-auth` | Exact `trustedOrigins` allowlist; origin/CSRF checks never disabled; secure cookie/session settings; trusted SSO discovery origins |

### `PROVISIONAL-AUTHPROV-02` — Provider inventory and environment separation

**Applicability:** Every environment touching a provider. Protects against production/test
tenant, callback, custom-domain, secret, and database mix-ups.

**Inspect and verify:** Per environment: provider tenant/instance/project identifier,
application/client ID, allowed origins, callback/logout/post-login URLs, enabled connections,
custom/hosted auth domains, session policy source, administrators, Management API/API-key
scopes, provider role/directory mappings. Production must reference production-only tenant,
secrets, and callback set; localhost/development origins absent from production allowlists;
no shared database across environments holding provider-linked identities.

**Unsafe evidence:** One tenant serving dev and prod; production callback lists containing
localhost or preview domains; identical client secrets across environments; staging API keys in
production configuration.

**Required negative test:** Trace one production sign-in and one staging sign-in end-to-end;
each must resolve to distinct tenant/client/callback/secret values. Any overlap = finding.

**Passing / Not verified:** Pass requires complete per-environment inventory from repository
plus supplied provider evidence. Dashboard-side connection/administrator state unverifiable =
`Not verified` until exported.

**Related skill routing:** Secret storage mechanics — `secod-secrets-config`; adapter skills
for Dashboard exports.

### `PROVISIONAL-AUTHPROV-03` — Server-side token verification against fixed trust anchors

**Applicability:** Every acceptance point for a provider-issued JWT/OIDC token (session tokens,
ID tokens, access tokens). Protects against forgery, algorithm confusion, and discovery abuse.

**Inspect and verify:** Verification runs server-side using an allowlisted exact issuer,
expected audience/client ID, pinned allowed algorithms, signature, lifetime (`exp`/`nbf`
where present), subject, and required claims. Keys/metadata come only from trusted configured
JWKS/discovery origins; `kid` cached, refreshed once bounded on unknown `kid`, refetches
rate-limited, rotation handled; client-supplied issuer, discovery URL, JWKS URL, algorithm, or
tenant identifier never trusted. IdP-initiated SSO assertions pass the same checks.

**Unsafe evidence:** `decode()`-without-verify in any request path; JWKS/issuer URL taken from
the token; `alg` accepted from token header; audience check skipped; unbounded refetch allowing
JWKS-flood; stale keys accepted indefinitely.

**Required negative test:** Token with `alg: none`, wrong-key signature, foreign issuer,
mismatched audience, or expired lifetime must each be rejected; rotated-out key must fail after
the documented grace window.

**Passing / Not verified:** Pass requires traced verification against fixed configured anchors
for every token class. Deployed rotation behavior needs runtime/provider evidence else
`Not verified`.

**Related skill routing:** Generic JWT depth — `secod-identity-access`; provider specifics —
adapter skills.

### `PROVISIONAL-AUTHPROV-04` — Token-purpose separation

**Applicability:** Every place a provider token authorizes something. Protects against ID-token
and cross-resource misuse.

**Inspect and verify:** Each credential is verified as its intended token class: ID tokens
never accepted as API or provider-management bearer credentials; access tokens accepted only
for their intended resource/audience; Management API credentials used server-side only, with
least-scoped permissions; refresh tokens never treated as access credentials.

**Unsafe evidence:** ID token sent as `Authorization: Bearer` to the app API; Management API
token exposed to clients; access token for resource A accepted by service B.

**Required negative test:** Replay a valid ID token against the app API and a wrong-audience
access token against a protected endpoint; both must reject.

**Passing / Not verified:** Pass requires token-class checks at every accepting endpoint.
Cross-service acceptance without evidence = `Fix before launch`.

**Related skill routing:** Client-side exposure — `secod-web-app-security`; API-key class —
`secod-identity-access`.

### `PROVISIONAL-AUTHPROV-05` — OAuth flow selection

**Applicability:** Every provider-mediated browser/public-client login. Protects against
code interception and legacy-flow downgrade.

**Inspect and verify:** Authorization Code + PKCE for public clients; implicit and deprecated
or otherwise unsafe flows prohibited under the selected profile; grant types on the provider
application restricted to those actually used; scopes minimized to features in use.

**Unsafe evidence:** Implicit flow configured; PKCE omitted for SPA/mobile; unused grants
(Password, client-credentials in browser) left enabled.

**Required negative test:** Attempt a response-type/id-token-only flow for a public client;
it must fail or be absent from allowed grant types.

**Passing / Not verified:** Pass requires flow construction in code plus provider-application
grant configuration evidence. Grant configuration unverifiable = `Not verified` via adapter.

**Related skill routing:** RFC 9700 conformance detail — `secod-identity-access`; adapter
skills for provider application settings.

### `PROVISIONAL-AUTHPROV-06` — Redirect, logout, and anti-CSRF parameter binding

**Applicability:** Every provider round-trip (login, logout, post-login, invitation links).
Protects against open redirects and CSRF/code-injection.

**Inspect and verify:** Exact redirect, logout, and post-login destinations bound and validated
against allowlists registered per environment; trusted origins exact; `state` single-use,
session-bound, validated before exchange; nonce validated for OIDC ID-token flows; PKCE
verifier generated high-entropy and checked at token exchange; no wildcards, no
request-derived return URLs, no development-origin leakage into production; IdP-initiated
flows land on validated defaults, not arbitrary `next` parameters.

**Unsafe evidence:** Redirect URI built from query parameters; wildcard subdomain patterns in
production allowlists; `state` optional or logged-and-reused; verifier accepted from client
without challenge binding.

**Required negative test:** Callback with manipulated destination, reused `state`, mismatched
nonce, or swapped PKCE verifier must each fail closed with no redirect issued.

**Passing / Not verified:** Pass requires parameter-handling traces for every provider
round-trip plus registered allowlist evidence per environment. Registered values need provider
evidence else `Not verified`.

**Related skill routing:** Open-redirect breadth — `secod-web-app-security`; adapter skills.

### `PROVISIONAL-AUTHPROV-07` — Session cookies, CSRF checks, and provider-secret hygiene

**Applicability:** Every provider-backed session and every provider credential. Protects
against fixation, CSRF-downgrade, and secret leakage.

**Inspect and verify:** Session cookies Secure, HttpOnly, appropriately scoped SameSite;
origin/CSRF checks enabled — never disabled without documented compensating controls recorded
by the owner; provider and management secrets server-side only, least-scoped, rotated with
evidence; sealed-session or cookie-signing secrets versioned with a rotation plan; no secret,
cookie, or bearer value in logs, client bundles, URLs, or reports.

**Unsafe evidence:** `disableCSRFCheck`/equivalent set in production; secrets imported into
client code; unversioned single sealing secret with no retirement plan; debug logging of
headers/cookies.

**Required negative test:** Cross-site state-changing request against a provider-session
endpoint must be rejected; grep-level scan confirms no secret-shaped literals reach client
bundles.

**Passing / Not verified:** Pass requires cookie/CSRF configuration traces plus secret-storage
evidence. Rotation history needs provider/ops evidence else `Not verified`.

**Related skill routing:** Cookie flags depth — `secod-web-app-security`; secret storage —
`secod-secrets-config`; Better Auth specifics — `secod-better-auth`.

### `PROVISIONAL-AUTHPROV-08` — Session strategy and revocation design

**Applicability:** Every provider session model. Protects against unrevocable stolen sessions.

**Inspect and verify:** Record the provider session strategy (stateful store vs stateless JWT)
with expiry, device/session listing, and revocation behavior per environment. Where a
stateless/JWT session cannot be immediately revoked, require an explicitly accepted
short-lifetime plus denylist/re-authentication design, or a stateful session store, for the
affected risk tier; logout invalidates server state, not only client artifacts; sensitive-action
reauthentication defined where the provider supports step-up.

**Unsafe evidence:** Long-lived stateless tokens with no denylist for privileged roles; logout
clearing cookie only while the provider session stays valid; no session-inventory surface for
users.

**Required negative test:** Revoke a session (documented procedure or fixture reasoning); the
revoked token must fail on next use within the documented propagation window; stateless designs
must show the bound on post-revocation usability.

**Passing / Not verified:** Pass requires documented strategy plus revocation-path traces.
Live revocation latency needs runtime evidence else `Not verified`.

**Related skill routing:** Session lifecycle primitives — `secod-identity-access`; adapter
skills for Dashboard session settings.

### `PROVISIONAL-AUTHPROV-09` — Identity-to-tenant mapping

**Applicability:** Every provider identity used for local authorization. Protects against
tenancy escalation via malleable claims.

**Inspect and verify:** Immutable provider subject plus organization/directory/membership
identifiers map to local user and tenant records at every authorization decision; tenancy,
admin role, or membership never granted solely from email domain, display name, unverified
email, or browser-held claims; organization switches re-resolve membership server-side; stale
custom claims not relied on where fresh server-side state is required.

**Unsafe evidence:** Tenant chosen from a JWT claim without membership recheck; email-domain
match granting organization access; UI-only active-organization state driving backend queries.

**Required negative test:** Present a valid token whose organization claim references a
tenant the user does not belong to; access must be denied server-side.

**Passing / Not verified:** Pass requires mapping traces for every provider-fed authorization
path. Directory-membership freshness needs provider event evidence (control `-11`) else
`Not verified` for lag-sensitive paths.

**Related skill routing:** BOLA/IDOR depth — `secod-identity-access`; organization features —
`secod-clerk`, `secod-auth0`, `secod-workos`, `secod-supabase-auth`.

### `PROVISIONAL-AUTHPROV-10` — Account linking, merging, and authenticator migration

**Applicability:** Every link/unlink/email-change/factor-change/account-merge and every
password↔OAuth↔passkey identity migration. Protects against takeover via linking and loss of
access during migration.

**Inspect and verify:** Linking, unlinking, email/factor changes, and merges require recent
authentication plus verified control of both identities; audit events recorded; affected
sessions notified; safe recovery preserved. Migration preserves the immutable local account,
requires a verified new authenticator and a valid recovery path, retains no stale access from
the replaced method, and prevents loss of the final recovery method; staged migration,
rollback, and re-authentication tested before cutover.

**Unsafe evidence:** Automatic merge on equal emails; unlink leaving zero remaining
authenticators; migration deleting the old credential before the new one verifies; no rollback
path.

**Required negative test:** Attempt to link an attacker-controlled provider identity sharing
only an email with a victim account; it must require verified control of both identities, not
auto-merge. Migration dry-run must show old access revoked and recovery intact.

**Passing / Not verified:** Pass requires linking/migration flow traces plus policy evidence.
Provider-side linking defaults need adapter evidence else `Not verified`.

**Related skill routing:** Account-linking baseline — `secod-identity-access`; provider
linking behavior — `secod-clerk`, `secod-better-auth`, `secod-auth0`.

### `PROVISIONAL-AUTHPROV-11` — Webhook authenticity and directory-sync reconciliation

**Applicability:** Every provider webhook/event consumer and every directory-sync-driven
access change. Protects against spoofed events and lifecycle lag.

**Inspect and verify:** Raw-body signatures verified with the provider SDK/constant-time
comparison; timestamp/ID fields checked where the provider supports them; provider event
version handled; deduplication on event ID; replay and out-of-order tolerance; failure handling
that queues or rejects rather than silently dropping. A missing, delayed, or out-of-order
webhook never proves access; provider events reconciled against provider API state before
granting, changing, or revoking directory-driven access; deprovisioning, organization
membership, directory-sync, and role-change events applied to local access with durable
event/offset tracking and periodic reconciliation.

**Unsafe evidence:** Signature check reading parsed JSON instead of raw body; events trusted
as sole proof of access; deleted-directory member retaining local role after reconciliation
window; offsets stored non-durably so restarts skip events.

**Required negative test:** Webhook with invalid signature, duplicated event ID, and stale
timestamp must each be rejected or ignored idempotently; simulated deprovisioning lag must
show reconciliation closing the gap within the documented window.

**Passing / Not verified:** Pass requires handler traces plus subscription evidence. Delivery
guarantees stay assumptions backed by provider docs — never invented schedules.

**Related skill routing:** Transport plumbing — `secod-inputs-apis`; queue failures —
`secod-failure-safety`; Clerk/Svix and WorkOS specifics — `secod-clerk`, `secod-workos`.

## Exceptional and failure conditions

- Provider/verification dependency timeout or outage: authentication fails closed; fallback
  paths must deny, never degrade to unverified acceptance.
- Partial operations (link created but local record write fails): cleanup/rollback or durable
  compensation required; orphaned half-links reported as findings.
- Retry and cancellation of migration/linking jobs: idempotent, resumable, no duplicate
  identities or lost authenticators.
- Session/token revocation propagation: bounded, documented windows; unbounded stateless
  validity for privileged roles is `Fix before launch`.
- Webhook duplicate, replay, redelivery, and failure: idempotent consumers, dedup on provider
  event ID, poison-event quarantine; never treat absence of webhooks as success.
- Never invent provider retry schedules, delivery guarantees, default lifetimes, plan or region
  availability; record unsupported claims as assumptions requiring official-source evidence.
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`, `secod-identity-access`.
Conditional routes: `secod-clerk`, `secod-auth0`, `secod-workos`, `secod-better-auth`,
`secod-supabase-auth` (always with `secod-supabase`), `secod-aws-cognito`.

If a required dependency or applicable route is missing, unresolved, malformed, or incomplete:
mark the affected controls `Not verified`; name the missing owner/evidence; never invent
replacement dependencies or routes; never issue launch readiness. Core application controls
remain evaluable even when an adapter is absent.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Do not ship`: client-supplied trust anchors accepted (`-03`); ID token used as API/management
  bearer (`-04`); origin/CSRF checks disabled in production without compensating controls
  (`-07`); production/test tenant or secret mix-up (`-02`).
- `Fix before launch`: missing signature/claim validation on any accepting endpoint (`-03`);
  unsigned webhooks granting access (`-11`); tenancy granted from email domain or unverified
  claims (`-09`); auto-merge linking (`-10`); no revocation design for privileged stateless
  sessions (`-08`).
- `Recommended hardening`: wildcard-but-scoped origins in non-production; session-inventory UX
  gaps; reconciliation windows longer than documented SLA; missing step-up on lower-risk actions.
- `Not verified`: Dashboard session/MFA/connection/administrator settings, Management API
  scopes, deployed signing-key/JWKS state, webhook registration/secret rotation, deployed
  instance parity — each with the exact evidence needed named.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (providers × environments, profile selected with
SDK versions, token classes, webhook subscriptions); test results; requested external evidence
(Dashboard exports, Management API reads, webhook logs, by owner); `Not verified` items with
next verification step; launch blockers. Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; none execute code locally.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-auth-provider-integrations/README.md` | Documentation-only plan | All controls |
| Callback/trusted-origin manipulation | Documentation-only case | -06 |
| Issuer/audience/token-type/JWKS confusion | Documentation-only case | -03, -04 |
| Stale/rotated key acceptance; provider discovery abuse | Documentation-only case | -03 |
| IdP-initiated SSO bypassing parameter binding | Documentation-only case | -05, -06 |
| Test/production tenant cross-wiring | Documentation-only case | -02, -07 |
| Revoked session still accepted (stateless vs stateful) | Documentation-only case | -08 |
| Organization/tenant mismatch; stale custom claims | Documentation-only case | -09 |
| Account-linking takeover; unverified-email merge | Documentation-only case | -10 |
| Authenticator migration losing final recovery method | Documentation-only case | -10 |
| Webhook replay/duplicate; deprovisioning lag | Documentation-only case | -11 |
| Missing-evidence case (no Dashboard export supplied) | Documentation-only case | All → `Not verified` |

Reasoning-based verification against described cases only. Never claim Markdown fixture plans
executed as code. Never run destructive, production-changing, user-creating, payment-creating,
refunding, key-rotating, dashboard-changing, or account-changing tests without explicit
authorization.

## References

- [`references/sources.md`](sources.md) — source register: portable normative sources (OWASP
  Authentication/MFA/OAuth cheat sheets, RFC 9700, W3C WebAuthn L3) and per-provider official
  indexes plus control-specific direct pages with review status.
