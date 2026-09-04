# Source register: secod-auth-provider-integrations

Use official documentation indexes (`llms.txt` / `llms-full.txt` where published) for discovery
only. Verify security-critical claims against the direct primary source and refresh this
register before its review-expiry date.

Documentation-index exports are discovery artifacts, not proof of current provider behavior.
Any claim that depends on current provider behavior requires live direct-source confirmation
or the affected control stays `Not verified`.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Version / assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP Foundation | 2026-08-26 | 2026-11-26 or on cheat-sheet revision | Reviewed | -03, -05, -07, -10 | Live direct page; authentication, session and reauthentication guidance; no page version exposed |
| S2 | OWASP Multifactor Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | OWASP Foundation | 2026-08-26 | 2026-11-26 or on cheat-sheet revision | Reviewed | -08, -10 | Live direct page; MFA lifecycle, recovery and factor-change guidance; no page version exposed |
| S3 | OWASP OAuth 2.0 Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html | OWASP Foundation | 2026-08-26 | 2026-11-26 or on cheat-sheet revision | Reviewed | -04, -05, -06 | Live direct page; token audience, Authorization Code + PKCE, state/nonce and refresh-token guidance |
| S4 | RFC 9700: Best Current Practice for OAuth 2.0 Security | https://www.rfc-editor.org/rfc/rfc9700.html | IETF OAuth WG | 2026-08-26 | 2027-08-26 or on RFC errata/update | Reviewed | -05, -06 | RFC 9700 / BCP 240, January 2025; exact redirect matching, PKCE and replay protections |
| S5 | W3C WebAuthn Level 3 specification | https://www.w3.org/TR/2026/REC-webauthn-3-20260825/ | W3C | 2026-08-26 | 2027-08-26 or on errata/new Recommendation | Reviewed | -10 | W3C Recommendation, 2026-08-25; immutable dated version retained |
| P1 | Clerk documentation index (`llms.txt`) and full export | https://clerk.com/docs/llms.txt ; https://clerk.com/docs/llms-full.txt | Clerk | 2026-08-26 | Local snapshot drift check each review; live re-check on provider docs change | Reviewed (snapshot) | -01 | Discovery only; exact Clerk SDK versions recorded per review |
| P2 | Auth0 top-level and docs indexes (`llms.txt`) | https://auth0.com/llms.txt ; https://auth0.com/docs/llms.txt | Okta / Auth0 | 2026-08-26 | Local snapshot drift check each review; live re-check on provider docs change | Reviewed (snapshot) | -01 | Discovery only; tenant region/plan assumptions recorded per review |
| P3 | WorkOS documentation index (`llms.txt`) and full export | https://workos.com/docs/llms.txt ; https://workos.com/docs/llms-full.txt | WorkOS Inc. | 2026-08-26 | Local snapshot drift check each review; live re-check on provider docs change | Reviewed (snapshot) | -01, -02, -11 | Discovery only; staging/production environment split assumed |
| P4 | Better Auth documentation index (`llms.txt`) | https://better-auth.com/llms.txt | Better Auth project | 2026-08-26 | Local index drift check each review | Reviewed (snapshot) | -01 | Full export returned `404 Not Found` when checked 2026-08-16 (PRD); direct pages substitute |
| P5 | Supabase documentation index and full export | https://supabase.com/llms.txt ; https://supabase.com/llms-full.txt | Supabase | 2026-08-26 | Local snapshot drift check each review; live re-check on provider docs change | Reviewed (snapshot) | -01, -09 | Discovery only; plan/region assumptions recorded per review |
| D1 | Better Auth — Security reference (trustedOrigins, disableCSRFCheck/disableOriginCheck, cookie defaults, state/PKCE storage) | https://www.better-auth.com/docs/reference/security | Better Auth project | 2026-08-26 | Re-fetch on version bump past v1.7 or on option changes | Reviewed | -01, -06, -07, -10 | v1.7 (Latest) at fetch time |
| D2 | Better Auth — Options reference | https://better-auth.com/docs/reference/options | Better Auth project | 2026-08-26 | 2026-11-26 or on Better Auth version/option change | Reviewed | -06, -07 | Live direct page; explicit `baseURL`, `trustedOrigins`, secure-cookie and CSRF/origin-check options; match exact installed version |
| D3 | Better Auth — Session management | https://better-auth.com/docs/concepts/session-management | Better Auth project | 2026-08-26 | 2026-11-26 or on Better Auth session-model change | Reviewed | -08 | Live direct page; database-backed session token, expiry/`updateAge`, listing and revocation behavior; deployed settings remain required |
| D4 | Better Auth — SSO plugin | https://better-auth.com/docs/plugins/sso | Better Auth project | 2026-08-26 | 2026-11-26 or on SSO-plugin/version change | Reviewed | -03, -09 | Live direct page; issuer/sub identity, discovery-origin allowlisting and domain-driven linking/organization behavior |
| D5 | Clerk — Manual JWT verification | https://clerk.com/docs/guides/sessions/manual-jwt-verification | Clerk | 2026-08-26 | 2026-11-26 or on Clerk SDK/JWT guidance change | Reviewed | -03 | Live direct page; instance public key/JWKS, signature/time and `azp`/`authorizedParties` checks; deployed issuer/key state remains required |
| D6 | Clerk — Account linking | https://clerk.com/docs/guides/configure/auth-strategies/social-connections/account-linking | Clerk | 2026-08-26 | 2026-11-26 or on Clerk linking-policy change | Reviewed | -10 | Live direct page; automatic same-email linking and unverified-email safeguards documented; application policy must still satisfy control -10 |
| D7 | Clerk — Session options | https://clerk.com/docs/guides/secure/session-options | Clerk | 2026-08-26 | 2026-11-26 or on Clerk session-setting/plan change | Reviewed | -08 | Live direct page; Dashboard inactivity timeout and maximum lifetime documented; current instance values remain required |
| D8 | Auth0 — Token best practices | https://auth0.com/docs/secure/tokens/token-best-practices | Okta / Auth0 | 2026-08-26 | 2026-11-26 or on Auth0 token guidance change | Reviewed | -03, -04 | Live direct page; token storage, validation, signing and lifetime guidance; tenant/API settings remain required |
| D9 | Auth0 — JSON Web Key Sets handling | https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-sets | Okta / Auth0 | 2026-08-26 | 2026-11-26 or on Auth0 JWKS/rotation guidance change | Reviewed | -03 | Live direct page; JWKS caching, unknown-`kid` refresh and refetch rate limiting documented |
| D10 | Auth0 — Refresh token security | https://auth0.com/docs/secure/tokens/refresh-tokens | Okta / Auth0 | 2026-08-26 | 2026-11-26 or on Auth0 refresh-token policy change | Reviewed | -08 | Live direct page; secure storage, rotation, denylisting and active-token limits documented; tenant settings remain required |
| D11 | Auth0 — Redirect users after login (callback allowlists) | https://auth0.com/docs/authenticate/login/redirect-users-after-login | Okta / Auth0 | 2026-08-26 | 2026-11-26 or on Auth0 redirect guidance change | Reviewed | -06 | Live direct page; Allowed Callback URLs and random validated `state` documented; tenant allowlists remain required |
| D12 | WorkOS — AuthKit session-token JWKS | https://workos.com/docs/reference/authkit/session-tokens/jwks | WorkOS Inc. | 2026-08-26 | 2026-11-26 or on WorkOS AuthKit/JWKS change | Reviewed | -03 | Live direct page; client-specific JWKS URL and signed access-token verification documented; deployed issuer/key state remains required |
| D13 | WorkOS — SSO | https://workos.com/docs/sso | WorkOS Inc. | 2026-08-26 | 2026-11-26 or on WorkOS SSO contract change | Reviewed | -05, -09 | Live direct page; organization/connection selection, callback and profile mapping documented; backend membership checks remain required |
| D14 | WorkOS — Environments | https://workos.com/docs/authkit/environments | WorkOS Inc. | 2026-08-26 | 2026-11-26 or on WorkOS environment model change | Reviewed | -02 | Live direct page; staging/production API keys, clients, organizations, connections and webhook endpoints are separate |
| D15 | WorkOS — Event synchronization (Directory Sync/Events API) | https://workos.com/docs/events/data-syncing | WorkOS Inc. | 2026-08-26 | 2026-11-26 or on WorkOS Events contract change | Reviewed | -11 | Live direct page; Events API and webhook synchronization paths documented; exact ordering/delivery and deployed reconciliation remain required |
| D16 | Supabase Auth — Sessions | https://supabase.com/docs/guides/auth/sessions | Supabase | 2026-08-26 | 2026-11-26 or on Supabase Auth session-policy change | Reviewed | -08 | Live direct page; session/JWT/refresh model, reuse handling and configurable timeout/single-session behavior documented |
| D17 | Supabase — JWT signing keys | https://supabase.com/docs/guides/auth/signing-keys | Supabase | 2026-08-26 | 2026-11-26 or on Supabase signing-key system change | Reviewed | -03 | Live direct page; asymmetric discovery, standby/current/previous/revoked rotation states and legacy-secret migration documented |
| D18 | Supabase Auth — MFA (AAL2) | https://supabase.com/docs/guides/auth/auth-mfa | Supabase | 2026-08-26 | 2026-11-26 or on Supabase MFA/AAL behavior change | Reviewed | -08, -10 | Live direct page; `aal1`/`aal2`, factor removal and backend/RLS enforcement documented; deployed policies remain required |
| D19 | Supabase Auth — Auth Hooks | https://supabase.com/docs/guides/auth/auth-hooks | Supabase | 2026-08-26 | 2026-11-26 or on Supabase Auth Hook contract change | Reviewed | -09, -11 | Live direct page; minimum `supabase_auth_admin` grants, public-role revocation and `security definer` warning documented |

Review status and limits:

- S1–S5 and D1–D19 are reviewed direct-source pages. Review proves only what current official
  documentation states; it never proves deployed issuer/JWKS/discovery state, Dashboard/API
  configuration, provider plan behavior, webhook delivery, key rotation, or reviewed-code parity.
- P1–P5 remain reviewed discovery snapshots only. They support discovery and profile selection,
  never current provider behavior or deployed configuration.
- Re-fetch any source at its expiry or earlier refresh trigger. A stale, inaccessible, changed,
  contradictory, or version-inapplicable page returns affected external-behavior claims to
  `Not verified` until owning review resolves it.
- Release blockers remain unchanged: this skill cannot pass when issuer/JWKS/discovery trust,
  token-purpose validation, callbacks/trusted origins, cookie/session and immediate-revocation
  design, account-linking or authenticator-migration policy, organization/directory mapping,
  lifecycle webhook/event reconciliation, or production/test tenant evidence is inaccessible.
- Never record a passing control from package presence, documentation alone, inaccessible
  Dashboard/API evidence, inferred configuration, or failed/incomplete tests.
- Per-provider deep verification and their own registers belong to `secod-clerk`,
  `secod-auth0`, `secod-workos`, `secod-better-auth`, `secod-supabase-auth`, `secod-aws-cognito`.
