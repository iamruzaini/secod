---
name: secod-inputs-apis
description: >-
  Help coding agents implement secure API, webhook, realtime, and outbound-request
  boundaries with server-side validation, authorization, injection defenses, SSRF
  controls, bounded resources, and minimal responses.
license: Apache-2.0
metadata:
  secod-category: "generalized"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure inputs and APIs

## Purpose

Implement safe boundaries wherever untrusted data enters code or external data returns. Exact
framework and provider adapters own version-specific request and webhook APIs.

## When to use

Use for HTTP/RPC/GraphQL/WebSocket handlers, server actions, webhooks, file metadata, redirects,
outbound URLs, third-party responses, query construction, and deserialization. Do not activate for
trusted internal values that cross no boundary.

## Context to inspect

Identify request framework, raw/body parsing order, authentication, schema library, side effects,
database/query APIs, outbound network policy, response fields, provider signature mechanism,
payload limits, timeout/retry behavior, and existing tests.

## Secure defaults

- Parse untrusted input with explicit schemas and size limits at boundary.
- Authorize before protected reads or effects.
- Use parameterized APIs and allowlists for identifiers, operations, destinations, and redirects.
- Resolve and validate outbound destinations; block local, private, link-local, metadata, and unsafe
  redirect targets where user-controlled URLs are required.
- Verify provider webhooks over exact required bytes before parsing or mutating state.
- Minimize responses; bound time, payload, pagination, concurrency, and retries.

## Implementation workflow

1. Map input source, parser, trust transition, protected effect, and output.
2. Select framework/provider recipe for exact request API and signature format.
3. Add schema, normalization, size limits, authentication, and authorization.
4. Use safe query/network primitives and define timeout, retry, duplicate, and failure behavior.
5. Add valid, malformed, unauthorized, injection, SSRF, replay, and failure tests as applicable.

## Implementation recipes

- [`references/typescript-api-boundary.md`](references/typescript-api-boundary.md) — TypeScript
  server handler pattern with schema validation and authorization.

## Unsafe patterns to avoid

- Validation only in browser/mobile client.
- String-built SQL, shell, LDAP, XPath, headers, or redirects.
- Fetching arbitrary user URLs with default redirect/DNS behavior.
- Parsing webhook JSON before provider-required raw-body verification.
- Returning provider/database objects without response allowlisting.

## Tests to add

Test valid authorized requests, malformed and oversized bodies, missing/wrong identity, forbidden
fields, injection payloads, internal-network URLs, tampered/replayed webhooks, timeouts, duplicate
delivery, and response minimization.

## Provider and deployment steps

Provider adapters own signature secrets, endpoint registration, network allowlists, and delivery
settings. Give exact setup and verification steps; never invent provider behavior.

## Official sources

Use [`references/sources.md`](references/sources.md) plus exact framework/provider source registers.

## Completion handoff

State boundary, schema, authorization, safe query/network behavior, response shape, tests run, and
external webhook/network setup remaining. No scanner output or certification.
