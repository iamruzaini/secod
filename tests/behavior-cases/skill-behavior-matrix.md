# SECOD skill behavior matrix

Minimum behavior contract for every public SECOD skill. Each section contains one positive request, one similar non-trigger request, one missing-evidence case, one expected finding, and one expected non-finding.

This matrix is a review/test plan, not proof that an LLM executed every case. A real agent run must preserve the expected evidence boundaries below.

Global rule: missing, inaccessible, stale, or conflicting evidence must remain `Not verified`; routing, reachable URLs, documentation-only plans, and fixture execution never prove a deployed control.

## `secod-abuse-limits`

- Trigger request: `Review rate limits and idempotency for a checkout, password-reset, and export workflow.`
- Non-trigger request: `Review the project README grammar only; no application workflow or abuse-control review is requested.`
- Missing-evidence scenario: Checkout and export endpoints exist, but provider quota, distributed limiter, and production alert evidence are inaccessible. Every affected control stays `Not verified`.
- Expected finding: An in-memory per-process limiter and no idempotency key allow duplicate refunds and multi-instance quota bypass. Report `Do not ship` with request and code evidence.
- Expected non-finding: A shared user/tenant limiter, atomic idempotency store, bounded retries, and current test evidence exist. Report no finding for those controls; do not infer unrelated provider controls.

## `secod-ai-api-integrations`

- Trigger request: `Review an application proxying chat and embedding requests through OpenAI and a vector store.`
- Non-trigger request: `Review a static marketing site with no AI SDK, model endpoint, embeddings, or AI data flow.`
- Missing-evidence scenario: AI proxy exists, but provider retention, training, deletion, spend ceiling, and fallback-parity evidence cannot be inspected. Report `Not verified`.
- Expected finding: A browser bundle contains a long-lived provider key and retrieval queries lack tenant scoping. Report the secret-exposure and cross-tenant retrieval findings.
- Expected non-finding: Backend-only credentials, model allowlists, tenant-scoped retrieval, bounded usage, structured output validation, and current provider evidence are present. Report no finding for those controls.

## `secod-anthropic`

- Trigger request: `Review an application using the Anthropic SDK with server-side Claude requests.`
- Non-trigger request: `Review a project with no Anthropic SDK, Anthropic key, Claude endpoint, or Anthropic webhook.`
- Missing-evidence scenario: Anthropic integration exists, but current model, retention, training, spending, and deletion settings cannot be inspected. Keep Anthropic-specific controls `Not verified`.
- Expected finding: The client can choose arbitrary Claude models and the Anthropic key is exposed through a public environment variable. Report `Do not ship`.
- Expected non-finding: The key remains server-side, model and token limits are enforced, tenant boundaries are tested, and current Anthropic evidence is available. Report no Anthropic finding.

## `secod-auth-provider-integrations`

- Trigger request: `Review a Clerk, Auth0, WorkOS, or Supabase Auth callback and account-linking integration.`
- Non-trigger request: `Review a service with no identity provider, OAuth callback, SSO, SCIM, passkey, or auth webhook.`
- Missing-evidence scenario: An identity provider is configured, but issuer, audience, JWKS rotation, dashboard session, and webhook evidence are inaccessible. Report `Not verified`.
- Expected finding: The callback accepts a client-supplied issuer and account linking merges identities by email alone. Report issuer-confusion and account-takeover findings.
- Expected non-finding: Fixed trust anchors, PKCE/state/nonce, scoped callbacks, immutable subject mapping, revocation, and provider evidence are present. Report no auth-provider finding.

## `secod-auth0`

- Trigger request: `Review an application using Auth0 Universal Login, JWT validation, and a Management API.`
- Non-trigger request: `Review the same application when it has no Auth0 tenant, SDK, issuer, audience, or Auth0 environment variable.`
- Missing-evidence scenario: Auth0 is detected, but tenant signing algorithm, JWKS rotation, refresh-token rotation, and Management API scope evidence are unavailable. Report `Not verified`.
- Expected finding: The API accepts an ID token as an API bearer credential and grants broad Management API scope to the runtime key. Report `Do not ship`.
- Expected non-finding: RS256/JWKS and audience are pinned, refresh rotation is enabled, Management API scope is minimal, and current evidence is reviewed. Report no Auth0 finding.

## `secod-aws-cognito`

- Trigger request: `Review an Amazon Cognito User Pool, Identity Pool, hosted UI callback, and token verifier.`
- Non-trigger request: `Review a project with no Cognito user pool, identity pool, hosted UI, AWS auth SDK, or Cognito issuer.`
- Missing-evidence scenario: Cognito is present, but pool/client settings, callback allowlist, MFA, token claims, and identity-pool role evidence cannot be inspected. Report `Not verified`.
- Expected finding: A Cognito Identity Pool maps unauthenticated identities to a write-capable role and callbacks accept a wildcard origin. Report `Do not ship`.
- Expected non-finding: Pool/client IDs, issuer/audience, PKCE, callback origins, MFA, and authenticated role mappings are fixed and evidenced. Report no Cognito finding.

## `secod-aws-data-services`

- Trigger request: `Review an AWS application using RDS, DynamoDB, ElastiCache, and OpenSearch.`
- Non-trigger request: `Review an application with no AWS data-service SDK, ARN, IaC resource, endpoint, or AWS environment signal.`
- Missing-evidence scenario: AWS data services are detected, but IAM/resource policies, network exposure, encryption keys, backups, and audit-data evidence are inaccessible. Report `Not verified`.
- Expected finding: A production DynamoDB table has a public resource policy and the runtime role has wildcard data access. Report public-data and least-privilege findings.
- Expected non-finding: Dedicated workload roles, private endpoints, scoped policies, encryption, audit logging, and restore evidence are present. Report no AWS data-service finding.

## `secod-aws-lambda-api-gateway`

- Trigger request: `Review an AWS Lambda API behind API Gateway with authorizers, retries, and event integrations.`
- Non-trigger request: `Review a project with no Lambda, API Gateway, Function URL, AWS handler, or related IaC.`
- Missing-evidence scenario: Lambda/API Gateway is detected, but deployed routes, authorizer settings, stage variables, throttles, and execution-role evidence are unavailable. Report `Not verified`.
- Expected finding: A public Lambda Function URL bypasses the API Gateway authorizer and the function role can read every secret. Report `Do not ship`.
- Expected non-finding: Routes, authorizers, throttles, execution roles, secret access, timeout limits, and deployment evidence are current and scoped. Report no finding.

## `secod-aws-s3-cloudfront`

- Trigger request: `Review an AWS S3 upload flow served through CloudFront signed URLs.`
- Non-trigger request: `Review an application with no S3 bucket, CloudFront distribution, presigned URL, or AWS object-storage signal.`
- Missing-evidence scenario: S3/CloudFront is present, but bucket policy, origin access control, cache policy, object ownership, and deletion evidence are inaccessible. Report `Not verified`.
- Expected finding: The bucket permits `Principal: *`, uploads trust file extensions, and CloudFront caches private objects without tenant-aware keys. Report public-storage and file-handling findings.
- Expected non-finding: Private bucket access, origin access control, object ownership, content validation, scoped signed URLs, cache isolation, and deletion evidence are present. Report no finding.

## `secod-aws-web`

- Trigger request: `Review an AWS account and web workload using IAM roles, STS, KMS, Secrets Manager, and CloudTrail.`
- Non-trigger request: `Review a project with no AWS account, IAM principal, ARN, SDK, IaC provider, or AWS deployment signal.`
- Missing-evidence scenario: AWS is detected, but organization, account, region, IAM, KMS, secret, logging, and cross-account evidence cannot be inspected. Report `Not verified`.
- Expected finding: A committed long-lived IAM access key and wildcard cross-account trust policy are used by production. Report `Do not ship`.
- Expected non-finding: Federated human access, short-lived workload roles, scoped policies, KMS separation, managed secrets, CloudTrail, and drift evidence are present. Report no AWS account finding.

## `secod-better-auth`

- Trigger request: `Review Better Auth route handlers, trusted origins, cookies, sessions, and OAuth providers.`
- Non-trigger request: `Review a project with no Better Auth package, betterAuth call, auth route, or Better Auth configuration.`
- Missing-evidence scenario: Better Auth is detected, but production base URL, trusted origins, cookie settings, session store, and provider evidence are inaccessible. Report `Not verified`.
- Expected finding: Production `trustedOrigins` contains a broad wildcard and session cookies lack Secure and HttpOnly protections. Report `Do not ship`.
- Expected non-finding: Exact origins, secure cookies, server-side sessions, CSRF/origin checks, provider callbacks, and current evidence are present. Report no Better Auth finding.

## `secod-clerk`

- Trigger request: `Review Clerk middleware, organizations, JWT templates, webhooks, and session settings.`
- Non-trigger request: `Review a project with no Clerk package, Clerk middleware, `CLERK_*` variable, webhook, or Clerk domain.`
- Missing-evidence scenario: Clerk is detected, but Dashboard session limits, organization claims, webhook signing, and production instance evidence are inaccessible. Report `Not verified`.
- Expected finding: A route trusts a client-provided organization ID instead of verified Clerk claims, allowing cross-tenant access. Report `Do not ship`.
- Expected non-finding: Clerk claims are verified against fixed issuer/audience, organization membership is checked server-side, webhooks are authentic, and session evidence is current. Report no Clerk finding.

## `secod-cloudflare`

- Trigger request: `Review a Cloudflare account, zone, API token, WAF, Access, and Developer Platform deployment.`
- Non-trigger request: `Review a project with no Cloudflare account, Wrangler file, binding, zone, API token, or Cloudflare endpoint.`
- Missing-evidence scenario: Cloudflare is detected, but account, zone, token, Access, WAF, DNS, and deployment evidence are inaccessible. Report `Not verified`.
- Expected finding: A broad API token is stored in source and an Access-protected origin is reachable directly without the expected identity check. Report `Do not ship`.
- Expected non-finding: Scoped tokens, protected origin paths, verified Access JWTs, DNS ownership, WAF decisions, and current dashboard evidence are present. Report no Cloudflare finding.

## `secod-cloudflare-ai-gateway`

- Trigger request: `Review Cloudflare AI Gateway BYOK, provider routing, logging, and rate limits.`
- Non-trigger request: `Review a project with no AI Gateway endpoint, binding, BYOK key, provider route, or Cloudflare AI signal.`
- Missing-evidence scenario: AI Gateway is detected, but gateway policy, provider keys, logging retention, spend limits, and fallback evidence cannot be inspected. Report `Not verified`.
- Expected finding: The gateway accepts arbitrary provider/model choices and logs raw prompts containing tenant secrets. Report model-allowlist and sensitive-data findings.
- Expected non-finding: Gateway routing, provider credentials, model allowlists, tenant limits, redacted logs, retention, and fallback parity are evidenced. Report no AI Gateway finding.

## `secod-cloudflare-hyperdrive`

- Trigger request: `Review Cloudflare Hyperdrive bindings connecting Workers to a PostgreSQL database.`
- Non-trigger request: `Review a project with no Hyperdrive binding, database connection, Wrangler configuration, or Cloudflare database signal.`
- Missing-evidence scenario: Hyperdrive is detected, but binding configuration, database TLS, credentials, network restrictions, and pool behavior cannot be inspected. Report `Not verified`.
- Expected finding: A Hyperdrive binding exposes a reusable production connection string to untrusted Worker code without tenant authorization. Report `Do not ship`.
- Expected non-finding: Bindings are environment-separated, credentials stay server-side, TLS and least privilege are evidenced, and tenant authorization precedes queries. Report no Hyperdrive finding.

## `secod-cloudflare-pages`

- Trigger request: `Review Cloudflare Pages, Pages Functions, preview deployments, bindings, and deployment protection.`
- Non-trigger request: `Review a project with no Pages project, Pages Function, Wrangler Pages config, or Cloudflare deployment signal.`
- Missing-evidence scenario: Pages is detected, but preview access, deployment settings, environment bindings, domains, and function runtime evidence are unavailable. Report `Not verified`.
- Expected finding: Untrusted preview deployments receive production secrets and a Pages Function trusts a browser-supplied role. Report preview-isolation and authorization findings.
- Expected non-finding: Preview credentials are isolated, function routes authorize server-side, domains are owned, bindings are scoped, and current deployment evidence is present. Report no Pages finding.

## `secod-cloudflare-queues`

- Trigger request: `Review Cloudflare Queues producers, consumers, retries, DLQs, and message authorization.`
- Non-trigger request: `Review a project with no Queue binding, producer, consumer, DLQ, or Cloudflare queue endpoint.`
- Missing-evidence scenario: Queues are detected, but consumer bindings, retry policy, DLQ handling, message retention, and monitoring evidence are inaccessible. Report `Not verified`.
- Expected finding: The consumer retries a poison message without a bound and processes tenant messages without checking message ownership. Report retry-storm and tenant-boundary findings.
- Expected non-finding: Authenticated producers, bounded retries, DLQ handling, idempotency, tenant binding, retention, and alert evidence are present. Report no Queues finding.

## `secod-cloudflare-vectorize`

- Trigger request: `Review Cloudflare Vectorize indexes, embeddings, metadata filters, and deletion flow.`
- Non-trigger request: `Review a project with no Vectorize index, embedding call, vector binding, or Cloudflare AI retrieval signal.`
- Missing-evidence scenario: Vectorize is detected, but index metadata, tenant filters, retention, deletion, and query authorization evidence cannot be inspected. Report `Not verified`.
- Expected finding: Vector search queries omit tenant metadata filters and return embeddings from another customer. Report `Do not ship`.
- Expected non-finding: Tenant-scoped indexing and querying, authorization before retrieval, deletion propagation, and current index evidence are present. Report no Vectorize finding.

## `secod-cloudflare-workers`

- Trigger request: `Review Cloudflare Workers bindings, secrets, routes, service bindings, and runtime isolation.`
- Non-trigger request: `Review a project with no Worker script, Wrangler config, Worker binding, route, or Cloudflare Worker signal.`
- Missing-evidence scenario: Workers are detected, but deployed code, bindings, secrets, routes, compatibility settings, and runtime evidence are inaccessible. Report `Not verified`.
- Expected finding: A Worker route is public without authorization and a plain-text secret is included in a non-secret binding. Report `Do not ship`.
- Expected non-finding: Routes are protected, bindings and secrets are scoped, runtime limits are bounded, and deployed evidence matches source. Report no Workers finding.

## `secod-cloudflare-workers-ai`

- Trigger request: `Review Workers AI bindings, `env.AI.run`, model selection, limits, and output handling.`
- Non-trigger request: `Review a project with no Workers AI binding, `env.AI`, model call, or Cloudflare AI runtime signal.`
- Missing-evidence scenario: Workers AI is detected, but account limits, model availability, data retention, prompt logging, and deployment evidence are inaccessible. Report `Not verified`.
- Expected finding: A public Worker forwards unbounded user input to arbitrary models and renders raw model output as HTML. Report abuse and output-safety findings.
- Expected non-finding: Authentication, model allowlists, per-tenant limits, safe rendering, redacted logs, and current Workers AI evidence are present. Report no Workers AI finding.

## `secod-cloudflare-workflows`

- Trigger request: `Review Cloudflare Workflows steps, retries, waits, events, state, and compensation paths.`
- Non-trigger request: `Review a project with no Workflow definition, `step.do`, event trigger, binding, or Cloudflare workflow signal.`
- Missing-evidence scenario: Workflows are detected, but step retries, state retention, event authenticity, compensation, and operational evidence are inaccessible. Report `Not verified`.
- Expected finding: A payment step retries non-idempotently after timeout and workflow events are accepted without authentication. Report duplicate-effect and webhook findings.
- Expected non-finding: Events are authenticated, retries are bounded and idempotent, state is tenant-scoped, and compensation/recovery evidence is current. Report no Workflows finding.

## `secod-container-runtime`

- Trigger request: `Review Docker and Kubernetes workloads, images, secrets, capabilities, and network policies.`
- Non-trigger request: `Review a project with no Dockerfile, Compose file, Kubernetes manifest, Helm chart, Terraform container resource, or container deployment.`
- Missing-evidence scenario: Container deployment is detected, but runtime configuration, image provenance, admission, network, and restore evidence cannot be inspected. Report `Not verified`.
- Expected finding: The image uses a mutable tag, runs as root with added capabilities, and receives secrets through Docker `ARG`. Report `Do not ship`.
- Expected non-finding: Images are digest-pinned, builds use secret mounts, workloads run non-root with dropped capabilities, and resources/network are bounded. Report no container finding.

## `secod-convex`

- Trigger request: `Review Convex public functions, internal functions, scheduled jobs, storage URLs, and authorization.`
- Non-trigger request: `Review a project with no Convex package, `convex/` directory, function, storage URL, or Convex deployment signal.`
- Missing-evidence scenario: Convex is detected, but deployed function visibility, auth configuration, storage access, scheduled jobs, and environment evidence are inaccessible. Report `Not verified`.
- Expected finding: A public Convex function calls a privileged internal path without user or tenant authorization and returns a reusable storage URL. Report `Do not ship`.
- Expected non-finding: Public functions authorize at the boundary, internal paths are protected, storage URLs are scoped/expiring, and current deployment evidence is present. Report no Convex finding.

## `secod-core`

- Trigger request: `Use SECOD core to inventory this repository, classify stack signals, compute dependency closure, and create a Security Plan.`
- Non-trigger request: `Review the README spelling only; do not inspect application code, dependencies, deployment, or security behavior.`
- Missing-evidence scenario: A repository review is requested, but the deployment root, production artifact, or required provider evidence is inaccessible. Classify affected signals as `Not verified` and do not issue readiness.
- Expected finding: A lockfile and production artifact disagree on the Next.js version, and core routes the framework skill while marking the conflict `Not verified`.
- Expected non-finding: Signals are classified with paths and scope, closure is complete, and no unverified conflict is found. Report no routing finding; routing itself is never proof of a control passing.

## `secod-crypto-data-protection`

- Trigger request: `Review TLS, token generation, encryption, retention, deletion, backups, and sensitive-data sharing.`
- Non-trigger request: `Review a static landing page with no credentials, personal data, storage, encryption, analytics, or backend data lifecycle.`
- Missing-evidence scenario: Sensitive data is present, but key management, backup restore, provider deletion, retention, and analytics evidence cannot be inspected. Report `Not verified`.
- Expected finding: The application uses predictable reset tokens, stores PII in unencrypted backups, and has no deletion propagation record. Report `Do not ship`.
- Expected non-finding: CSPRNGs, authenticated encryption, separated keys, retention/deletion records, encrypted backups, and direct evidence are present. Report no crypto/data-protection finding.

## `secod-data-files`

- Trigger request: `Review uploads, downloads, signed URLs, exports, image processing, and file retention.`
- Non-trigger request: `Review a project with no upload, download, attachment, storage object, export, rendering, or file-processing path.`
- Missing-evidence scenario: File handling exists, but content validation, malware decision, signed URL policy, rendering limits, deletion, and CDN evidence are inaccessible. Report `Not verified`.
- Expected finding: The upload endpoint trusts the filename, accepts unlimited archives, and generates tenant-free public download URLs. Report unrestricted-upload and authorization findings.
- Expected non-finding: Magic bytes, type/size limits, generated names, scoped expiring URLs, processing bounds, cache isolation, and deletion evidence are present. Report no file-handling finding.

## `secod-dodo-payments`

- Trigger request: `Review Dodo Payments checkout, webhook verification, subscriptions, refunds, and entitlement mapping.`
- Non-trigger request: `Review a project with no Dodo Payments SDK, checkout route, webhook, customer ID, or Dodo configuration.`
- Missing-evidence scenario: Dodo is detected, but webhook capability, event version, signing, retries, reconciliation, and production account evidence are inaccessible. Report `Not verified`.
- Expected finding: The application grants access from the browser return URL and accepts a Dodo webhook without raw-body authenticity verification. Report `Do not ship`.
- Expected non-finding: Verified Dodo state is authoritative, events are deduplicated and reconciled, credentials stay server-side, and current evidence is present. Report no Dodo finding.

## `secod-email-messaging`

- Trigger request: `Review email, SMS, OTP, magic-link, invitation, and delivery-webhook flows.`
- Non-trigger request: `Review a project with no email/SMS SDK, OTP, magic link, invitation, notification, or delivery webhook.`
- Missing-evidence scenario: Messaging is detected, but provider credentials, recipient binding, delivery authenticity, suppression, SPF/DKIM/DMARC, and abuse evidence are inaccessible. Report `Not verified`.
- Expected finding: A password-reset link is reusable and the response reveals whether an email address exists. Report token-lifecycle and enumeration findings.
- Expected non-finding: Credentials stay server-side, links/OTPs are single-use and expiring, responses are uniform, delivery events are verified, and evidence is current. Report no messaging finding.

## `secod-failure-safety`

- Trigger request: `Review failure handling for database, storage, network, provider, queue, and payment operations.`
- Non-trigger request: `Review a static page with no server operation, dependency call, state mutation, job, retry, or failure boundary.`
- Missing-evidence scenario: Server operations exist, but production failure drills, rollback evidence, timeout behavior, and degraded-state evidence cannot be inspected. Report `Not verified`.
- Expected finding: A timeout after payment mapping leaves an entitlement granted, retries non-idempotently, and returns a stack trace. Report `Do not ship`.
- Expected non-finding: Authorization fails closed, partial mutations roll back or reconcile, retries are classified, cancellation propagates, and errors are redacted. Report no failure-safety finding.

## `secod-firebase`

- Trigger request: `Review Firebase Authentication, Firestore, Realtime Database, Storage Rules, App Check, and Admin SDK use.`
- Non-trigger request: `Review a project with no Firebase config, Rules file, Firebase SDK, Admin SDK, or Firebase service.`
- Missing-evidence scenario: Firebase is detected, but deployed Rules, App Check rollout, Admin SDK permissions, indexes, and project environment evidence are inaccessible. Report `Not verified`.
- Expected finding: Firestore Rules allow any authenticated user to read every tenant document and Firebase Storage accepts writes without App Check. Report `Do not ship`.
- Expected non-finding: Rules deny by default with tenant tests, App Check is enforced where required, Admin credentials are server-only, and deployed evidence is current. Report no Firebase finding.

## `secod-google-cloud-storage`

- Trigger request: `Review Google Cloud Storage buckets, signed URLs, IAM, object retention, and public access.`
- Non-trigger request: `Review a project with no GCS bucket, Google Cloud Storage SDK, `gs://` URI, signed URL, or GCP storage resource.`
- Missing-evidence scenario: GCS is detected, but bucket IAM, uniform access, signed URL policy, retention, encryption, and audit evidence cannot be inspected. Report `Not verified`.
- Expected finding: A bucket grants `allUsers` object access and signed URLs are not bound to tenant or object ownership. Report public-storage and authorization findings.
- Expected non-finding: Uniform bucket access, scoped service accounts, private objects, bounded signed URLs, retention/deletion, encryption, and current evidence are present. Report no GCS finding.

## `secod-google-cloud-web`

- Trigger request: `Review a Google Cloud web workload using IAM, service accounts, Secret Manager, KMS, and Cloud Audit Logs.`
- Non-trigger request: `Review a project with no GCP project, service account, Google Cloud SDK, Terraform provider, or GCP deployment signal.`
- Missing-evidence scenario: GCP is detected, but organization/project IAM, service-account keys, Secret Manager, KMS, network, and logging evidence are inaccessible. Report `Not verified`.
- Expected finding: A downloaded service-account JSON key is committed and a production service account has a basic Owner role. Report `Do not ship`.
- Expected non-finding: Workload identity, dedicated service accounts, scoped IAM, managed secrets, KMS separation, audit logs, and project-environment evidence are present. Report no GCP finding.

## `secod-google-genai`

- Trigger request: `Review a Gemini or Google GenAI integration using the Google GenAI SDK, Vertex AI, or Live API.`
- Non-trigger request: `Review a project with no Gemini, Vertex AI, Google GenAI SDK, model endpoint, or Google AI environment signal.`
- Missing-evidence scenario: Google GenAI is detected, but project IAM, model access, retention, regional, Live API, and spend evidence cannot be inspected. Report `Not verified`.
- Expected finding: A Gemini API key is shipped to the browser and Live API sessions are not bound to an authenticated user or origin. Report `Do not ship`.
- Expected non-finding: Credentials and project access stay server-side, models and quotas are scoped, Live API tokens are constrained, and current Google evidence is present. Report no Google GenAI finding.

## `secod-identity-access`

- Trigger request: `Review login, session, authorization, API keys, MFA, OAuth, share links, tenant checks, and account recovery.`
- Non-trigger request: `Review a static site with no login, session, token, API key, role, tenant, share link, or privileged action.`
- Missing-evidence scenario: An authenticated application exists, but deployed session, revocation, MFA, key, recovery, and authorization evidence cannot be inspected. Report `Not verified`.
- Expected finding: A user can change `tenant_id` in a request and read another tenant's invoice; server code trusts the browser role. Report BOLA and missing server authorization findings.
- Expected non-finding: Backend authorization is deny-by-default, tenant/resource checks are tested, tokens and sessions have lifecycle controls, and evidence is current. Report no identity finding.

## `secod-inputs-apis`

- Trigger request: `Review REST, GraphQL, WebSocket, outbound HTTP, webhook, redirect, and error-handling boundaries.`
- Non-trigger request: `Review a static asset repository with no server route, API client, webhook, parser, redirect, or network boundary.`
- Missing-evidence scenario: API boundaries exist, but deployed route inventory, proxy topology, outbound allowlists, schemas, webhook settings, and negative-test evidence are inaccessible. Report `Not verified`.
- Expected finding: A server fetches a user-supplied URL through unrestricted redirects and a webhook trusts parsed JSON without authenticity verification. Report SSRF and webhook findings.
- Expected non-finding: Routes are inventoried, schemas and responses are allowlisted, outbound destinations are constrained, redirects are validated, and errors fail closed. Report no API-boundary finding.

## `secod-lemonsqueezy`

- Trigger request: `Review Lemon Squeezy checkout, signed webhooks, licenses, subscriptions, and entitlement state.`
- Non-trigger request: `Review a project with no Lemon Squeezy SDK, store/product ID, checkout, webhook, license, or Lemon configuration.`
- Missing-evidence scenario: Lemon Squeezy is detected, but signing secret, event handling, API version, replay, reconciliation, and production account evidence are inaccessible. Report `Not verified`.
- Expected finding: The application trusts the checkout redirect and does not verify the Lemon Squeezy webhook signature before granting a license. Report `Do not ship`.
- Expected non-finding: Signed events are deduplicated and reconciled, licenses are tied to authenticated users, credentials are server-only, and current evidence is present. Report no Lemon Squeezy finding.

## `secod-neon`

- Trigger request: `Review Neon branches, PostgreSQL roles, RLS, connection pooling, Data API, backups, and preview data.`
- Non-trigger request: `Review a project with no Neon project, PostgreSQL connection, Neon SDK, `neon.tech` host, or Neon configuration.`
- Missing-evidence scenario: Neon is detected, but branch protection, role grants, RLS, TLS, Data API, IP Allow, backups, and restore evidence cannot be inspected. Report `Not verified`.
- Expected finding: A pooled connection reuses tenant context and the application role has `BYPASSRLS`; preview branches contain production PII. Report `Do not ship`.
- Expected non-finding: Roles are least-privileged, RLS and transaction-local tenant context are tested, preview data is isolated, TLS is verified, and restore evidence is current. Report no Neon finding.

## `secod-nextjs`

- Trigger request: `Review a Next.js App Router application with Route Handlers, Server Actions, caching, and image configuration.`
- Non-trigger request: `Review a project with no `next` dependency, Next.js config, App/Pages Router, Route Handler, or Next.js build.`
- Missing-evidence scenario: Next.js is detected, but production build/runtime, version, cache, source-map, server-action, and deployment evidence cannot be inspected. Report `Not verified`.
- Expected finding: A Server Action trusts its hidden UI caller, a shared cache key omits tenant identity, and production browser source maps are public. Report `Do not ship`.
- Expected non-finding: Server boundaries authorize independently, cache keys are scoped, action origins/body limits are constrained, image patterns are narrow, and production evidence is current. Report no Next.js finding.

## `secod-observability-response`

- Trigger request: `Review audit logs, redaction, alerts, key revocation, incident response, and restore drills.`
- Non-trigger request: `Review a static asset with no logging, alerting, credential lifecycle, incident response, backup, or restore process.`
- Missing-evidence scenario: Security logging or recovery is claimed, but deployed log policy, retention, alert delivery, runbooks, revocation, and restore evidence are inaccessible. Report `Not verified`.
- Expected finding: Login logs contain bearer tokens and no alert exists for disabled webhook endpoints or revoked-key use. Report sensitive-log and detection findings.
- Expected non-finding: Structured events are redacted, retention/access are scoped, alerts map to runbooks, revocation is visible, and restore drills are evidenced. Report no observability finding.

## `secod-openai`

- Trigger request: `Review an OpenAI API, Responses, Realtime, files, tools, and project-spend integration.`
- Non-trigger request: `Review a project with no OpenAI SDK, API key, Responses/Realtime call, file upload, tool, or OpenAI endpoint.`
- Missing-evidence scenario: OpenAI is detected, but project limits, model access, retention, data controls, Realtime configuration, and spend evidence are inaccessible. Report `Not verified`.
- Expected finding: The browser receives an unrestricted OpenAI key and model output can invoke a destructive tool without server authorization or confirmation. Report `Do not ship`.
- Expected non-finding: Keys remain server-side, project/model/user limits are enforced, tool calls are allowlisted and authorized, output is validated, and current OpenAI evidence is present. Report no OpenAI finding.

## `secod-packages-delivery`

- Trigger request: `Review dependency manifests, lockfiles, CI workflows, release tags, artifacts, provenance, and rollback.`
- Non-trigger request: `Review a repository containing only prose and static assets with no dependency, build, CI, artifact, or release surface.`
- Missing-evidence scenario: A delivery pipeline exists, but registry policy, action pins, secret handling, artifact provenance, SBOM, vulnerability findings, and rollback evidence are inaccessible. Report `Not verified`.
- Expected finding: A workflow executes mutable third-party Actions and a pull request can publish an artifact with production credentials. Report supply-chain and privilege findings.
- Expected non-finding: Lockfiles are enforced, actions use full commit SHAs, forks are isolated, artifacts are immutable and attested, and rollback evidence is current. Report no delivery finding.

## `secod-payments-billing`

- Trigger request: `Review checkout, subscriptions, invoices, refunds, disputes, webhooks, entitlements, and payment reconciliation.`
- Non-trigger request: `Review an application with no checkout, billing account, subscription, invoice, refund, payment webhook, or entitlement path.`
- Missing-evidence scenario: A payment flow exists, but provider state, webhook capabilities, API version, ledger, reconciliation, and production evidence cannot be inspected. Report `Not verified`.
- Expected finding: The browser supplies price and paid status, duplicate webhooks create duplicate entitlements, and refund events are not reconciled. Report `Do not ship`.
- Expected non-finding: The server resolves prices, verified provider state is authoritative, events are idempotent/reconciled, credentials are isolated, and current evidence is present. Report no payment finding.

## `secod-polar`

- Trigger request: `Review Polar checkout, customer binding, webhooks, subscriptions, and entitlement state.`
- Non-trigger request: `Review a project with no Polar SDK, checkout, product, customer, webhook, or Polar environment variable.`
- Missing-evidence scenario: Polar is detected, but webhook signing, account binding, event status, retries, reconciliation, and production evidence are inaccessible. Report `Not verified`.
- Expected finding: The checkout customer is selected from a request body and a forged Polar event can grant membership. Report `Do not ship`.
- Expected non-finding: Authenticated users are bound to Polar customers, signed events are deduplicated/reconciled, and current provider evidence is present. Report no Polar finding.

## `secod-runtime-execution`

- Trigger request: `Review subprocess, shell, template, dynamic-code, LDAP, XPath, or job execution paths.`
- Non-trigger request: `Review a project with no process spawn, shell command, dynamic evaluation, template source, query construction, or execution boundary.`
- Missing-evidence scenario: An execution boundary exists, but runtime identity, sandbox, argument policy, timeout, output cap, and production evidence are inaccessible. Report `Not verified`.
- Expected finding: A request parameter is concatenated into `shell=True` command execution. Report OS command injection and argument-injection findings.
- Expected non-finding: Executable and arguments are fixed/validated, shell use is disabled, the worker is least-privileged and bounded, and evidence is current. Report no runtime-execution finding.

## `secod-secrets-config`

- Trigger request: `Review environment variables, credentials, bearer capabilities, secret stores, rotation, revocation, and production config.`
- Non-trigger request: `Review a project with no credential, environment variable, secret store, token, configuration, CI secret, or privileged capability.`
- Missing-evidence scenario: Secrets or privileged configuration exist, but runtime exposure, rotation, revocation, history, environment separation, and deployment evidence are inaccessible. Report `Not verified`.
- Expected finding: A live payment key appears in a client bundle and a committed secret was removed without rotation or history-removal evidence. Report `Do not ship`.
- Expected non-finding: Secrets stay server-side in scoped stores, environments are separated, rotation/revocation and history scanning are evidenced, and current configuration is reviewed. Report no secrets finding.

## `secod-ship-check`

- Trigger request: `Run a SECOD pre-launch ship check after all applicable skill findings and evidence are collected.`
- Non-trigger request: `Summarize product copy; do not aggregate security findings or issue a launch-readiness assessment.`
- Missing-evidence scenario: A launch check is requested, but one triggered skill, dependency, provider source, deployment artifact, or negative test is missing. Issue no readiness verdict and mark affected controls `Not verified`.
- Expected finding: A triggered provider adapter is absent from the dependency closure and authorization evidence is missing. Return `Do not ship` or `Not verified`, never launch-ready.
- Expected non-finding: Every triggered skill and dependency returns current control-level evidence with no blockers. Report the bounded status supported by that evidence; do not claim certification.

## `secod-stripe`

- Trigger request: `Review Stripe Checkout, PaymentIntents, webhooks, subscriptions, refunds, and entitlement mapping.`
- Non-trigger request: `Review a project with no Stripe SDK, secret, customer, price, checkout, webhook, or Stripe configuration.`
- Missing-evidence scenario: Stripe is detected, but account mode, API version, webhook endpoint, signing, replay, reconciliation, and production evidence are inaccessible. Report `Not verified`.
- Expected finding: A live secret key is exposed and the application grants entitlement from the success redirect instead of verified Stripe state. Report `Do not ship`.
- Expected non-finding: Secret/live-test separation, server-resolved prices, signed/deduplicated webhooks, reconciliation, and current Stripe evidence are present. Report no Stripe finding.

## `secod-supabase`

- Trigger request: `Review Supabase Postgres, RLS, Storage, Realtime, Edge Functions, service-role keys, and project configuration.`
- Non-trigger request: `Review a project with no Supabase URL, SDK, migration, service-role key, Storage, Realtime, or Supabase deployment signal.`
- Missing-evidence scenario: Supabase is detected, but project settings, RLS policies, roles, service keys, Storage policies, Realtime, and production evidence are inaccessible. Report `Not verified`.
- Expected finding: The browser uses a service-role key and an exposed table has no tenant RLS policy. Report `Do not ship`.
- Expected non-finding: Publishable/secret boundaries are enforced, service authority stays server-side, RLS and roles are tested, Storage/Realtime access is scoped, and evidence is current. Report no Supabase finding.

## `secod-supabase-auth`

- Trigger request: `Review Supabase Auth SSR cookies, OAuth, MFA, JWT signing keys, Auth Hooks, redirects, and RLS integration.`
- Non-trigger request: `Review a project with no Supabase Auth calls, GoTrue config, auth callback, JWT, MFA, or Supabase Auth environment variable.`
- Missing-evidence scenario: Supabase Auth is detected, but signing-key/JWKS, session limits, refresh reuse, redirect, MFA, Auth Hook, and dashboard evidence are inaccessible. Report `Not verified`.
- Expected finding: Server code trusts `getSession()` cookie data for authorization and a broad redirect allows OAuth token leakage. Report `Do not ship`.
- Expected non-finding: Server claims use fixed issuer/audience/JWKS, cookies and PKCE are safe, redirect origins are exact, MFA/RLS are enforced, and current evidence is present. Report no Supabase Auth finding.

## `secod-threat-model`

- Trigger request: `Create a threat model covering assets, actors, trust boundaries, tenants, abuse cases, failures, and high-impact flows.`
- Non-trigger request: `Rewrite a product description; do not model application assets, attackers, trust boundaries, or security flows.`
- Missing-evidence scenario: A high-impact feature is under review, but data classes, deployment boundaries, provider flows, or failure evidence are unknown. Mark scope `Not verified` and block readiness.
- Expected finding: The model omits the admin export trust boundary and cross-tenant retrieval abuse case. Report the unmodeled high-impact path.
- Expected non-finding: Assets, actors, boundaries, abuse cases, failure states, mitigations, and residual risks are explicitly documented. Report no threat-model omission for covered scope.

## `secod-vercel-ai`

- Trigger request: `Review Vercel AI SDK or AI Gateway provider routing, models, budgets, telemetry, and data boundaries.`
- Non-trigger request: `Review a project with no Vercel AI SDK, AI Gateway, model route, provider configuration, or Vercel AI signal.`
- Missing-evidence scenario: Vercel AI is detected, but project/provider scope, model limits, telemetry, retention, budgets, and deployment evidence are inaccessible. Report `Not verified`.
- Expected finding: A client-controlled provider and model can bypass the approved budget and raw prompts are sent to an unreviewed fallback provider. Report `Do not ship`.
- Expected non-finding: Provider/model allowlists, project scope, budgets, tenant isolation, redacted telemetry, fallback parity, and current evidence are present. Report no Vercel AI finding.

## `secod-vercel-platform`

- Trigger request: `Review Vercel projects, deployments, environments, domains, protection, OIDC, bypass secrets, and rollback.`
- Non-trigger request: `Review a project with no Vercel config, deployment URL, `VERCEL_*` variable, Vercel CLI, or Vercel Git integration.`
- Missing-evidence scenario: Vercel is detected, but project/team access, deployment protection, environment variables, domains, bypasses, logs, and rollback evidence are inaccessible. Report `Not verified`.
- Expected finding: A preview deployment receives production credentials and a shareable-link bypass exposes a production deployment. Report `Do not ship`.
- Expected non-finding: Environment isolation, protected deployments, scoped OIDC, domain ownership, bypass rotation, logs, source-map policy, and rollback evidence are current. Report no Vercel finding.

## `secod-vulnerability-management`

- Trigger request: `Review dependency alerts, SCA/SAST, secret scanning, SBOM, provenance, remediation ownership, and rescans.`
- Non-trigger request: `Review a static document repository with no dependency, source code, build, advisory, scanner, SBOM, or release surface.`
- Missing-evidence scenario: A software supply chain exists, but scanner coverage, findings, SBOM, provenance, remediation SLA, and exception evidence are inaccessible. Report `Not verified`.
- Expected finding: A critical dependency advisory has no owner or SLA, and the release lacks an SBOM and provenance attestation. Report `Do not ship`.
- Expected non-finding: Scans cover the build, findings have owners and deadlines, SBOM/provenance are verified, exceptions expire, and fixes are rescanned. Report no vulnerability-management finding.

## `secod-web-app-security`

- Trigger request: `Review browser rendering, CSP, cookies, CSRF/CORS, iframe/postMessage, redirects, caches, service workers, and source maps.`
- Non-trigger request: `Review a backend-only batch script with no browser output, cookie, cross-origin request, HTML, iframe, service worker, or client bundle.`
- Missing-evidence scenario: Browser content exists, but deployed headers, CSP, cache behavior, source-map publication, origins, and client-token evidence are inaccessible. Report `Not verified`.
- Expected finding: A user-controlled HTML value is rendered unsanitized and a permissive CSP allows arbitrary scripts; sensitive tokens are stored in browser-accessible storage. Report `Do not ship`.
- Expected non-finding: Output is contextual/escaped, CSP is strict, cookies/CSRF/CORS are scoped, caches isolate users, and deployed header evidence is current. Report no web-security finding.

## `secod-whop`

- Trigger request: `Review Whop checkout, memberships, webhooks, access checks, and server credentials.`
- Non-trigger request: `Review a project with no Whop SDK, product, membership, checkout, webhook, or Whop configuration.`
- Missing-evidence scenario: Whop is detected, but membership state, webhook authenticity, credential scope, retries, and production evidence are inaccessible. Report `Not verified`.
- Expected finding: The browser claims a paid membership and server code grants access without retrieving verified Whop state. Report `Do not ship`.
- Expected non-finding: Least-privilege credentials, verified provider membership, deduplicated events, server-side access decisions, and current evidence are present. Report no Whop finding.

## `secod-workos`

- Trigger request: `Review WorkOS AuthKit, SSO, Directory Sync, SCIM, refresh tokens, webhooks, and organization mapping.`
- Non-trigger request: `Review a project with no WorkOS SDK, AuthKit, SSO, SCIM, Directory Sync, WorkOS key, or WorkOS webhook.`
- Missing-evidence scenario: WorkOS is detected, but client/application environment, refresh-token, organization, directory, webhook, and Events API evidence are inaccessible. Report `Not verified`.
- Expected finding: SCIM deprovisioning events are not reconciled and a user retains tenant access after directory removal. Report `Do not ship`.
- Expected non-finding: WorkOS identities map to immutable local subjects, refresh tokens are protected, SCIM/events reconcile, webhooks are verified, and current evidence is present. Report no WorkOS finding.

## `secod-xai-grok`

- Trigger request: `Review an xAI Grok API integration, model allowlist, usage limits, retention, and optional transport authentication.`
- Non-trigger request: `Review a project with no xAI SDK, Grok model, xAI endpoint, `XAI_API_KEY`, or xAI configuration.`
- Missing-evidence scenario: xAI is detected, but project/model, key scope, retention, usage, region, webhook, and transport evidence are inaccessible. Report `Not verified`.
- Expected finding: The xAI key is exposed to the client and user input selects arbitrary high-cost models without tenant or spend limits. Report `Do not ship`.
- Expected non-finding: xAI credentials remain server-side, model and spend limits are enforced, data handling is reviewed, and current xAI evidence is present. Report no xAI finding.
