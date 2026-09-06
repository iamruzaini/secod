---
name: secod-cloudflare-hyperdrive
description: >-
  Help coding agents securely implement Cloudflare Hyperdrive features using version-matched official APIs, secure defaults, and provider-specific tests. Use when Hyperdrive bindings, database connections, Wrangler Hyperdrive configuration, TLS, or pooling.
license: Apache-2.0
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure Cloudflare Hyperdrive implementation

## Purpose

Implement Cloudflare Hyperdrive features securely. Provider-family router supplies shared context; this skill owns exact product decisions and version-qualified SDK/runtime use.

## When to use

Use when Hyperdrive bindings, database connections, Wrangler Hyperdrive configuration, TLS, or pooling. Do not activate from package presence alone when current feature does not use Cloudflare Hyperdrive.

## Context to inspect

Inspect current feature, imports and calls, manifest/lockfile, runtime configuration, environment, identity/tenant model, data classes, trust boundaries, provider-family context, and nearby tests. Never collect secret values.

## Secure defaults

- Authorize every query/object against trusted user, tenant, and ownership state.
- Use parameterized/structured APIs and least-privilege workload credentials.
- Keep data private by default and bound query, upload, result, and connection resources.
- Test cross-tenant, unauthorized, malformed, duplicate, and dependency-failure paths.
- Keep credentials in bindings/secrets, verify database identity with TLS, and authorize/query safely in Worker code.

## Implementation workflow

1. Resolve exact installed SDK/runtime/API version and product features in use.
2. Read version-matched direct official documentation before writing provider calls.
3. Reuse project conventions; implement validation and authorization before provider effect.
4. Add idempotency, limits, safe failure, redaction, and environment separation where applicable.
5. Add successful, denied, cross-tenant, malformed, replay/retry, and provider-failure tests.

## Implementation recipes

- [Supported versions](references/versions.md) — resolve compatible SDK, runtime, and API surfaces.
- [Secure implementation recipe](references/data-access.md) — provider-specific boundaries and coding sequence.
- [Security-focused tests](references/tests.md) — positive, denied, replay, failure, and version tests.

## Unsafe patterns to avoid

- Inventing SDK methods, options, model capabilities, service behavior, or dashboard state.
- Copying examples for another major version or runtime without checking installed version.
- Trusting client-controlled identity, tenant, resource, price, tool, or authority fields.
- Replacing implementation with findings, score, account audit, or certification language.

## Tests to add

Test version-compatible setup, expected success, missing identity, wrong tenant/resource, malformed input, duplicate/replay where applicable, timeout/provider failure, secret/log redaction, and unavailable external configuration.

## Provider and deployment steps

Implement repository-owned code first. For required external settings, name exact official page and verification action. If inaccessible, do not claim setting was checked.

## Official sources

Use [source register](references/sources.md). llms.txt indexes aid discovery only; direct provider documentation governs implementation.

## Completion handoff

State SDK/runtime/API version used, secure boundary implemented, tests run, provider-family defaults applied, assumptions, and exact external step remaining. Never claim whole application or provider account is secure.
