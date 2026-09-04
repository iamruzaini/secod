---
name: secod-inputs-apis
description: Inventory and authorize every server and third-party API boundary; validate requests, allowlist responses, prevent injection/SSRF/header-smuggling, fail closed on errors, and enforce provider-capability-aware webhook authenticity with bounded realtime behavior. Triggers include REST/RPC route handlers, GraphQL resolvers, WebSocket endpoints, outbound fetch/HTTP clients to third-party APIs, webhook receiver routes, reverse-proxy/CDN/load-balancer configs, debug/playground/introspection surfaces, and deserialization or path-handling code touching user input; package presence alone is Candidate.
---

# SECOD Inputs APIs Security

## Mission

Prove that every server-reachable API boundary validates untrusted input against explicit schemas, authorizes
its caller at the backend, returns only intended fields, treats third-party responses as untrusted, prevents
injection and SSRF, fails closed under error, and processes webhooks authentically and idempotently.
Repository-only review cannot prove deployed proxy/parser behavior, live debug-surface exposure, provider
webhook retry semantics, or dashboard settings. `secod-ship-check` owns final launch readiness; this skill never
issues it.

## Scope and ownership

Owned controls: API boundary inventory and lifecycle ownership; debug/test/playground surface isolation; request
schema validation and canonicalization; response-field allowlisting and data minimization; third-party response
validation; REST/GraphQL/WebSocket endpoint authorization; GraphQL surface policy; SQL/NoSQL injection
prevention; deserialization and path-traversal safety; HTTP header/CRLF/request-splitting integrity plus desync
review; SSRF, egress allowlists, redirect-target validation and outbound credential stripping; fail-closed
exception handling with redacted errors; webhook authenticity, freshness, dedup, replay protection, idempotency
and bounded retries.

Excluded controls (owned elsewhere): OS-command/template/SSTI/LDAP-filter injection defenses
(`secod-runtime-execution` â€” this skill inventories and routes those execution boundaries but does not verify
them); browser-side XSS/CSP/CORS (`secod-web-app-security`); session/token issuance and revocation
(`secod-identity-access`); rate limits/quotas/idempotency-key abuse economics (`secod-abuse-limits`);
upload/download content validation (`secod-data-files`); secret values in logs/bundles (`secod-secrets-config`);
deep failure semantics/rollback drills (`secod-failure-safety`); payment webhook capability matrices
(`secod-payments-billing` plus adapter); webhook-failure alerting (`secod-observability-response`); verdicts
(`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-runtime-execution` when command/template/LDAP boundaries appear inside inventored
flows; platform adapters (Cloudflare Workers, AWS Lambda/API Gateway, Next.js) when their
runtime owns parser/proxy/handler mechanics for an inventoried
boundary; payment/AI/email adapters when their webhook receivers appear in inventory.

## Required inputs

Repository: route/handler definitions per framework; middleware chains; resolver maps; WebSocket upgrade
handlers; outbound fetch call sites with target construction; webhook receivers and signature-verification code;
schema/validation usage; serialization call sites; path-joining on user input; committed reverse-proxy/CDN/LB
configs; OpenAPI/GraphQL SDL; mock/test route definitions; deprecated or shadow route registrations.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`): deployed route
inventory versus source; live debug/playground reach while signed out; fronting-proxy parsing behavior;
provider webhook retry schedules/redelivery guarantees; third-party contracts at runtime; Dashboard
introspection/schema-publication settings.

Human-supplied evidence: authorized signed-out probes of deployed URLs; proxy/CDN config exports; provider
delivery logs; third-party contract documentation links.

## Applicability and discovery

Always applicable: any application exposing server endpoints or calling third-party APIs.

Signal groups:

- Package/SDK: web frameworks/routers, GraphQL servers, WebSocket libraries (`ws`, socket.io),
HTTP clients (`fetch`, axios), validators (zod/Joi/class-validator), deserializers (pickle/marshal/yaml.load,
`unserialize`).
- Environment variables: names only â€” upstream base URLs, proxy headers, GraphQL enablement
flags, webhook secret names.
- Routes/webhooks: every registered handler including versioned, deprecated, undocumented,
mock/test, playground (GraphiQL/Altair/Swagger UI), health/debug and callback paths.
- Configuration and deployment/provider evidence: proxy/nginx/Envoy configs, CDN rules, body-size
and parser limits, trusted-origin lists; signed-out deployed-URL probes, delivery logs, Management-API exports.

Classification follows `secod-core`: `Candidate` (package/example-variable/dormant route only), `Likely` (code
exists, deployed state unverified), `Active` (repository behavior correlates with
deployed/runtime/Dashboard/Management-API evidence). Keep separate development, preview, staging, production
inventories; conflicting/shared environment signals force affected controls `Not verified`. Reference discovery
uses official `llms.txt`/`llms-full.txt`; conclusions verified against directly linked official documentation,
never the snapshot alone.

## Review workflow

1. Inventory environments and trust boundaries: every host, route class, version, third-party flow
per environment; retirement owners for deprecated surfaces; flag command/template/LDAP-crossing flows for
routing. Parallelizable per environment once inventories exist.
2. Correlate active features and flows: map each route to caller identity source, validation
layer, datastore, outbound calls, exceptional paths. Parallelizable after step 1 completes there.
3. Verify applicable controls below against code plus supplied deployed/proxy evidence.
4. Run safe negative tests: reason through forged-input, oversized-input, cross-tenant,
SSRF-to-private-target, replayed-webhook, malformed-header cases against traced code/config â€” no traffic against
production or third parties without explicit authorization.
5. Classify evidence, emit findings, route execution boundaries to `secod-runtime-execution`,
platform gaps to owning adapters, hand off to `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are `PROVISIONAL-api-N` and
require catalog approval before promotion.

### `PROVISIONAL-api-1` â€” API boundary inventory and lifecycle ownership

**Applicability:** Every server-exposed endpoint, version, and sensitive third-party data flow; protects against
unreviewed or orphaned surfaces.

**Inspect and verify:** Enumerate hosts/environments/routes/methods/versions from router registrations, IaC,
gateway configs; reconcile source against supplied deployed inventory; deprecated/shadow/duplicate routes need
named retirement owner and date; record every third-party flow (destination, fields, sensitivity); mark
command/template/LDAP-crossing flows for routing.

**Unsafe evidence:** Deployed-reachable routes absent from source inventory; deprecated endpoints without
retirement owner; uninventoried third-party data exchange.

**Required negative test:** A documented-nonexistent legacy route reasoned against the router table must show
removed or retained-with-owner; source-versus-deployment diff must be empty or explained.

**Passing / Not verified:** Pass needs reconciled per-environment inventory with owners for every non-current
surface; no supplied export keeps deployed-route truth `Not verified`.

**Related skill routing:** Execution-boundary entries â†’ `secod-runtime-execution`; asset/actor context â†’
`secod-threat-model`; platform route mechanics â†’ hosting adapters.

### `PROVISIONAL-api-2` â€” Debug, test, and playground surface isolation

**Applicability:** Every debug console, profiler, phpinfo-style page, ORM/query studio, API playground
(GraphiQL/Altair/Swagger UI), verbose introspection, test/mock route; protects against unauthenticated
operational access.

**Inspect and verify:** Per surface: build-time exclusion from production bundles or server-enforced privileged
gating; verify from the deployed URL **while signed out** â€” never from source absence alone (dead-code
elimination may not apply); mock/test routes must not register in production bootstrap; verbose/introspection
modes must not be enableable via query param or env flip in production.

**Unsafe evidence:** Signed-out probe reaching GraphiQL/phpinfo/debug console; mock fixtures registered
unconditionally; "hidden path" treated as control.

**Required negative test:** Signed-out request to each enumerated path must return 404/401/403 per traced
policy; enabling-flag attempt via env/query must fail in the production config trace.

**Passing / Not verified:** Pass needs per-surface disposition trace plus supplied signed-out probe results
matching policy; missing probe = `Not verified` even if source looks safe.

**Related skill routing:** Privileged-auth mechanics â†’ `secod-identity-access`; production config gates â†’
`secod-secrets-config`.

### `PROVISIONAL-api-3` â€” Request schema validation and canonicalization

**Applicability:** Every endpoint accepting external input (body, query, headers, path params, multipart);
protects against malformed input reaching logic.

**Inspect and verify:** Explicit server-side schema (zod/Joi/class-validator/Pydantic-class) before business
logic; deliberate unknown-field policy; type/range/length/enum limits on every field including nested arrays and
pagination; canonicalization once, before authorization and storage (Unicode normalization, URL decoding, path
normalization) so duplicate encodings cannot bypass checks; rejections leak nothing about internals.

**Unsafe evidence:** Handlers reading `req.body.*` without parsed schema; client-side-only limits;
decode-after-validation ordering; ad-hoc checks instead of shared schema layer.

**Required negative test:** Oversized string, negative offset, wrong-type field, overlong array must be rejected
before any state access per trace; percent-encoded duplicate key (`%2561dmin`) must resolve identically to
canonical form.

**Passing / Not verified:** Pass needs schema-coverage trace across every inventoried route with limits
evidenced; a route without extractable schema is a finding, not an assumption.

**Related skill routing:** Framework parsing quirks â†’ `secod-nextjs`, hosting adapters; upload content rules â†’
`secod-data-files`.

### `PROVISIONAL-api-4` â€” Response-field allowlists and data minimization

**Applicability:** Every endpoint response including errors and list views; protects against over-returning
internal, cross-tenant, or sensitive fields.

**Inspect and verify:** Responses built via explicit field selection/allowlist or DTO mapping â€” never raw
ORM/model dump; serializers cannot leak internal columns (`password_hash`, tokens, other tenants' rows); error
responses bounded and shape-safe; list pagination server-enforced; mass-assignment blocked on writes via
explicit assignable-field lists.

**Unsafe evidence:** `res.json(dbUser)`/model passthrough; request-body spread into ORM update; stack traces or
SQL fragments in any response class.

**Required negative test:** Traced serializer output for profile and list endpoints must contain only
allowlisted fields; PATCH carrying extra privileged field (`role`, `tenant_id`) must be ignored or rejected by
the traced filter.

**Passing / Not verified:** Pass needs serializer/DTO trace per response class; reflection-based serialization
without enumerable field set stays `Not verified`.

**Related skill routing:** Browser exposure â†’ `secod-web-app-security`; field classification â†’
`secod-crypto-data-protection`.

### `PROVISIONAL-api-5` â€” Third-party response validation as untrusted input

**Applicability:** Every outbound call whose response influences state, rendering, or decisions (payment status,
AI output, SSO metadata, partner feeds); blocks poisoned upstream data.

**Inspect and verify:** Response validated against explicit expected schema before use â€” status checked,
required fields present, types/ranges/lengths enforced; content-type respected; TLS verification never disabled;
size/time bounds set; third-party data entering storage/rendering passes user-input-grade controls; ID/token
values issuer/audience-checked where applicable.

**Unsafe evidence:** Fetch result used as trusted object directly; upstream HTML/JSON rendered or stored
unchecked; certificate-verification disabled; unbounded streaming into memory.

**Required negative test:** Simulated upstream response missing a required field or oversized must be rejected
per trace; mutated upstream value must not reach a state-changing decision without passing schema checks.

**Passing / Not verified:** Pass needs per-integration schema trace plus the applicable third-party contract;
missing contract evidence keeps runtime response guarantees `Not verified`, and contract drift is a documented
limitation monitored via the source register.

**Related skill routing:** AI output handling â†’ `secod-ai-api-integrations`; payment reconciliation â†’
`secod-payments-billing`.

### `PROVISIONAL-api-6` â€” Endpoint authentication and authorization (REST/GraphQL/WebSocket)

**Applicability:** Every REST/RPC route, GraphQL operation, WebSocket upgrade/message; blocks unauthenticated
access and broken object/function-level authorization.

**Inspect and verify:** Every route carries an explicit public/private decision; protected routes verify
credentials server-side (never cookie presence, header existence, referrer); object-level checks bind resource
to principal/tenant on every read/write; function-level checks gate admin/high-impact operations; WebSocket
upgrades authenticate before `upgrade` completes and re-validate scope per message; GraphQL resolvers
individually authorized â€” public root field does not expose nested resolvers.

**Unsafe evidence:** Route groups trusting middleware presence elsewhere without handler verification; WS
messages processed on connect-time identity after privilege change; handlers fetching by raw ID without owner
predicate; admin mutation gated only by UI.

**Required negative test:** Unauthenticated request per private route class denied by traced server-side check;
non-owner requesting another tenant's object ID denied at the data-access predicate; post-revocation message on
a live WebSocket rejected.

**Passing / Not verified:** Pass needs per-route decision table plus object-level predicate traces;
middleware-only evidence leaves those handlers `Not verified`.

**Related skill routing:** Credential/session depth â†’ `secod-identity-access`; rate ceilings â†’
`secod-abuse-limits`; invocation-path authz â†’ hosting adapters.

### `PROVISIONAL-api-7` â€” GraphQL surface policy

**Applicability:** Every GraphQL endpoint (queries, mutations, subscriptions); blocks complexity-based denial of
service and unintended schema disclosure.

**Inspect and verify:** Introspection disabled or explicitly allowed per environment with reason;
schema-publication decision recorded (no accidental SDL serving); server-side depth, breadth/node count, and
complexity limits with tested rejection; persisted queries preferred for production clients; alias batching
bounded; pagination capped; subscription count/size bounded per connection; `PROVISIONAL-api-6` authorization on
every root field.

**Unsafe evidence:** Unlimited introspection in production unjustified; no depth/complexity analysis anywhere;
deeply nested/high-alias queries accepted; client-supplied `limit` passed unbounded to datastore.

**Required negative test:** Deep-nested and high-alias documents rejected before resolver execution per limiter
trace; signed-out introspection to production returns denied/empty per recorded policy.

**Passing / Not verified:** Pass needs limiter configuration trace plus introspection/publication decisions per
environment; claimed-but-unlocatable limiter is `Not verified`.

**Related skill routing:** Schema-design exposure â†’ `secod-threat-model`; datastore rules behind resolvers â†’
database/data-service adapters.

### `PROVISIONAL-api-8` â€” Data-store injection prevention (SQL/NoSQL)

**Applicability:** Every code path constructing a query from any external value; protects stored data from
injection-driven reads/writes.

**Inspect and verify:** All SQL parameterized (prepared statements/ORM bound parameters) â€” never string
concatenation or template interpolation of values; identifiers/keywords from fixed allowlists, never user input;
NoSQL uses typed parameters â€” user objects never spread whole into filters (`$where`, server-evaluated JS
avoided); raw-query escape hatches enumerated and parameterized; dynamic sort/filter keys validated against
column allowlists.

**Unsafe evidence:** Interpolation holes in built SQL; Mongo filters spreading `req.query`; `$where` receiving
external strings; ORDER BY from raw input.

**Required negative test:** Injection payloads reasoned through each raw-query site must remain bound parameters
(inert as syntax); crafted filter (`{"$gt": ""}`) rejected by typed-parameter trace.

**Passing / Not verified:** Pass requires zero unparameterized call sites in the traced query inventory; any raw
site without parameterization proof is `Fix before launch` grade.

**Related skill routing:** OS-command/template/LDAP injection â†’ `secod-runtime-execution` (routed from
inventory); database platform hardening â†’ data-service adapters.

### `PROVISIONAL-api-9` â€” Deserialization and path-traversal safety

**Applicability:** Every deserialization of externally influenced bytes and filesystem/path operation on
external input; blocks code execution and unauthorized file access.

**Inspect and verify:** No native object deserialization on untrusted data (Python `pickle`/`marshal`, PHP
`unserialize`, Java native, Ruby `Marshal`, .NET `BinaryFormatter`); safe formats only (JSON with schema per -3;
YAML safe loaders); paths join a fixed base with sanitized canonical segments then real-path containment
verified â€” traversal and absolute inputs rejected, symlink escape considered; user input never selects modules,
templates, or classes.

**Unsafe evidence:** Pickle-family loads on request/session/cache data from shared stores; `fs.readFile(base +
userInput)` without containment; `__import__`/dynamic loading from request data.

**Required negative test:** `../../etc/passwd` (URL-encoded variants included) through each path site must
resolve outside-base and be rejected; crafted serialized blob refused because format is off the safe list.

**Passing / Not verified:** Pass requires complete deserialization call-site inventory with safe formats plus
path-containment traces; dynamic-loading sites without enumerable name sources stay `Not verified`.

**Related skill routing:** Upload specifics â†’ `secod-data-files`; sandbox/code-eval review â†’
`secod-runtime-execution`.

### `PROVISIONAL-api-10` â€” HTTP header integrity and request-smuggling review

**Applicability:** Every endpoint setting headers from input, and every deployment fronted by a reverse proxy,
CDN, LB, or multiple HTTP parsers; blocks CRLF injection, response splitting, desync.

**Inspect and verify:** Input-derived header values CR/LF-stripped or rejected; raw user input never composes
`Location`, `Set-Cookie`, link headers; hop-by-hop handling matches RFC 9110; with multiple parsers,
Content-Length/Transfer-Encoding conflicts reviewed â€” ambiguous dual-framing rejected, normalization owned by
one identified layer; `X-Forwarded-*` accepted only from configured proxies.

**Unsafe evidence:** Unsanitized `setHeader(userInput)`; redirect header from unvalidated input; known proxy/app
framing divergence unmitigated; app trusting forwarding headers from arbitrary clients.

**Required negative test:** `%0d%0aSet-Cookie:` payload through each input-derived header site stripped/rejected
by trace; dual CL+TE framing rejected at the identified normalizing layer per deployed-chain reasoning.

**Passing / Not verified:** Pass needs header-construction traces plus, for multi-parser deployments, a
documented normalization point; proxy claims without config/export evidence are `Not verified`.

**Related skill routing:** Cache-layer consequences â†’ `secod-web-app-security`; edge mechanics â†’ CDN/hosting
adapters.

### `PROVISIONAL-api-11` â€” SSRF, egress allowlists, and credential stripping

**Applicability:** Every outbound request whose target derives from external influence (webhook delivery, URL
preview/fetch, importers, OAuth/OIDC discovery, media processing); protects internal networks and cloud metadata
endpoints.

**Inspect and verify:** Destination checked against scheme (prefer `https`) and exact-host/prefix allowlist; DNS
pinned, each resolved IP denied against loopback, RFC 1918/private, link-local, cloud-metadata ranges, unusual
ports; redirects resolved manually so every hop repeats validation; size/time/concurrency bounded;
credentials/Authorization/Cookie stripped on cross-origin redirect hops and sent only to their own allowlisted
origin; IPv6/decimal/octal obfuscation normalized.

**Unsafe evidence:** User-supplied URL fetched directly; auto-follow wrappers skipping per-hop checks; metadata
endpoint reachable via import/preview; bearer tokens forwarded across origins.

**Required negative test:** `http://127.0.0.1`, `http://169.254.169.254`, `http://[::1]`, and a DNS-rebinding
hostname refused at the traced layer; redirect chain ending private aborts at that hop; cross-origin redirect
drops credential headers.

**Passing / Not verified:** Pass needs per-fetch-site trace covering scheme, host, IP-range, redirect hops;
runtime rebinding behavior beyond static review is a documented limitation â€” probe evidence else `Not verified`.

**Related skill routing:** Redirect/browser side and WebRTC egress â†’ `secod-web-app-security`; Workers fetch
mechanics â†’ `secod-cloudflare-workers`.

### `PROVISIONAL-api-12` â€” Fail-closed error and exception handling

**Applicability:** Every endpoint's failure path; blocks error-driven disclosure and open-on-failure
authorization.

**Inspect and verify:** Global exception boundary per entrypoint type (handler, worker, queue consumer, cron):
logs internally with secrets/tokens redacted, returns bounded generic response â€” no stack traces, driver errors,
SQL fragments, internal paths; authn/authz helper failures deny by default â€” exception/timeout/dependency error
resolves to refusal, never allowance; security toggles default safe when unreadable; partial operations clean up
or record recoverable state; health endpoints disclose no component detail.

**Unsafe evidence:** Authorization wrapped so errors return success; verbose error mode reachable in production;
raw exception text echoed; entrypoint without any boundary.

**Required negative test:** Simulated dependency exception during an authorization decision resolves to denial
per trace; malformed request hitting an unhandled branch produces the generic shape with no internals.

**Passing / Not verified:** Pass needs boundary trace per entrypoint plus fail-closed ordering (check before
state change); missing boundaries are findings.

**Related skill routing:** Failure semantics/circuit breakers â†’ `secod-failure-safety`; log redaction plumbing â†’
`secod-observability-response`.

### `PROVISIONAL-api-13` â€” Webhook authenticity, replay defense, and idempotency

**Applicability:** Every inbound webhook/callback receiver (payments, email, AI providers, SCIM, partner
callbacks); blocks forged, replayed, reordered, duplicated deliveries driving state.

**Inspect and verify:** Raw body captured pre-parse for signature verification (re-serialization breaks
signatures); provider-documented mechanism and secret â€” constant-time HMAC compare, or asymmetric signature with
pinned algorithm and boot-time JWKS; timestamp/freshness enforced where supplied; event/delivery ID deduplicated
in persistent store keyed for at-least-once providers; where neither signed timestamp nor unique delivery ID
exists, require the adapter-documented compensating strategy â€” never invent retry schedules/guarantees; effects
idempotent; verification failures return promptly without provider detail; slow work deferred to queues within
the provider's documented window; receiver authorization independent of network obscurity.

**Unsafe evidence:** Signature computed over re-parsed body; non-constant-time comparison; no dedup store on
at-least-once providers; state change before verification completes; "unguessable URL" offered as control.

**Required negative test:** Replayed identical delivery acknowledged without repeating the effect per dedup
trace; tampered body with valid original signature fails verification; expired timestamp rejected where
provided.

**Passing / Not verified:** Pass needs per-provider verification trace plus dedup/idempotency mechanism
evidence; retry/redelivery guarantees and other capability claims need the adapter's capability matrix â€” absent
official evidence routes there and stays `Not verified` here.

**Related skill routing:** Payment matrices/reconciliation â†’ `secod-payments-billing` plus adapters; failure
alerting â†’ `secod-observability-response`; duplicate-abuse economics â†’ `secod-abuse-limits`.

## Exceptional and failure conditions

- Verification dependency unavailable (signature service, JWKS, dedup store down): processing
fails closed â€” refuse or defer, never accept unverified.
- Partial webhook processing: persist idempotency/event state before external effects so retries
converge; unrecoverable halves go to dead-letter with operator playbook (routed to `secod-failure-safety`).
- Retry/cancellation: only idempotent operations auto-retry; cancellation propagates before
irreversible side effects; bounded attempts, backoff for transient classes only.
- Credential revocation mid-flight: cached authorizations invalidated or short-lived enough that
revoked callers lose access within the documented bound; long-lived WS/stream connections re-checked per message
for high-impact actions.
- Webhook duplicates/out-of-order/redelivery: dedup keys plus monotonic/state-version checks where
ordering matters; acknowledged-but-failed deliveries reconciled via provider retrieval where supported. Never
invent provider retry schedules, redelivery windows, or guarantees â€” cite the routed adapter's registered
documentation or leave `Not verified`.
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-runtime-execution` (command/template/LDAP boundaries found during inventory);
platform/runtime adapters owning parser or handler mechanics for inventoried boundaries (`secod-nextjs`,
Cloudflare Workers/Pages, AWS Lambda/API Gateway);
provider webhook receivers â†’ their adapters (`secod-payments-billing` family, `secod-email-messaging`, AI
adapters).

If `secod-core` is missing/unresolved/malformed/incomplete: affected inventory-dependent controls become `Not
verified`, missing owner named, inventories never reconstructed here, no launch readiness issued. A routed owner
that cannot be invoked leaves its verification share `Not verified` with the owner named â€” never silently
dropped.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`, `Not verified`.
Thresholds:

- `Passed with evidence`: reconciled per-environment boundary inventory; schema/authorization/
serializer traces complete per applicable control; SSRF and webhook traces complete; supplied deployed/probe
evidence matches intent.
- `Fix before launch`: exploitable injection/deserialization site; SSRF-reachable internal target;
unsigned webhook driving state change; authorization failing open; debug surface reachable signed out; responses
exposing secrets or cross-tenant data.
- `Recommended hardening`: limits present but tunable; missing freshness window on timestamp-
capable providers; redirect resolution improvable to stricter allowlists.
- `Not verified`: deployed-route truth, live probes, proxy parser behavior, provider guarantees,
or third-party contracts without supplied evidence â€” each with exact artifact needed.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported, or failed
evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`, `impact`,
`recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`. End with: applicability
inventory (boundaries Ã— environment, third-party flows, execution-boundary routing flags); test results;
requested external evidence (signed-out probes, proxy exports, delivery logs â€” by owner); `Not verified` items
with next step; launch blockers. Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

All fixtures are documentation-only plans; none execute code locally.

| Fixture | Type | Controls |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-inputs-apis/README.md` | Documentation-only plan | All |
| Clean baseline: validated, allowlisted, signed-webhook API | Documentation-only case | -3, -4, -6, -13 |
| Shadow debug route reachable signed out; mass-assignment PATCH; cross-tenant raw-ID read | Documentation-only case | -1/-2, -3/-4, -6 |
| Deep aliased GraphQL query + unlimited introspection; concatenated SQL + `$where`; pickle blob + `../..` escape | Documentation-only case | -7, -8, -9 |
| CRLF-injected header + CL/TE smuggling past proxy; URL-preview fetching metadata via redirect hop | Documentation-only case | -10, -11 |
| Authorization-helper exception allowing access; replayed webhook without dedup, signature on re-parsed body | Documentation-only case | -12, -13 |
| Missing-evidence case: no deployment export, probe, or delivery log | Documentation-only case | All |

Reasoning-based verification only. Never claim Markdown fixture plans executed as code. Never run destructive,
production-changing, user-creating, payment-creating, refunding, key-rotating, dashboard-changing, or
account-changing tests without explicit authorization.

## References

- [`references/sources.md`](references/sources.md) â€” source register: OWASP API Security Top 10 2023, OWASP
ASVS 5.0.0, OWASP SSRF and Injection Prevention cheat sheets, GraphQL security guidance, RFC 9110, RFC 6455.
