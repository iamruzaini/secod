<!-- SECOD template for secod-ship-check. This is a scoped task check, not certification. -->

---
name: secod-ship-check
description: >-
  Confirm that security-relevant implementation work for the current feature is
  complete before handoff. Use near task completion after SECOD-guided code and tests exist.
license: Apache-2.0
metadata:
  secod-category: "task-completion"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# SECOD task completion check

## Purpose

Check that the feature changed in the current task includes the secure decisions, code, tests, and deployment handoff required by its selected SECOD skills. This is not a repository-wide audit, vulnerability scan, release approval, or statement that the application is secure.

## When to use

Use near completion when:

- code or configuration was changed for a security-relevant feature;
- applicable SECOD skills have already guided the implementation;
- the agent is preparing to hand the work back to the user.

Do not activate for explanation-only tasks or use it as a substitute for the implementation skills.

## Context to inspect

- The user's requested feature and acceptance criteria.
- Files changed during the task.
- Security invariants declared by the selected skills.
- Tests added or updated for this feature.
- Provider/deployment actions introduced by this implementation.
- Relevant command output already available in the task.

Do not expand into unrelated repository areas unless the changed feature directly depends on them.

## Secure defaults

- Keep the check limited to the feature and files changed in the current task.
- Use executable test evidence when available.
- Distinguish code/configuration completed locally from external actions left to the user.
- Fix safe in-scope omissions when authorized; do not expand into unrelated remediation.
- Describe concrete limitations without scoring or certifying the application.

## Implementation workflow

1. Reconstruct the trust boundary and security invariants for the changed feature.
2. Confirm each invariant is represented in implementation code or required configuration.
3. Confirm positive, negative, and abuse-oriented tests exist where executable testing is practical.
4. Run the smallest relevant checks permitted by the task.
5. Confirm secrets and sensitive data were not introduced into untrusted code, fixtures, logs, or output.
6. Identify exact provider/deployment actions that could not be performed locally.
7. Fix in-scope omissions when authorized; otherwise give a concrete follow-up.

## Implementation recipes

- [`references/feature-handoff.md`](references/feature-handoff.md) — reconstruct selected skills, invariants, changed boundaries, and evidence.
- [`references/external-actions.md`](references/external-actions.md) — report provider or platform actions without implying they were performed.

This skill checks implementation produced by other skills; it must not create a second audit framework.

## Completion criteria

The task is ready for handoff when:

- requested secure behavior is implemented at the correct trust boundary;
- relevant tests pass;
- unsafe alternatives documented by selected skills were not introduced;
- version-sensitive provider/framework APIs are supported by official sources;
- external actions are clearly separated from actions actually completed;
- remaining assumptions are narrow and visible.

These criteria describe task completion, not application security certification.

## Unsafe patterns to avoid

- Expanding a focused feature task into an unsolicited repository-wide review.
- Treating a documentation-only test plan as an executed test.
- Marking inaccessible provider settings as passed.
- Converting unrelated pre-existing issues into blockers for the current handoff.
- Claiming the feature or application is secure, certified, or vulnerability-free.

## Handoff format

Report concise implementation evidence:

- secure behavior implemented;
- important files/boundaries changed;
- tests and commands run with results;
- exact provider/deployment action remaining;
- narrow limitation or assumption, if any.

Do not generate severity tables, broad findings, scores, “passed security,” or certification language.

## Tests to add

Test this skill against:

- a complete secure feature with passing tests;
- missing authorization or negative tests within the changed scope;
- a documentation-only test plan incorrectly presented as executed;
- an inaccessible provider setting;
- unrelated pre-existing repository issues that must not expand task scope;
- a request to certify the whole application, which must be declined or reframed.

## Provider and deployment steps

Carry forward only external actions introduced by the changed feature. Name the exact setting, secure value, verification procedure, and whether it was performed. Do not request unrelated account-wide evidence.

## Official sources

Use [`references/sources.md`](references/sources.md) for SECOD's implementation and evidence-boundary policies. Feature-specific sources remain owned by the selected implementation skills.
