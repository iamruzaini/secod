---
name: secod-runtime-execution
description: >-
  Help coding agents implement process, shell, template, archive, and dynamic execution boundaries without command, argument, or template injection.
license: Apache-2.0
metadata:
  secod-category: "generalized"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Safe runtime execution

## Purpose

Own portable security invariants for safe runtime execution. Provider and framework adapters own exact SDK calls and deployment controls.

## When to use

Use for process execution, shell commands, interpreters, templates, archive extraction, plugins, or dynamic code loading. Do not activate for unrelated documentation or presentation-only changes.

## Context to inspect

Inspect changed feature, trust boundaries, identity and tenant model, sensitive data, installed versions, existing project conventions, nearby tests, and selected provider adapters. Ask only for context repository cannot reveal.

## Security invariants

- Untrusted data never selects executable code, command names, or shell syntax.
- Process arguments use structured APIs and strict allowlists.
- Execution runs with bounded resources and least privilege.

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

- Passing concatenated strings to a shell.
- Using denylist escaping as primary command-injection defense.
- Evaluating templates, expressions, or code from untrusted data.

## Tests to add

Test valid behavior, unauthenticated/unauthorized or cross-tenant denial when applicable, malformed and boundary input, duplicate/concurrent/retried execution, dependency failure, and sensitive error/log redaction.

## Provider and deployment steps

Apply selected provider adapter for exact SDK, console, plan, region, and deployment behavior. Never invent provider APIs. Name inaccessible external configuration and exact verification step without claiming it was inspected.

## Official sources

Use [`references/sources.md`](references/sources.md). Direct primary pages support recipes; documentation indexes or `llms.txt` files may aid discovery but do not replace exact source pages.

## Completion handoff

State invariant implemented, code and tests changed, provider adapter used, assumptions, and precise external action remaining. State inaccessible settings and unexecuted tests accurately; never invent provider APIs or certify application security.
