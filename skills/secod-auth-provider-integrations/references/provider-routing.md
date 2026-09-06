# Auth Provider Integrations product routing

## Selection rule

Require current-feature evidence: import or SDK call, provider configuration/IaC, runtime binding, route, or explicit user request. Package presence alone is Possible. Route only Confirmed products.

## Adapter map

- Clerk selects secod-clerk.
- Auth0 selects secod-auth0.
- WorkOS/AuthKit/SSO/Directory Sync selects secod-workos.
- Better Auth selects secod-better-auth.
- Supabase Auth selects secod-supabase-auth plus secod-supabase.
- Amazon Cognito selects secod-aws-cognito plus secod-aws-web.

## Shared context

Pass exact product, resolved SDK/tool version, environment, resource/project/account identifiers without secrets, identity model, data classes, trust boundaries, likely files, tests, routing reason, and narrow assumptions.

## Shared defaults

- Keep provider secrets and privileged session operations server-side.
- Validate issuer, audience, signature, time, purpose, state, nonce, and PKCE as applicable.
- Map immutable provider subject and provider/tenant identity to local user and tenant records.
- Authorize application resources independently of provider authentication.

## Exclusions

Do not select sibling adapters without product evidence. Do not inspect unrelated account settings. Do not guess plan, Region, deployment state, or APIs.
