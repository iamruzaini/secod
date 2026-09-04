# Behavior case: secod-workos

## Clean AuthKit integration

Fixture contains reachable `@workos-inc/authkit-nextjs` code, a fixed non-secret client ID,
server-only API/sealing secret references, fixed client-specific JWKS/issuer/audience constants,
HttpOnly/Secure sealed cookie, exact production callbacks, backend resource authorization using
verified active membership, durable event cursor/deduplication, and raw-body Action/webhook
verification before queueing work.

Supplied redacted provider evidence shows separate staging/production applications, domains,
organizations, connections, endpoint secrets, session settings, logout/revocation, SSO/IdP MFA
policy, custom domain before production passkeys, and enabled feature subscriptions. The expected
review executes the applicable controls, requests current direct sources, records plan/region/
maturity/version assumptions, and returns `Passed with evidence` only for controls whose negative
tests and provider evidence are complete. Optional API Keys/API Gateway remain not applicable
unless their reachable code and Dashboard evidence are included.
