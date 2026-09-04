# Source register: secod-web-app-security

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | MDN: Content Security Policy implementation guide (strict CSP, nonces vs hashes, strict-dynamic, report-to preference, unsafe-inline pitfalls) | https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/CSP | Mozilla | 2026-08-24 (page dated 2026-08-15) | Refresh on guide revision | Reviewed | PROVISIONAL-web-3 |
| S2 | MDN: CSP script-src directive (nonce/hash sources, strict-dynamic semantics, backwards-compatible fallback chains) | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src | Mozilla | 2026-08-24 (page dated 2026-08-12) | Refresh on reference revision | Reviewed | PROVISIONAL-web-3 |
| S3 | web.dev: Mitigate XSS with a strict Content Security Policy (nonce requirements 128+ bits, hash-based static variant, Report-Only rollout) | https://web.dev/articles/strict-csp | Google | 2026-08-24 | Refresh on article revision | Reviewed | PROVISIONAL-web-3 |
| S4 | RFC 10017: OAuth 2.0 for Browser-Based Applications BCP (token storage analysis; no credentials in web storage; BFF pattern) | https://www.rfc-editor.org/info/rfc10017 | IETF OAuth WG | 2026-08-24 | Refresh on errata/update affecting storage sections | Reviewed | PROVISIONAL-web-7 |

Community-layered-policy discussion (SRI + Trusted Types support matrices) consulted during
research but not retained as a source: browser support for `require-trusted-types-for` remains
Chromium-led per MDN/SRI tables — treat Trusted Types as hardening layer with documented
coverage, never sole control. Provider-specific header/cache mechanics are registered in each
routed platform adapter's own register.
