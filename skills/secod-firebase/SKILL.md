---
name: secod-firebase
description: Deny unauthorized client access through tested Firebase Security Rules; enforce App Check for every detected supported Firebase service after an evidence-based rollout; keep Admin…
---

# SECOD Firebase

## Scope and applicability

Deny unauthorized client access through tested Firebase Security Rules; enforce App Check for
every detected supported Firebase service after an evidence-based rollout; keep Admin SDK,
service-account and Cloud Functions authority server-side; and make Firebase Auth, Functions and
billing controls resistant to abuse. Apply to each detected Firebase project, app, product and
environment. `secod-identity-access`, `secod-secrets-config`, `secod-abuse-limits` and `secod-
observability-response` remain required general-skill dependencies; route `secod-ai-api-
integrations` too when Firebase AI Logic or a Gemini integration is detected.

## Control requirements

Exact Firebase/Google Cloud organization, project number/ID, billing account, application
identifiers, region, plan, product, SDK/CLI, service-account, API-key, Auth-provider, App Check
attestation provider, Cloud Functions/Hosting and development/preview/staging/production
inventory; distinct projects for pre-production and production, least-privilege IAM through
groups, multiple appropriately protected production owners, no production-data access by
default, production alert recipients and project-deletion/recovery safeguards; default-deny
Firebase Security Rules for every Firestore, Realtime Database and Cloud Storage resource, with
explicit user, tenant, owner, role, field/path, query and upload/download constraints, Rules
treated as application schema rather than a launch-only task, and positive plus negative
Emulator Suite tests committed and run in CI against each environment's rules; no client-side
rule bypass through Admin SDK, service-account credential or trusted-server proxy, with Admin
SDK/service account, FCM server credentials and non-Firebase private keys only in developer-
controlled server runtimes, ADC/managed workload identity preferred where available, and non-
Google secrets in Secret Manager rather than Cloud Functions environment variables, source,
client configuration, logs or CI output; App Check service-support inventory, registered
attestation provider/app versions, metrics and rollout evidence, enforcement status for every
supported production service rather than an App Check “decision”, and limited-use/replay
protection evidence where replay-sensitive endpoints use it—while retaining Auth, Rules and IAM
because App Check is supplementary; Firebase client API-key inventory that correctly
distinguishes Firebase-provisioned keys as public project identifiers from secrets, restricts
each key to the exact application and required APIs, keeps Firebase keys only on Firebase-
related APIs, uses separate restricted keys for non-Firebase Google APIs including Gemini,
constrains relevant API quotas, and never exposes Admin, FCM server, service-account, provider
or other secret keys; Firebase Auth inventory covering exact authorized domains, OAuth callback
and email action URLs, no unowned/broad production wildcard, disabled unused sign-in providers,
anonymous authentication limited to warm onboarding with Rules requiring a durable sign-in
method or verified email for non-public data, email-enumeration protection and sign-in quota
policy, MFA/step-up where required, and Phone Auth reCAPTCHA/App Check, authorized-domain and
SMS-region-abuse policy evidence; Cloud Functions and callable/HTTP endpoint inventory with per-
function runtime identity/IAM invoker policy, public-versus-private decision, server-side
authentication/authorization, request/schema/size/timeout/concurrency/max-instance limits, App
Check enforcement where supported, restricted outbound destinations, idempotent event handling,
trigger-loop protection, explicit retry/error/dead-letter behavior and local-emulator test
evidence; Hosting/App Hosting/Cloud Run, Extensions, FCM, Remote Config, Realtime and Storage
configurations reviewed when detected for public endpoints, secrets, authorization, release
environment and data-exposure risks; budget alerts, usage/quota/abuse and cost-spike monitoring,
applicable Firebase spend caps, service/dashboard alerts, Cloud Functions logs and post-
dependency-update monitoring, with a documented response because budget alerts are not caps;
exact rules, Auth, App Check, IAM, API-key, secret, environment, billing and monitoring console
evidence; source URL/status or version/last-modified evidence, reviewed date and review expiry;
negative tests for open/overbroad Rules, query or cross-tenant bypass, Storage-path abuse,
Admin/service-account/secret delivery to client, unenforced or replayable App Check, API-key
misuse and quota abuse, disabled-provider/anonymous/Auth-domain/SMS abuse, callable/HTTP/IAM
authorization bypass, function trigger loops, function over-scaling/cost abuse, emulator-versus-
production drift, and missing alerts or incident evidence.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-identity-access`, `secod-secrets-config`, `secod-abuse-limits`, `secod-observability-response`.

When a required dependency is not installed or cannot be invoked, record the affected
control as **Not verified** and do not issue a passing or launch-ready conclusion.

## Negative fixtures and tests

- Run the maintained trigger case and insecure fixture plan at `tests/` for this skill.
- Test the unsafe or missing-control cases implied by the control requirements, including
  unavailable-provider and partial-failure behavior where applicable.
- Keep tests read-only unless the user explicitly authorizes a change.

## Output schema

For each finding return: `control_id`, `status`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, and `source_refs`. Valid status values are `Do not ship`,
`Fix before launch`, `Recommended hardening`, `Passed with evidence`, and `Not verified`.

## Verification and safe failure

Never infer dashboard, deployment, provider, or production settings from package presence.
Redact secrets and bearer credentials. Fail closed: preserve unknown or failed checks as
**Not verified**, identify the next verification step, and never claim launch readiness from
incomplete evidence.

## References

Use the source register in `references/sources.md`. For each security-critical source,
record the direct URL, documentation index URL, version, reviewed date, review expiry,
hash/ETag when available, owner, plan/tier, region, feature maturity, and linked control IDs.
