---
name: secod-web-app-security
description: Treat all browser-rendered and cross-origin content as untrusted; enforce browser boundaries — XSS prevention, strict CSP with nonce/hash discipline, Trusted Types, sanitization, SRI, clickjacking/iframe/postMessage isolation, CSRF/CORS/cookie flags, token isolation from client code, cache and header trust boundaries, service-worker integrity, source-map decisions — independently of UI visibility. Triggers include any browser-rendered route, iframe/embed usage, third-party script tag, cookie/session handling in client code, postMessage handlers, service workers, and source-map configuration; package presence alone is Candidate.
---

# SECOD Web App Security

## Mission

Prove that every browser-facing surface enforces its boundaries at the HTTP/browser layer — not
through UI visibility or client-side checks — so that injected content, cross-origin pages, and
malicious frames cannot execute code, steal credentials, or reach private data.

Repository-only review cannot prove deployed response headers, CDN/cache behavior, real
third-party script contents at runtime, browser-enforcement coverage across actual traffic, or
that report endpoints receive violations. `secod-ship-check` owns final launch readiness; this
skill never issues it.

## Scope and ownership

Owned controls: contextual XSS prevention and output encoding; HTML sanitization of allowed
markup; strict CSP construction including nonce/hash discipline, Trusted Types where supported,
report endpoint and report-data redaction; third-party-script review and SRI; clickjacking/
frame-ancestors, iframe sandboxing, postMessage validation, link `noopener`; CSRF defenses,
secure cookie flags, CORS allowlists; browser-storage hygiene and raw-bearer-token isolation
from user-authored code/untrusted frames/plugins/client RPC; cache controls, cache-key
confusion/poisoning review, shared-cache exclusion of personalized responses; host/forwarded-
header trust boundaries with canonical origin allowlists; service-worker scope/update/integrity;
source-map inventory plus explicit publication decision; DOM clobbering and prototype-pollution
source/sink review; CSS/URL/redirect/navigation injection prevention; WebRTC/STUN/TURN egress
containment-or-acceptance decision.

Excluded controls (owned elsewhere): server-side injection/SSRF/webhook authenticity
(`secod-inputs-apis`); command/template/code-injection execution (`secod-runtime-execution`);
session issuance/revocation logic (`secod-identity-access`); secret values in bundles
(`secod-secrets-config`); file download/upload content handling (`secod-data-files`);
CDN/provider platform headers (`secod-vercel-platform`, Cloudflare/AWS/GCP routers);
launch verdicts (`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-nextjs` when Next.js detected (framework-level header/script
mechanics); hosting/platform adapters when their edge config carries headers/caches; provider
adapters whose embedded widgets/iframes appear on pages.

## Required inputs

Repository: rendered templates/components and their data interpolation points; any
`dangerouslySetInnerHTML`/`v-html`/`innerHTML` sinks; CSP/meta/header middleware; cookie-setting
code; CORS configuration; iframe/embed markup; `postMessage` handlers; service-worker files;
source-map generation settings; redirect/navigation logic; cache headers per route class;
WebRTC usage.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
deployed response headers per environment/route class; CDN/cache-tier effective behavior;
runtime third-party script contents and subresource integrity outcomes; CSP violation reports;
real-browser enforcement results; production source-map presence.

Human-supplied evidence: authorized curl/header captures from deployed URLs per environment;
CDN dashboard cache-rule exports; CSP report summaries; WebRTC TURN policy documents.

## Applicability and discovery

Always applicable: every application rendering HTML in a browser.

Signal groups:

- Package/SDK: sanitizer libraries (DOMPurify-class), CSP middleware (helmet-class), WebRTC
  SDKs, analytics/tag-manager loaders.
- Environment variables: names for CSP report URLs, canonical origins, cookie domains.
- Routes/webhooks: CSP report-only/enforce endpoints, embed/callback pages, share/preview
  routes rendered for unauthenticated visitors.
- Configuration: next.config/proxy-middleware header blocks, meta CSP tags, `_headers`
  files, vercel.json/wrangler header rules, service-worker registration.
- Deployment/provider evidence: live headers, generated preview URLs, CDN behavior.

Classification follows `secod-core`: `Candidate`, `Likely`, `Active` per corroboration depth.
Maintain separate development/preview/staging/production inventories — header and cache policies
routinely differ per environment; conflicting or merged signals keep affected controls `Not
verified`.

## Review workflow

1. Inventory environments and trust boundaries: which routes render what, for whom, through
   which caches/CDNs; where unauthenticated visitors meet authenticated fragments.
   Parallelizable per environment once inventories exist.
2. Correlate active flows: sinks, embeds, postMessage pairs, worker scopes, redirect targets,
   personalized cached routes. Parallelizable after step 1 completes there.
3. Verify applicable controls below against code plus supplied deployed evidence.
4. Run safe negative tests: reason through sink-injection, frame-embedding, postMessage-forgery,
   cache-poisoning cases against the traced code/config. No traffic against real users.
5. Classify evidence, emit findings, route platform-specific gaps to owning skills, hand off to
   `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-web-N` and require catalog approval before promotion.

### `PROVISIONAL-web-1` — Contextual XSS prevention and safe rendering

**Applicability:** Every template/component interpolating data into HTML, attributes, JS,
CSS, or URL contexts. Protects against script/markup injection.

**Inspect and verify:** Framework auto-escaping relied upon deliberately (list escape-on by
default frameworks); every bypass sink enumerated — `dangerouslySetInnerHTML`, `v-html`,
`innerHTML`, `outerHTML`, `document.write`, `insertAdjacentHTML`, `eval`, `new Function`,
`setAttribute('href'/'src', ...)` with user data; attribute-context values quoted and encoded;
URL-context values scheme-checked (`http(s)` only — block `javascript:`/`data:`); JS-context
values serialized via JSON, never string-concatenated; CSS-context values validated against
grammars.

**Unsafe evidence:** User-controlled strings flowing into any enumerated sink without sanitizer;
`javascript:` URLs accepted from input; template engines with autoescape disabled without
justification.

**Required negative test:** Payload `<img src=x onerror=alert(1)>` traced through each sink path
must render inert (encoded/removed); `javascript:alert(1)` submitted as profile URL must be
rejected at write time.

**Passing / Not verified:** Pass requires sink inventory reconciled against code with each sink
either removed, sanitized, or justified. Untraceable dynamic-sink data flow keeps that path
`Not verified`.

**Related skill routing:** Server-side injection → `secod-inputs-apis`; evaluation sinks →
`secod-runtime-execution`; framework specifics → `secod-nextjs`.

### `PROVISIONAL-web-2` — HTML sanitization for allowed markup

**Applicability:** Any feature permitting rich/user HTML (comments, bios, email templates
rendered client-side).

**Inspect and verify:** Sanitizer is maintained library (DOMPurify-class) configured with
explicit tag/attribute allowlists; dangerous elements (`script`, `iframe`, `object`, `embed`,
`form`, `meta`) and event-handler attributes stripped; URI attributes scheme-filtered; sanitizer
runs in parsing context equal to rendering context; mXSS-relevant configs reviewed (SVG/MathML
namespaces); sanitizer version tracked with advisory monitoring.

**Unsafe evidence:** Regex-based "sanitization"; allowlists including event handlers or
`javascript:` URIs; sanitize-on-read skipped because "wrote it clean" without proof.

**Required negative test:** Known filter-evasion payload set (mutation-XSS classics) run through
the configured policy must yield inert output; `<svg><script>` variants must be stripped.

**Passing / Not verified:** Not applicable — pass requires policy config evidence plus version
currency; stale sanitizer versions with known advisories are `Fix before launch` via
`secod-vulnerability-management`.

**Related skill routing:** `secod-vulnerability-management` (library advisories),
`secod-ai-api-integrations` (model-output rendering must pass here too).

### `PROVISIONAL-web-3` — Strict Content-Security-Policy

**Applicability:** Every HTML response. Protects against injected-script execution regardless
of sink gaps.

**Inspect and verify:** Policy delivered via HTTP header (not meta alone); `script-src` built on
per-request CSPRNG nonces (128+ bits, never reused, response marked uncacheable) or build-time
hashes for static content; `'strict-dynamic'` present with documented fallback chain
(`https:` / `'unsafe-inline'` ignored by modern engines when nonce/hash present);
`object-src 'none'`; `base-uri 'none'`; no broad host allowlists doing the authorization work;
`require-trusted-types-for 'script'` with named `trusted-types` policy adopted where Chromium-
dominated audience permits, else report-only rollout documented; report endpoint exists, is
rate-limited, authenticatable, and redacts report bodies (never logs full violating snippets
containing user data); Report-Only phase evidence before enforcement changes.

**Unsafe evidence:** `'unsafe-inline'` carrying authorization in modern-engine traffic;
host-allowlist-only policy presented as XSS mitigation; nonce reused across responses or applied
to cacheable pages; missing `object-src`/`base-uri`.

**Required negative test:** Injected inline `<script>` without nonce must not execute under
traced policy semantics; `document.createElement('script')` with attacker URL must fail under
Trusted Types where enforced.

**Passing / Not verified:** Pass requires header construction trace plus supplied live-header
capture matching intent. Deployed header state without capture stays `Not verified`.

**Related skill routing:** Platform header mechanics → `secod-nextjs`, `secod-vercel-platform`,
edge routers; violation-report plumbing → `secod-observability-response`.

### `PROVISIONAL-web-4` — Third-party scripts and subresource integrity

**Applicability:** Every externally loaded script/style. Protects against supply-chain
execution on pages.

**Inspect and verify:** Inventory every third-party origin with business owner and purpose;
`integrity` attribute (sha384+) plus `crossorigin` on static-versioned resources; dynamic-API
scripts (maps/chat widgets) reviewed for version pinning or documented vendor-integrity gap;
loader scripts from tag managers treated as full-page-code-trust decisions requiring named
approval; `'strict-dynamic'` propagation understood — integrity never inherited, loader must set
it; third-party changes monitored (build-time lint failing when cross-origin `<script>` lacks
`integrity` where SRI applies).

**Unsafe evidence:** Uninventoried analytics/marketing tags; `document.write`-based embeds;
version-floating vendor loaders on authenticated pages without acceptance record.

**Required negative test:** Modified external file (hash mismatch) must be blocked by browser —
verify `integrity` present and correct in traced markup.

**Passing / Not verified:** Pass requires complete origin inventory with trust decisions.
Runtime contents of third parties are unverifiable — residual risk documented, not resolved.

**Related skill routing:** `secod-packages-delivery` (dependency-side supply chain),
`secod-threat-model` (third-party flow records).

### `PROVISIONAL-web-5` — Clickjacking, iframe isolation, postMessage

**Applicability:** Every HTML response and every embedded/embedding surface.

**Inspect and verify:** `frame-ancestors` (CSP) set per route class — deny-all for non-embedding
pages, explicit allowlist for intentional embeds; legacy `X-Frame-Options: DENY/SAMEORIGIN`
where older clients matter; embedded iframes carry `sandbox` with minimal tokens (no
`allow-scripts allow-same-origin` together with cross-origin content); `postMessage` handlers
validate `event.origin` against exact allowlists, validate `source`, schema-check payload before
use, never act on wildcard-origin messages; outbound `postMessage` targets explicit windows with
exact origins; all user-content/target links carry `rel="noopener noreferrer"`.

**Unsafe evidence:** `frame-ancestors *` or missing frame protection on sensitive routes;
`event.data` used without origin check; `target="_blank"` without `noopener`.

**Required negative test:** Framing the account-settings URL from an attacker origin must be
blocked by traced policy; forged postMessage from wrong origin must be ignored by handler.

**Passing / Not verified:** Pass requires per-route-class frame policy trace plus handler code
evidence. Deployed header confirmation needs live captures else `Not verified`.

**Related skill routing:** Payment/AI provider iframes → their adapters' widget guidance;
`secod-identity-access` for token-bearing frames.

### `PROVISIONAL-web-6` — CSRF, cookie flags, CORS

**Applicability:** Every cookie-authenticated state change and cross-origin API surface.

**Inspect and verify:** State-changing requests protected by framework CSRF tokens or
SameSite=Strict/Lax cookies with method+origin verification — defense layered, SameSite not sole
control for top-level-navigation-reachable flows; session cookies `HttpOnly`, `Secure`,
explicit `SameSite`, `__Host-` prefix where path/domain semantics allow; CORS responses reflect
exact allowlisted origins only — no wildcard combined with credentials, no request-derived Origin
echoing; preflight caches bounded; credential-bearing cross-origin reads enumerated deliberately.

**Unsafe evidence:** `Access-Control-Allow-Origin: *` with `credentials: include`;
origin echoed from request without allowlist check; CSRF token absent on cookie-authenticated
POST/PUT/DELETE; `SameSite=None` without `Secure`.

**Required negative test:** Cross-site form POST to funds-transfer endpoint must fail CSRF
validation; credentialed fetch from attacker origin must be denied by CORS while legitimate
origin passes.

**Passing / Not verified:** Pass requires middleware/config trace plus deployed-header capture.
Browser-enforcement nuances documented as defense-in-depth, never sole control.

**Related skill routing:** Session mechanics → `secod-identity-access`; platform edge behavior →
hosting adapters.

### `PROVISIONAL-web-7` — Browser storage and bearer-token isolation

**Applicability:** Any client-side storage use and any token/capability crossing into browser
code.

**Inspect and verify:** No authentication tokens, JWTs, refresh tokens, raw share-link verifiers,
or capability bearers in localStorage/sessionStorage/IndexedDB/non-HttpOnly cookies — XSS single-
point-extraction rule per OWASP session guidance and RFC 10017; tokens reach only HttpOnly
cookies or BFF-mediated flows; IndexedDB/localStorage contents inventoried with data-class
justification; sensitive PII minimized in persistent storage; caches holding personalized data
cleared on logout where applicable.

**Unsafe evidence:** `localStorage.setItem('token', ...)` anywhere; refresh token reachable by
page JavaScript; full user profile cached persistently without justification.

**Required negative test:** Simulated XSS payload enumerating storage APIs must find no usable
credential material; logout must clear persisted personalization data.

**Passing / Not verified:** Pass requires storage-inventory trace across bundle code. Runtime
extension/plugin access out of scope — documented limitation.

**Related skill routing:** `secod-identity-access` (token design), `secod-crypto-data-protection`
(retention), provider adapters for their SDK storage patterns.

### `PROVISIONAL-web-8` — Cache controls, host-header and forwarded-header boundaries

**Applicability:** Every cacheable response class and any proxy/CDN fronted deployment.

**Inspect and verify:** Personalized/authenticated responses excluded from shared caches via
explicit `Cache-Control: private, no-store` (not relying on absence of caching headers); CSP-
nonced responses uncacheable; cache-key composition reviewed against header/cookie confusion —
unkeyed headers influencing content (`X-Forwarded-*`, Accept-Language) flagged for poisoning/
web-cache-deception review; host/header trust boundary enforced server-side: canonical origin
allowlist decides self-references (password-reset links, redirects), never raw `Host`/
`X-Forwarded-Host`; forwarding proxies stripped/validated at trust edge.

**Unsafe evidence:** Reset emails built from `Host` header; authenticated JSON cached by CDN due
to missing `private` directive; application trusting `X-Forwarded-For` for authz decisions
without trusted-proxy validation.

**Required negative test:** Request with attacker `Host` driving password-reset link generation
must yield canonical-host link or rejection; authenticated response fetched through shared-cache
path must miss.

**Passing / Not verified:** Pass requires per-route-class cache directive inventory plus
canonical-origin resolution trace. Live CDN behavior needs supplied evidence/dashboards else
`Not verified`.

**Related skill routing:** Platform caches → hosting adapters; `secod-inputs-apis` (request
smuggling adjacent review).

### `PROVISIONAL-web-9` — Service workers

**Applicability:** Any registered service worker / offline-first layer.

**Inspect and verify:** Scope minimal (subdirectory, not root-by-default); registration/update
flow uses byte-compare updates with safe activation (`skipWaiting` deliberate); fetch-handler
never serves stale authenticated content to new users nor caches personalized responses in
shared caches; worker code versioned/hashed with update integrity; kill-switch path documented;
cache-storage entries inventoried with eviction.

**Unsafe evidence:** Root-scope worker caching everything including `/api/*` personalized
responses; update flow that can serve indefinitely-stale code; no uninstall/kill procedure.

**Required negative test:** Authenticated response stored by worker must not be served to a
different subsequent user on shared machine; forced update must replace worker within one reload
cycle.

**Passing / Not verified:** Pass requires scope/fetch-handler/cache-strategy code trace.
Deployed update behavior needs runtime evidence else `Not verified`.

**Related skill routing:** `secod-data-files` (cached object sensitivity), hosting adapters for
worker-file serving.

### `PROVISIONAL-web-10` — Source maps, prototype pollution, navigation injection, WebRTC egress

**Applicability:** Build output publishing, client JS sink hygiene, redirect/navigation logic,
WebRTC usage. Protects IP/source disclosure, client-side gadget chains, open-redirect phishing,
and covert network egress.

**Inspect and verify:** Source maps: production build decision explicit — published maps
inventory-listed with justification, or generation disabled/servers-blocked (`*.map` 403) and
verified from deployed URL; DOM clobbering sources (global-reaching ids/names) reviewed against
gadget-prone library sinks; prototype-pollution entry points (recursive merge, query-param
parsers) audited with `__proto__`/`constructor.prototype` hardening; CSS injection contexts
bounded; redirects/navigation targets validated against canonical-origin allowlist — no
request-derived full URLs; WebRTC/STUN/TURN identified as network-egress paths — either
contained (TURN allowlists, ICE candidate policies) and tested, or explicitly documented and
accepted with residual-risk owner recorded.

**Unsafe evidence:** `.map` files reachable in production unnoticed; `?next=` redirect accepted
verbatim; merge helper recursing user objects into internals; TURN server open-relay assumed
safe without test.

**Required negative test:** `https://site.example?next=https://evil.example` must be rejected or
sanitized to relative path; `?a[__proto__][x]=y` pollution probe must not alter Object prototype;
deployed `app.js.map` request must 404 when publication is declined.

**Passing / Not verified:** Pass requires build-config evidence plus deployed-URL checks where
supplied. Prototype-gadget exploitability depth beyond source review routed onward.

**Related skill routing:** `secod-packages-delivery` (build artifacts), `secod-threat-model`
(WebRTC egress acceptance), `secod-inputs-apis` (redirect target validation server-side).

## Exceptional and failure conditions

- CSP report endpoint unavailable/failing: enforcement rollout pauses; violations unseen is a
  blind spot, not safety — treat as `Not verified` visibility.
- Header middleware bypassed on error pages/static routes: inventory must cover every response
  class including errors; uncovered classes are findings, not exceptions.
- Sanitizer/parser version skew between write-time and render-time contexts: normalize to one
  context or sanitize at read; mismatched dual-sanitization is mXSS risk.
- CDN/platform strips or rewrites security headers: platform adapter must supply evidence of
  effective final headers; assumption of passthrough is `Not verified`.
- Service-worker update failure loops: kill-switch must remain functional; stuck-stale-worker
  state is a finding.
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-nextjs` (framework header/script mechanics), hosting/platform adapters
when edge config carries headers/caches (`secod-vercel-platform`, Cloudflare Pages/Workers,
AWS S3/CloudFront, Google Cloud Storage/web), provider adapters whose embedded widgets
appear on pages.

If `secod-core` is missing/unresolved/malformed: mark inventory-dependent controls `Not
verified`, name the missing owner, never reconstruct inventories, never issue launch readiness.
Platform-header questions unresolved by repository stay `Not verified` pending adapter-supplied
live captures.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: sink inventory reconciled; strict-CSP construction traced; frame/
  postMessage/CSRF/CORS traces complete; storage free of credential material; cache directives
  per route class; source-map decision executed; supplied deployed-header captures match intent.
- `Fix before launch`: exploitable sink without sanitizer/CSP coverage; wildcard CORS with
  credentials; missing frame protection on sensitive routes; bearer tokens in web storage;
  personalized responses entering shared caches; reachable production source maps with secrets.
- `Recommended hardening`: Trusted Types report-only not yet enforcing; legacy `X-Frame-Options`
  gaps; incomplete `noopener` coverage; non-root worker scopes improvable.
- `Not verified`: deployed headers/caches/runtime third-party contents/report delivery without
  supplied captures — each with exact evidence needed.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (route classes × environment, sinks, embeds,
workers); test results; requested external evidence (live-header captures, CDN rule exports, CSP
report summaries, by owner); `Not verified` items with next verification step; launch blockers.
Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; none execute code locally.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-web-app-security/README.md` | Documentation-only plan | All controls |
| Comment field rendering via `innerHTML` | Documentation-only case | -1 |
| Filter-evasion payload surviving regex sanitizer | Documentation-only case | -2 |
| Host-allowlist-only CSP claimed as XSS fix | Documentation-only case | -3 |
| Nonce reused on cached page | Documentation-only case | -3 |
| Unversioned tag-manager loader on authed page | Documentation-only case | -4 |
| Account page framed cross-origin; forged postMessage accepted | Documentation-only case | -5 |
| Wildcard CORS with credentials | Documentation-only case | -6 |
| JWT readable in localStorage after simulated XSS | Documentation-only case | -7 |
| Reset link built from attacker Host header | Documentation-only case | -8 |
| Worker serving stale authed content cross-user | Documentation-only case | -9 |
| Reachable prod `.map`; `?next=` open redirect; `__proto__` pollution probe | Documentation-only case | -10 |

Reasoning-based verification only. Never claim Markdown fixture plans executed as code. Never
run destructive, production-changing, user-creating, payment-creating, refunding, key-rotating,
dashboard-changing, or account-changing tests without explicit authorization.

## References

- [`references/sources.md`](references/sources.md) — source register: MDN CSP implementation guide, MDN
  script-src/strict-dynamic reference, web.dev strict-CSP guidance, RFC 10017 browser-token
  storage rules.
