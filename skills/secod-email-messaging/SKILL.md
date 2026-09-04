---
name: secod-email-messaging
description: Review email, SMS, OTP, magic-link, invitation and notification delivery security. Apply when an SMTP/provider SDK (nodemailer, resend, @sendgrid/mail, postmark.js, AWS SES, mailgun), OTP library (otplib, speakeasy, otpauth), magic-link flow, invitation flow or delivery webhook receiver is present. Package presence alone is Candidate.
---

# Email Messaging Security

## Mission

Keep outbound message delivery (email/SMS/OTP/magic links/invitations/notifications) from becoming an
account-takeover, spoofing, injection or spam-amplification vector: delivery credentials stay
server-controlled, recipient-bound state stays server-resolved, one-time links/codes stay single-use
and expiring, and the sending domain proves its identity with SPF, DKIM and DMARC.

Repository-only review cannot prove DNS authentication records, provider account configuration,
Dashboard/API settings, actual delivery outcomes, webhook endpoint reachability or production bounce
behavior. Those require external evidence; absent evidence is `Not verified`.
`secod-ship-check` owns final launch readiness; this skill never issues it alone.

## Scope and ownership

Owned controls: message-delivery security (`PROVISIONAL-EMAIL-01` through `PROVISIONAL-EMAIL-11`
below). The catalog defines no stable control IDs for this skill yet; these are provisional and
catalog approval is required before promotion.

Excluded controls and their owners:

- General secret storage/handling discipline: `secod-secrets-config`; this skill verifies only the
  delivery-credential subset inside EMAIL-01.
- Rate-limit mechanics, idempotency stores, quota infrastructure: `secod-abuse-limits`; this skill
  verifies only the email-flow application (uniform responses, send ceilings) inside EMAIL-04.
- Token cryptography depth (CSPRNG, hashing, key lifecycle): `secod-crypto-data-protection`.
- Authentication/session semantics behind magic links and OTPs: `secod-identity-access`.
- Webhook signature/authenticity mechanics: `secod-inputs-apis`; this skill requires verification
  exists (EMAIL-08) but does not own HMAC/TLS detail.
- XSS/output-encoding primitives and CSP: `secod-web-app-security`.
- Generic failure handling, rollback, circuit breakers: `secod-failure-safety`.
- Provider-native account/plan/domain configuration: owning provider skill when one exists.

Direct dependencies (copied exactly from `secod/catalog.json`): `secod-core`.

Conditional routes (only when the detected feature applies):

- Auth flows delivered by email/SMS (login, recovery, verification): `secod-identity-access`,
  plus the matching auth-provider adapter when one is used.
- Delivery-webhook receivers: `secod-inputs-apis`.
- Sending-rate/quota infrastructure: `secod-abuse-limits`.
- Provider platform specifics (SES/IAM, SendGrid account settings, Supabase Auth SMTP): the owning
  provider skill when one exists.

## Required inputs

Repository-supplied:

- Sending code paths: templates, provider clients, SMTP configuration, OTP/magic-link generation,
  invitation and notification flows.
- Environment-variable usage showing per-environment provider credentials and sender identities.
- Route inventory: send endpoints (`/api/auth/*`, `/invite`, `/verify`, `/unsubscribe`),
  delivery/bounce/complaint webhook receivers.
- Tests covering expired/replayed/consumed tokens, duplicate webhook deliveries and failed sends.
- Deployment definitions separating development, preview, staging and production.

Commonly unavailable repository-only inputs (label as such when absent):

- DNS evidence for the sending domain: SPF, DKIM selectors, DMARC record.
- Provider Dashboard/API evidence: verified sender domains, webhook signing secrets, suppression
  lists, sending-domain reputation and plan limits.
- Production evidence: delivery logs, bounce rates, actual webhook deliveries.
- Human confirmation of alert recipients for deliverability failures.

## Applicability and discovery

Inventory each environment separately. Conflicting or shared environment signals across
development/preview/staging/production are `Not verified`.

Signal groups:

- Package/SDK: `nodemailer`, `resend`, `@sendgrid/mail`, `postmark.js`, `mailgun.js`,
  `aws-sdk/` SES clients, `@upstash/qstash` email helpers, SMTP transports, `react-email`, `mjml`;
  OTP libraries `otplib`, `speakeasy`, `otpauth`; SMS providers; notification frameworks.
- Environment variables: `SMTP_*`, `RESEND_API_KEY`, `SENDGRID_API_KEY`, `SENDGRID_WEBHOOK_KEY`,
  `POSTMARK_TOKEN`/`POSTMARK_WEBHOOK_SECRET`, `MAILGUN_API_KEY`/`MAILGUN_WEBHOOK_SIGNING_KEY`,
  `AWS_SES_*`, `TWILIO_*`, `EMAIL_FROM`,
  `NEXT_PUBLIC_*` mail/redirect variables.
- Routes/webhooks: magic-link issue/verify, OTP issue/verify, password-recovery senders,
  invitation accept, unsubscribe, provider webhook receivers (`/webhooks/resend`,
  `/webhooks/sendgrid`, `/webhooks/postmark`, `/webhooks/ses`, `/webhooks/twilio`).
- Configuration: sender/from addresses, reply-to, redirect/base URLs, template directories,
  link-tracking toggles, suppression-list handling.
- Deployment/provider evidence: DNS TXT/CNAME records for the sending domain, provider domain
  verification status, webhook signing-secret configuration, dashboard event logs.

Classification:

- `Candidate`: package installed, example variable, dormant template file or weak signal only.
- `Likely`: repository code/config implements a control; deployed/DNS/provider state unverified.
- `Active`: repository behavior correlates with DNS records, provider Dashboard/API, runtime or
  webhook evidence.

## Review workflow

Steps 1 and 2 are parallelizable; later steps depend on them.

1. Inventory environments and trust boundaries: every message-sending path, what triggers it, which
   credentials it uses, which recipient identity it trusts, per environment.
2. Correlate active features and flows: map each flow (login, recovery, invite, notification,
   marketing) to its token model, redirect targets and provider.
3. Verify applicable controls below against repository evidence first, then DNS and provider
   evidence.
4. Run safe negative tests locally or in an authorized non-production environment only.
5. Classify evidence and route findings per status rules and the ownership table.

## Control requirements

### `PROVISIONAL-EMAIL-01` — Server-only delivery credentials and sender identity

**Applicability:** Every configured email/SMS provider integration. Protected property: nobody can
send as the application's domains using client-reachable material.

**Inspect and verify:** Provider API keys, SMTP passwords, signing secrets referenced only in
server code/server env; different credentials (or at minimum separate scopes/domains) between test
and production environments; from/reply-to addresses fixed server-side; no credential or signing
secret in client bundles, public env prefixes, repo files or logs.

**Unsafe evidence:** API key in client-callable code or `NEXT_PUBLIC_*` variable; same production
key reused in preview/dev; SMTP password committed; from-address accepted from request body.

**Required negative test:** Build the client bundle and grep it for provider key patterns; expect
no match. Request a send endpoint with a forged from/recipient override; expect the server value
used or rejection.

**Passing / Not verified:** Pass requires server-only credential wiring plus the bundle test per
environment class. Package presence alone or inaccessible env/deployment state is `Not verified`.

**Related skill routing:** Secret-storage depth: `secod-secrets-config`; provider platform detail:
owning provider skill.

### `PROVISIONAL-EMAIL-02` — Recipient and tenant binding

**Applicability:** Every send whose content grants access, privilege or sensitive information:
magic links, OTPs, invitations, passwordless login, admin notifications. Protected property:
message content reaches only the intended principal of the intended tenant.

**Inspect and verify:** Recipient derived server-side from the authenticated session or from
verified input for pre-auth flows; invitation binds invitee email, tenant/workspace and role at
creation time; token/state stored with tenant scope; accepting an invite or link checks the
presenting user against the stored binding; no client-supplied recipient for privileged content.

**Unsafe evidence:** Invite acceptance trusts only the token without checking presenting identity;
magic-link token usable by any session; tenant ID taken from request payload instead of server
state; cross-tenant resend possible.

**Required negative test:** Present a valid invitation/token while authenticated as a different
principal or in another tenant context; expect rejection. Alter tenant/email fields in the accept
request; expect no effect.

**Passing / Not verified:** Pass requires binding checks in code plus the negative test. Missing
tenant model evidence is `Not verified`.

**Related skill routing:** Tenant isolation depth: `secod-threat-model`, `secod-identity-access`.

### `PROVISIONAL-EMAIL-03` — Single-use expiring magic links and OTPs

**Applicability:** Every emailed/emailed-code credential: magic links, login codes, recovery codes,
verification codes. Protected property: stolen or forwarded message yields at most one short-lived
use by the bound principal.

**Inspect and verify:** Tokens/codes generated with a CSPRNG; stored hashed (not plaintext);
explicit expiry short enough for the flow's risk; consumed atomically on first redemption so reuse
fails; issuance invalidates prior outstanding tokens for the same purpose; OTP attempt-count cap
with lockout/expiry; comparison constant-time.

**Unsafe evidence:** Long-lived or non-expiring links; token stored plaintext; redemption not
atomic (two concurrent clicks both succeed); old links remain valid after new ones are issued;
unlimited OTP guessing; sequential/guessable codes.

**Required negative test:** Redeem the same link/code twice; second attempt fails. Attempt more
than the configured number of wrong OTPs; further attempts rejected. Expired token rejected.

**Passing / Not verified:** Pass requires code-path evidence plus all three tests. Library presence
alone is `Not verified`. Cryptographic primitive selection depth routes to `secod-crypto-data-protection`.

**Related skill routing:** Identity semantics: `secod-identity-access`; token crypto:
`secod-crypto-data-protection`.

### `PROVISIONAL-EMAIL-04` — Anti-enumeration and sending abuse limits on message flows

**Applicability:** Every endpoint that triggers a send keyed to an identifier a third party knows
(email, phone): login-with-magic-link, recovery, signup verification, invitations, marketing sends.
Protected property: attacker cannot discover which accounts exist nor drain provider quota.

**Inspect and verify:** Identical user-visible response and timing whether or not the address
exists; per-recipient and per-source send ceilings enforced server-side before dispatch;
re-request throttling (cooldown between resends); invitation sending limited per user/tenant;
limits backed by a store consistent across instances.

**Unsafe evidence:** Distinct responses/messages/timings for existing versus unknown addresses;
unbounded resend; invitation flood possible with free accounts; limiter present only in UI.

**Required negative test:** Submit known and unknown addresses through the same flow; compare
responses byte-for-byte and timing; both identical. Exceed the resend ceiling; further requests
throttled.

**Passing / Not verified:** Pass requires uniform-response evidence plus ceiling tests. Limiter
infrastructure depth stays with `secod-abuse-limits`.

**Related skill routing:** Limit mechanics and quotas: `secod-abuse-limits`; response-uniformity
background: OWASP Authentication Cheat Sheet (see `references/sources.md`).

### `PROVISIONAL-EMAIL-05` — Safe redirect destinations after link/OTP redemption

**Applicability:** Every message containing a link that lands back in the application with a token
(magic link, verify, invite accept, unsubscribe). Protected property: redemption redirects only to
pre-approved destinations; the token never leaks to other origins.

**Inspect and verify:** Redirect target validated against a server-side allowlist of exact hosts/
paths (not prefix/substring matching); open-redirect parameters (`next`, `redirect_url`,
`returnTo`) validated or ignored; token carried in path/body rather than query string where the
framework allows, or Referer-leak risk addressed; HTTPS-only absolute URLs in all outbound links;
link host matches the deployed environment.

**Unsafe evidence:** Redirect built from unvalidated request parameter; wildcard allowlist such as
`*.example.com` matching attacker subdomains; HTTP links; staging URLs leaking into production
messages; token echoed to a third-party tracker URL.

**Required negative test:** Redeem with `?next=https://evil.example` style parameter; expect
fallback to default destination. Craft link with lookalike host; expect rejection.

**Passing / Not verified:** Pass requires allowlist validation plus the open-redirect test.
General redirect hygiene beyond message flows routes to `secod-inputs-apis`.

**Related skill routing:** Redirect/SSRF boundaries: `secod-inputs-apis`.

### `PROVISIONAL-EMAIL-06` — Link-tracking and scanner compatibility without weakening tokens

**Applicability:** Any flow where click-tracking rewrites, prefetching (security scanners, corporate
mail proxies) or bot crawlers may hit one-time links. Protected property: automated prefetches do
not burn single-use tokens nor reveal validity.

**Inspect and verify:** Redemption endpoint distinguishes human confirmation from bare prefetch —
for example a confirmation interstitial or POST-based redemption — so GET-prefetch alone does not
consume the token; click-tracking rewrites preserve the original destination's security properties;
tracking disabled for authentication-critical messages; monitoring distinguishes prefetch bursts
from real redemptions.

**Unsafe evidence:** Plain GET consumes the token (first scanner prefetch locks out the user);
tracking service inserted between user and redemption that receives the raw token; expiry extended
to survive scanners instead of fixing consumption semantics.

**Required negative test:** Issue a token, GET the redemption URL twice without confirming; then
confirm once; expect exactly one successful redemption and the user able to complete the flow.

**Passing / Not verified:** Pass requires consumption-semantics evidence plus the test. Where the
application documents that scanners are trusted to consume, treat as unsafe and record finding.

**Related skill routing:** None beyond owned controls.

### `PROVISIONAL-EMAIL-07` — Template and HTML/header injection prevention

**Applicability:** Every message built from dynamic data: user names, emails, tenant names, URLs,
support replies. Protected property: attacker-controlled data cannot inject HTML/script into the
rendered message or extra headers/recipients into the SMTP envelope.

**Inspect and verify:** Templating engine auto-escaping enabled and dynamic values passed as
variables, never concatenated into HTML strings; subject/to/from built through the provider SDK's
address/subject APIs (CRLF-safe) rather than raw string assembly; plain-text alternative rendered
from the same escaped data; no user-controlled `<a href>` targets except allowlisted URL schemes;
links generated from server-side base URLs.

**Unsafe evidence:** String concatenation into HTML body; user input in subject line without the
SDK API; user-controlled URL rendered as clickable link without scheme/host validation; template
partials accepting raw HTML from database fields populated by users.

**Required negative test:** Register/display a name or tenant containing `<img src=x onerror=...>`
and CRLF sequences; received message shows escaped text, renders nothing, adds no header/recipient.

**Passing / Not verified:** Pass requires escaping/path evidence plus the probe against a locally
rendered template. Output-encoding primitives route to `secod-web-app-security`.

**Related skill routing:** XSS encoding depth: `secod-web-app-security`.

### `PROVISIONAL-EMAIL-08` — Verified and deduplicated delivery webhooks

**Applicability:** Every receiver for provider events: delivered, bounced, complained, opened,
clicked. Protected property: only the provider can mutate delivery-derived state, and each event
mutates it exactly once.

**Inspect and verify:** Signature/HMAC or documented verification mechanism checked over raw body
before any state change; secret stored server-side; duplicate/redelivery handled through persisted
event IDs so replay is idempotent; handler validates event type/schema before acting; failures
return error status so the provider retries rather than silent 200 swallowing; endpoint not
enumerable or guessable beyond the signature requirement.

**Unsafe evidence:** Webhook processed on URL obscurity alone; verification skipped or applied
after side effects; duplicates create repeated state transitions; handler returns 200 regardless.

**Required negative test:** Post an unsigned/incorrectly signed event; expect rejection with no
state change. Redeliver a captured valid event; expect exactly one state transition.

**Passing / Not verified:** Pass requires verification-in-code plus both tests. Signature-scheme
detail and transport rules belong to `secod-inputs-apis`; never invent a specific provider's
signing algorithm — cite the provider's own documentation or leave `Not verified`.

**Related skill routing:** Signature mechanics: `secod-inputs-apis`; billing-adjacent events:
`secod-payments-billing` when payment state derives from them.

### `PROVISIONAL-EMAIL-09` — Bounce and suppression handling

**Applicability:** All recurring or bulk sending to user-provided addresses. Protected property:
the system stops mailing dead/abusive addresses and keeps reputation intact without dropping
critical transactional mail silently.

**Inspect and verify:** Hard-bounce and complaint events feed a suppression list honored before
every send; suppression scoped per environment; permanent versus transient classification recorded;
critical transactional failures surfaced to the requesting user/support channel instead of failing
silently; unsubscribe honored for non-transactional classes.

**Unsafe evidence:** Sends continue after hard bounces; suppression shared between dev and prod;
bounce webhook ignored entirely; recovery/password-reset mails suppressed without alternate path.

**Required negative test:** Mark an address suppressed (non-production); trigger a bulk flow; expect
no send to that address. Trigger a transactional flow for the suppressed address; expect explicit
failure surfaced, not silent success.

**Passing / Not verified:** Pass requires suppression logic in code plus webhook linkage from
EMAIL-08. Provider-side suppression state without Dashboard evidence is `Not verified`.

**Related skill routing:** Monitoring/alerting: `secod-observability-response`.

### `PROVISIONAL-EMAIL-10` — Sending-domain SPF, DKIM and DMARC evidence

**Applicability:** Every domain the application sends from. Protected property: third parties can
verify the application's mail and spoofers cannot pass as it.

**Inspect and verify:** Derive every RFC5322.From Author Domain and DKIM selector from server-side
configuration or provider evidence. Run timestamped DNS queries for: SPF authorization ending in
`-all`; provider DKIM selectors; and the applicable DMARC Policy Record found by RFC 9989 policy
discovery/DNS tree walk. Verify at least one authenticated SPF or DKIM identifier aligns with the
Author Domain; prefer both. For `p=reject`, require aligned DKIM, not SPF alone. Repository
configuration/IaC must match but never substitutes for live DNS. RFC 7489 is obsolete; use RFCs
9989, 9990 and 9991.

**Unsafe evidence:** No SPF record or `+all`/`?all`; missing DKIM selector; no applicable DMARC
record; no aligned authenticated identifier; `p=reject` relying only on SPF; obsolete `pct` treated
as a rollout control; from-domain differing from any verified provider domain. `p=none` is valid,
but call it monitoring mode only when aggregate reports are requested and received; otherwise
report missing enforcement/monitoring evidence without claiming RFC noncompliance.

**Required negative test:** Query DNS for a lookalike/unconfigured subdomain used nowhere; confirm
no stray records authorize unknown senders. Confirm the SPF evaluation of the production provider
path resolves within DNS lookup limits (safe read-only `dig`/`Resolve-DnsName`). Confirm DMARC
policy discovery for an applicable sending subdomain resolves to the expected direct or inherited
policy, including `sp`/`np` behavior where relevant.

**Passing / Not verified:** EMAIL-10 can never pass repository-only. Pass requires timestamped live
DNS results plus matching deployed provider/configuration evidence; delivered-message headers with
aligned authentication are stronger corroboration. IaC, docs, packages and provider-domain strings
show intent only. Without live DNS, request exact names/selectors/records and set `Not verified`.

**Current source boundary:** RFCs 9989, 9990 and 9991 were reviewed on 2026-08-26. Use RFC 9989 for
core policy, RFC 9990 for aggregate reports and RFC 9991 for failure reports; reports never replace live DNS evidence.

**Related skill routing:** DNS/domain ownership: owning provider/platform skill.

### `PROVISIONAL-EMAIL-11` — Recovery under delay, replay and provider failure

**Applicability:** Flows where a send is the precondition for a state change (verification pending,
invite pending, password reset queued) or where the provider call fails/times out mid-flow.
Protected property: failures degrade safely, retries never mint duplicate valid credentials.

**Inspect and verify:** Provider calls have timeouts; retry classification bounded (transient
network/5xx retried, 4xx not); queued sends idempotent so a retried job does not issue a fresh token
each attempt; partial flows reconciled (record marked sent only after dispatch succeeds or is
confirmed); provider outage blocks dependent flows explicitly (fail closed) with user-visible
degraded state; revoked sessions/users invalidate outstanding links/codes.

**Unsafe evidence:** Fire-and-forget send treated as success; retry loop regenerates tokens leaving
multiple live credentials; timeout crashes the flow leaving half-created invites; outage silently
skips verification allowing unverified accounts into protected areas; deletion of a user leaves
their outstanding magic links valid.

**Required negative test:** Inject a persistent provider failure in a non-production environment;
dependent flow denies or degrades visibly, no state marks completion. Force one queued job to run
twice; expect one message and one unchanged token.

**Passing / Not verified:** Pass requires bounded/idempotent send-path evidence plus the failure
test. Retry/backoff depth routes to `secod-failure-safety`; never invent provider retry schedules
or delivery guarantees.

**Related skill routing:** Failure-mode depth: `secod-failure-safety`; queue infra: owning platform
skill.

## Exceptional and failure conditions

Fail-closed behavior required where applicable:

- Timeouts and dependency failure: provider unreachable or slow — dependent flows deny or degrade
  explicitly (EMAIL-11); never assume delivery happened.
- Partial operations, cleanup, rollback, reconciliation: invite/verification records reflect actual
  dispatch outcome; aborted sends leave no half-applied state (EMAIL-11); deep rollback belongs to
  `secod-failure-safety`.
- Retry and cancellation: bounded retries only (EMAIL-11); cancelling a flow invalidates its
  outstanding message tokens.
- Session/token revocation: password change, session revoke or account delete invalidates
  outstanding magic links, OTPs and invitations bound to that principal (EMAIL-03, EMAIL-02).
- Webhook duplicate, replay, redelivery and failure: dedupe holds under all four; failed handlers
  signal errors so providers retry rather than lose events (EMAIL-08).

A failed checker or incomplete test never counts as success. Never invent provider retry schedules,
delivery guarantees, expiry defaults, plan availability or regional availability.

## Dependency and routing rules

Direct dependencies copied exactly from `secod/catalog.json`: `secod-core`.

Conditional routes: auth flows delivered by message to `secod-identity-access` (+ auth-provider
adapter); delivery webhooks to `secod-inputs-apis`; send ceilings/quotas to `secod-abuse-limits`;
platform specifics to the owning provider skill.

If an applicable dependency or route is missing, unresolved, malformed or incomplete: mark affected
controls `Not verified`, name the missing owner/evidence, never invent replacement dependencies,
never issue launch readiness.

## Evidence and status rules

Valid statuses only:

- `Do not ship`: account-takeover-grade flaws reachable pre-auth or with a free account — reusable
  or non-expiring magic links/OTPs (EMAIL-03), missing recipient/tenant binding on privileged
  messages (EMAIL-02), unsigned delivery webhooks mutating state (EMAIL-08), client-trusted
  recipients or from-address (EMAIL-01/02).
- `Fix before launch`: control present but bypassable — enumeration distinguishable (EMAIL-04),
  open redirect on redemption (EMAIL-05), GET-consumable tokens (EMAIL-06), HTML/header injection
  reachable (EMAIL-07), no suppression handling on recurring sends (EMAIL-09), missing negative-test
  coverage.
- `Recommended hardening`: DMARC `p=none` without rollout plan (EMAIL-10), missing click-tracking
  monitoring, dev/prod credential separation weaker than per-env scoping, missing degraded-state UX.
- `Passed with evidence`: code-path evidence plus the control's negative test in each applicable
  environment class, and DNS/provider evidence where the control requires it (EMAIL-10).
- `Not verified`: package-only presence, inferred configuration, inaccessible or stale DNS/Dashboard
  state, contradictory sources, unsupported claims, incomplete or failed tests.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported or
failed evidence.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`, `verification`,
`limitations`, `source_refs`, `routed_skills`.

End the report with:

- Applicability inventory (flows x environments, Candidate/Likely/Active)
- Test results including negative tests
- Requested external evidence (DNS records, Dashboard/API items not obtainable repository-only)
- `Not verified` items
- Launch blockers
- A `release_handoff` object with `verdict_owner: secod-ship-check`, `readiness_verdict: not_issued`, control statuses, blockers and requested external evidence

Route overall launch readiness to `secod-ship-check`. `readiness_verdict: not_issued` is an explicit
ownership boundary, not an omitted result. This skill never converts `Not verified` into a launch
verdict and never issues release readiness itself.

## Negative fixtures and tests

Fixture mapping (see `tests/insecure-fixtures/secod-email-messaging/README.md`,
`tests/trigger-cases/secod-email-messaging.md`, `tests/expected-results/secod-email-messaging.md`):

| Fixture case | Controls exercised | Executable? |
| --- | --- | --- |
| Clean app: hashed single-use tokens, allowlisted redirects, signed webhooks, DNS evidence | All pass paths | Documentation-only |
| Reusable/non-expiring magic link, plaintext token storage | EMAIL-03 | Documentation-only |
| Invitation redeemable cross-tenant | EMAIL-02 | Documentation-only |
| Enumeration-distinguishable recovery responses, unbounded resend | EMAIL-04 | Documentation-only |
| Open redirect via `next` on link redemption | EMAIL-05 | Documentation-only |
| GET-consumed token burned by scanner prefetch | EMAIL-06 | Documentation-only |
| User data concatenated into HTML body/subject | EMAIL-07 | Documentation-only |
| Unsigned webhook; duplicate event double-applies | EMAIL-08 | Documentation-only |
| Sends continue after hard bounce | EMAIL-09 | Documentation-only |
| Missing SPF/DKIM/DMARC records | EMAIL-10 | Documentation-only |
| Provider outage silently skips verification; retried job mints new token | EMAIL-11 | Documentation-only |
| Missing-evidence case (integration present, DNS/Dashboard unknown) | All | Documentation-only |

All target fixtures are Markdown plans; none are executable code. Never claim a Markdown fixture
was executed. Safe local probes (template rendering with hostile input, duplicate webhook posts to a
locally started app, read-only DNS queries via `Resolve-DnsName`/`dig`) may run locally or against
an explicitly authorized non-production environment only. Never run destructive,
production-changing, user-creating, payment-creating, refunding, key-rotating, dashboard-changing
or account-changing tests, and never send real messages to third parties, without explicit
authorization.

## References

- Source register: `references/sources.md`.
- Trigger case: `../../tests/trigger-cases/secod-email-messaging.md`; expected result:
  `../../tests/expected-results/secod-email-messaging.md`; fixture plan:
  `../../tests/insecure-fixtures/secod-email-messaging/README.md`.
- Keep direct URLs, version notes and plan/region assumptions in `references/sources.md`.
