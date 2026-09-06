---
name: secod-ship-check
description: >-
  Help coding agents finish a security-sensitive implementation by checking changed feature code,
  selected-skill invariants, tests, accidental secrets, and external configuration handoffs. Use when user
  asks to finish, verify, or summarize security work for a feature; do not issue launch verdicts.
license: Apache-2.0
metadata:
  secod-category: "task-completion"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Complete secure implementation

## Purpose

Close current coding task without turning SECOD into a scanner or certification gate. Check only
changed feature, invariants supplied by already-selected skills, tests, accidental secrets, and
external configuration introduced by that feature.

## When to use

Use after implementing a security-sensitive feature or when user explicitly requests implementation
verification. Do not activate for unrelated documentation, product copy, or account-wide auditing.

## Context to inspect

Inspect requested feature, files changed during the current task, selected SECOD skill instructions,
tests added or executed, changed content that could contain secrets, and external provider actions
introduced by this feature.

## Secure defaults

- Use already-selected skills; do not start new repository-wide routing or review.
- Check changed feature against invariants those selected skills require.
- Run relevant tests and report exact commands and results.
- State unexecuted tests as unexecuted.
- Check changed code, configuration, fixtures, and logs for accidentally introduced secrets.
- Provide exact provider setting, environment, and official verification path when external work remains.
- Ignore unrelated repository conditions unless current feature directly depends on them.

## Implementation workflow

1. Establish current task boundary from user request and changed files.
2. Check only selected-skill invariants that apply to changed feature.
3. Check changed content for secrets or privileged credentials.
4. Run tests added for feature and smallest relevant existing checks.
5. Correct in-scope omissions when user requested implementation.
6. Record exact external configuration handoff without claiming it was inspected.
7. Summarize changed feature, invariants, secret check, tests, and remaining external action.

## Implementation recipes

- [Completion checklist](references/completion-checklist.md) — implementation and test handoff.
- [Official sources](references/sources.md) — sources governing completion behavior.

## Unsafe patterns to avoid

- Blocking implementation because unrelated provider or production evidence is absent.
- Assigning severity, broad findings, scores, or launch-readiness status to ordinary coding work.
- Claiming an inaccessible external setting was inspected.
- Claiming documentation-only tests executed.
- Inventing provider APIs or certifying application security.

## Tests to add

Test activation after implementation, non-activation for unrelated work, selected-skill invariant
coverage, tests added/executed, accidental-secret detection, missing-context handling, and exact
external handoff. Include unrelated repository defects and confirm they do not block task handoff.

## Provider and deployment steps

Name external setting, provider project/account, environment, official page, and verification
action. Never claim completion of an action the agent did not perform.

## Official sources

Use [sources.md](references/sources.md). Direct official pages support provider actions; documentation
indexes only help locate those pages.

## Completion handoff

Return concise implementation summary: changed feature/files, selected-skill invariants checked,
secret-check result, tests added/executed with results, and exact external action remaining. No
application-security certification or shipping decision.
