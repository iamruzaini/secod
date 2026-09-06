<!-- SECOD template for a broad provider family and feature router. -->

---
name: <secod-provider-family>
description: >-
  Route <provider family> coding tasks to secure product-specific implementation
  guidance and shared provider defaults. Use when <family detection signals>.
license: Apache-2.0
compatibility: "Requires use of <provider family>; product adapters state SDK and runtime support."
metadata:
  secod-category: "provider-family"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# Secure <provider family> implementation routing

## Purpose

Apply security defaults shared across <provider family> and select only the product adapters needed by the current coding task. This skill coordinates implementation; it does not load every service, inspect the whole cloud account, or replace product-specific guidance.

## When to use

Activate when <provider family> is explicitly requested or detected through:

- official SDK/package imports;
- provider configuration files or infrastructure definitions;
- environment variables or endpoints with clear provider ownership;
- an existing wrapper around a provider service.

Do not infer use from generic terms such as “cloud,” “database,” “auth,” or “storage” alone.

## Context to inspect

- Exact provider products used by the feature.
- SDK, API, CLI, infrastructure, and runtime versions.
- Client credentials, workload identity, service roles, and resource policies.
- Region, tenancy/account/project boundary, and data residency when relevant.
- Existing provider wrappers and local test/emulator strategy.
- Generalized and framework skills already selected.

## Secure defaults

- Use short-lived workload identity or narrowly scoped roles instead of long-lived embedded credentials.
- Separate public client configuration from privileged server credentials.
- Scope permissions to the exact service actions and resources required.
- Encrypt transport and stored sensitive data using provider-supported mechanisms.
- Bound retries, concurrency, execution time, and cost-amplifying operations.
- Redact secrets and sensitive payloads from provider telemetry.

## Product routing

| Detected or requested feature | Select adapter | Shared prerequisites |
|---|---|---|
| <product/feature> | `<secod-provider-product>` | `<generalized-skill>` |
| <product/feature> | `<secod-provider-product>` | `<generalized-skill>` |
| <product/feature> | `<secod-provider-product>` | `<generalized-skill>` |

Keep the full routing map in `references/product-routing.md` when it becomes large.

## Implementation workflow

1. Confirm that the provider is actually in scope.
2. Resolve the exact products and trust boundaries used by the feature.
3. Select product adapters and their transitive prerequisites.
4. Apply family-wide identity, secret, telemetry, retry, and data defaults.
5. Let each product adapter own exact SDK calls, policies, and tests.
6. Return only deployment steps relevant to the implemented feature.

## Implementation recipes

- [`references/workload-identity.md`](references/workload-identity.md) — <supported identity models>.
- [`references/provider-client-boundaries.md`](references/provider-client-boundaries.md) — <public versus privileged clients>.
- [`references/retries-observability.md`](references/retries-observability.md) — <provider-wide behavior>.

Do not duplicate product-specific recipes here.

## Unsafe patterns to avoid

- Selecting all provider services because one SDK is installed.
- Giving broad administrator permissions to simplify local development.
- Shipping service credentials in a web or mobile client.
- Assuming a resource is private because its SDK call originates on the server.
- Treating provider defaults as stable without confirming current official documentation.

## Tests to add

- Product routing selects only requested/detected adapters.
- Missing or excessive permissions fail predictably.
- Privileged credentials cannot reach untrusted clients.
- Retry and duplicate behavior is bounded for provider calls.
- Emulator, local integration, or mocked-contract tests cover the changed provider boundary.

## Provider and deployment steps

State exact role/policy/resource configuration needed by the feature and how the user can confirm it. Do not ask for unrelated account-wide screenshots or claim deployment state was checked without access.

## Official sources

Use [`references/sources.md`](references/sources.md). Include the provider documentation homepage, official `llms.txt` endpoint when published, direct identity/security pages, and direct product pages used by child adapters.

## Completion handoff

State which provider products were selected, what family defaults were applied, which adapters implemented the feature, tests run, and required deployment actions.
