<!-- SECOD template for provider-independent implementation guidance. -->

---
name: <secod-generalized-skill>
description: >-
  Help AI coding agents implement <portable security capability> securely across
  web and mobile stacks. Use when <specific coding-task triggers>.
license: Apache-2.0
metadata:
  secod-category: "generalized"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# <Generalized secure implementation capability>

## Purpose

Provide provider-independent secure defaults and implementation patterns for <capability>. Adapt the pattern to the repository's language and framework without weakening the security invariant.

## When to use

Use for:

- <feature or boundary>;
- <feature or boundary>;
- <feature or boundary>.

Do not use for <nearby concern>; route that work to `<skill>`.

## Context to inspect

- Relevant request path, data flow, and trust boundary.
- Existing framework conventions, shared helpers, and validation libraries.
- Identity, role, ownership, and tenant model.
- Sensitive-data classification and retention requirements.
- Existing tests at the same boundary.
- Provider adapter selected by `secod-core`, if any.

## Security invariants

State a short set of properties that must remain true regardless of stack:

- <Invariant that can be tested>.
- <Invariant that can be tested>.
- <Invariant that can be tested>.

## Secure defaults

- Enforce decisions at a trusted server, backend, worker, or platform boundary.
- Deny or constrain behavior when identity, ownership, validation, or policy context is missing.
- Minimize privileges, exposed data, accepted input, execution time, and retry scope.
- Produce errors useful to the caller without leaking secrets or sensitive internals.
- Make duplicate, concurrent, delayed, and partial execution safe where the feature can encounter them.
- Add tests in the same change as the implementation.

## Implementation workflow

1. Identify the invariant and where it can be enforced.
2. Choose the stack-specific recipe already closest to the repository.
3. Implement validation and authorization before privileged effects.
4. Bound resource use and define safe failure behavior.
5. Add positive, negative, cross-boundary, and regression tests.
6. Apply provider-specific constraints from the selected adapter without duplicating that adapter here.

## Implementation recipes

- [`references/<runtime-or-framework>-recipe.md`](references/<runtime-or-framework>-recipe.md) — <supported context>.
- [`references/<alternative>-recipe.md`](references/<alternative>-recipe.md) — <supported context>.

If no matching recipe exists, implement the invariant using existing project conventions and record a narrow assumption. Do not invent a provider API.

## Unsafe patterns to avoid

- <Tempting shortcut> breaks <invariant>; use <safe pattern>.
- <Tempting shortcut> creates <failure mode>; use <safe pattern>.
- <Tempting shortcut> hides <boundary>; use <safe pattern>.

## Tests to add

- Authorized, valid behavior succeeds.
- Unauthenticated, unauthorized, or cross-tenant behavior fails safely.
- Invalid and boundary-value input cannot reach the protected effect.
- Duplicate/concurrent/retried execution preserves the invariant when applicable.
- Errors, logs, and responses do not disclose protected data.
- The secure behavior fails if the implementation regresses.

## Provider and deployment steps

Generalized skills own portable security invariants. Provider skills own exact SDK calls, platform settings, and provider-specific limitations. When both apply, combine them; do not replace one with the other.

Include external configuration only when the generalized implementation depends on it. Name the exact action and verification method without implying that inaccessible settings were checked.

## Official sources

Use [`references/sources.md`](references/sources.md). Prefer standards, framework security documentation, and primary technical sources directly supporting the implementation. Mark source review state in the source register; do not turn it into an application pass/fail result.

## Completion handoff

Summarize the invariant implemented, code and tests changed, provider adapter applied, and any precise deployment action remaining. Do not emit a mandatory findings report.
