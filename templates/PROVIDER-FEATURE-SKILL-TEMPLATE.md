<!-- SECOD template for an exact provider product, SDK, API, or integration. -->

---
name: <secod-provider-feature>
description: >-
  Help AI coding agents implement <provider product or feature> securely using
  supported APIs and SDKs. Use when <exact product, package, API, or task triggers>.
license: Apache-2.0
compatibility: "Requires <provider/product>; recipes state supported SDK and runtime versions."
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# Secure <provider product/feature> implementation

## Purpose

Give the coding agent provider-specific decisions, safe code patterns, tests, and official documentation for <feature>. Combine this adapter with the applicable generalized and framework skills.

## When to use

Use when the task or repository includes:

- `<official-package-or-import>`;
- <specific API/resource/configuration>;
- <specific feature request>.

Do not activate for <similar provider/product>. Route broad provider discovery to `<provider-family-skill>`.

## Context to inspect

- Exact product, API, SDK, and runtime versions.
- Existing provider client initialization and credential source.
- Trusted server/worker versus browser/mobile boundary.
- Identity, tenant, ownership, role, and resource-policy model.
- Data classification, region, retention, and deletion needs.
- Webhook/event delivery, retries, concurrency, and idempotency where applicable.
- Local emulator, sandbox, test mode, or provider test tooling.

## Dependencies

- Generalized prerequisite: `<secod-generalized-skill>`.
- Framework/mobile prerequisite when applicable: `<secod-framework-or-mobile-skill>`.
- Provider-family prerequisite when useful: `<secod-provider-family>`.

Dependencies provide shared invariants. This adapter owns exact provider APIs and limitations.

## Secure defaults

- Initialize privileged clients only in trusted runtimes.
- Prefer workload identity or short-lived credentials; scope permissions to required actions and resources.
- Enforce user/tenant/resource authorization before provider effects.
- Validate provider-bound and provider-originated data against an explicit schema.
- Verify webhook/event authenticity over the exact raw payload when the provider requires it.
- Use idempotency, deduplication, conditional writes, or reconciliation appropriate to the product.
- Bound timeouts, retries, concurrency, payload size, and cost exposure.
- Minimize sensitive fields in storage, responses, errors, and logs.

## Implementation workflow

1. Confirm the exact provider feature and supported version.
2. Identify the trusted enforcement point and credential boundary.
3. Choose the matching recipe from `references/`.
4. Implement authorization and validation before calling the provider.
5. Implement safe retries, duplicate handling, rollback/reconciliation, and cleanup as applicable.
6. Add unit plus sandbox/emulator/integration tests appropriate to the provider.
7. List only the console or infrastructure steps the implemented code actually requires.

## Implementation recipes

- [`references/<feature>-<runtime>.md`](references/<feature>-<runtime>.md) — <supported SDK/runtime/version>.
- [`references/<event-or-policy>.md`](references/<event-or-policy>.md) — <specific provider boundary>.

Every recipe must include:

- supported versions and assumptions;
- packages, imports, client initialization, and credential source;
- complete safe implementation code or a tightly scoped patch pattern;
- authorization, validation, secrets, persistence, and error behavior;
- timeout, retry, concurrency, idempotency, cleanup, and reconciliation where relevant;
- positive, negative, replay/abuse, and provider-test-mode coverage;
- direct official documentation supporting version-sensitive decisions.

## Unsafe patterns to avoid

- Using a public/client SDK for privileged administration.
- Trusting client-supplied identity, tenant, price, role, object key, or completion state.
- Copying an official quickstart without adding application-level authorization and validation.
- Treating successful request submission as durable business completion.
- Retrying non-idempotent operations without a stable idempotency or deduplication key.
- Logging provider credentials, tokens, signatures, payment data, or model inputs containing secrets.

Replace this generic list with product-specific traps before publication.

## Tests to add

- Authorized success using the provider's supported sandbox/emulator/test mode.
- Rejection of missing identity and cross-tenant/resource access.
- Malformed, oversized, tampered, replayed, or stale input as applicable.
- Duplicate delivery and retry behavior.
- Provider timeout, throttling, partial failure, and out-of-order event behavior.
- Secret absence from untrusted bundles, responses, snapshots, and logs.
- Cleanup, revocation, refund, rollback, or reconciliation behavior as applicable.

## Provider and deployment steps

For each external setting, state:

1. exact provider product and configuration path;
2. minimum secure value/policy;
3. why the code depends on it;
4. a concrete CLI, API, emulator, or console verification step;
5. whether the agent actually performed that verification.

If the setting cannot be inspected, give the user the step without claiming a pass or turning it into a scanner result.

## Official sources

Use [`references/sources.md`](references/sources.md). Include the provider's official documentation homepage, official `llms.txt` or `llms-full.txt` when published, and direct pages for each API, security constraint, and test facility used. Community material may explain context but must not be the sole authority for provider behavior.

## Completion handoff

State the provider feature implemented, security properties enforced, SDK/runtime versions assumed, tests run, and exact external configuration still required.
