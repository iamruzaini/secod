---
name: secod-ai-api-integrations
description: >-
  Help coding agents implement provider-independent AI, RAG, streaming, file, and tool features with protected credentials, tenant isolation, constrained outputs, and authorized effects.
license: Apache-2.0
metadata:
  secod-category: "generalized"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure AI feature implementation

## Purpose

Own portable security invariants for secure ai feature implementation. Provider and framework adapters own exact SDK calls and deployment controls.

## When to use

Use for model APIs, chat, RAG, embeddings, vector search, streaming, realtime, AI files, agents, or tool execution. Do not activate for unrelated documentation or presentation-only changes.

## Context to inspect

Inspect changed feature, trust boundaries, identity and tenant model, sensitive data, installed versions, existing project conventions, nearby tests, and selected provider adapters. Ask only for context repository cannot reveal.

## Security invariants

- Model input and output remain untrusted across every application boundary.
- Retrieval, memory, files, and tools preserve caller and tenant authorization.
- Consequential effects require deterministic server policy and appropriate confirmation.

## Secure defaults

- Enforce policy at trusted server, worker, database, or provider boundary.
- Minimize accepted input, authority, sensitive data, resource use, and failure scope.
- Deny or stop safely when required identity, ownership, validation, or policy context is missing.
- Add positive, negative, boundary, retry, and regression tests in same change.

## Implementation workflow

1. Trace feature from untrusted input through protected effect and persistent state.
2. Resolve stack versions and reuse established project abstractions.
3. Implement invariant before privileged effect; keep provider SDK details in selected adapter.
4. Define bounded failure, retry, rollback, and observability behavior where applicable.
5. Add tests proving allowed behavior and meaningful rejection paths.

## Implementation recipes

- [`references/secure-patterns.md`](references/secure-patterns.md) — detailed portable implementation patterns.
- [`references/tests.md`](references/tests.md) — positive, rejected, retry, and failure-path tests.

## Unsafe patterns to avoid

- Letting model text or tool arguments directly select privileged effects.
- Retrieving across tenants or placing secrets in prompts.
- Assuming system prompts, schema mode, or model alignment is authorization.

## Tests to add

Test valid behavior, unauthenticated/unauthorized or cross-tenant denial when applicable, malformed and boundary input, duplicate/concurrent/retried execution, dependency failure, and sensitive error/log redaction.

## Provider and deployment steps

Apply selected provider adapter for exact SDK, console, plan, region, and deployment behavior. Never invent provider APIs. Name inaccessible external configuration and exact verification step without claiming it was inspected.

## Official sources

Use [`references/sources.md`](references/sources.md). Direct primary pages support recipes; documentation indexes or `llms.txt` files may aid discovery but do not replace exact source pages.

## Completion handoff

State invariant implemented, code and tests changed, provider adapter used, assumptions, and precise external action remaining. State inaccessible settings and unexecuted tests accurately; never invent provider APIs or certify application security.
