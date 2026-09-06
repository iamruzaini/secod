<!--
SECOD base authoring contract. Do not install this file as a skill.
Choose a specialized template whenever one applies.
Replace bracketed placeholders and remove all authoring comments.
-->

---
name: <skill-name>
description: >-
  Help AI coding agents implement <security outcome> securely. Use when
  <concrete feature, technology, or coding-task triggers>.
license: Apache-2.0
metadata:
  secod-category: "<router|generalized|framework|provider-family|provider-feature|mobile|task-completion>"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# <Human-readable skill title>

## Purpose

Help the coding agent build <feature or capability> with <important security properties> from the start. Produce implementation decisions, code changes, and tests that fit the project's existing architecture.

This skill does not certify the application, perform a broad security audit, or claim that inaccessible deployment settings were checked.

## When to use

Use this skill when the task includes:

- <specific trigger>;
- <specific trigger>;
- <specific trigger>.

Do not activate it merely because <similar but non-applicable condition>. Route to `<other-skill>` when <boundary>.

## Context to inspect

Before editing, identify only what is needed for this task:

- framework, runtime, language, and relevant versions;
- server, client, worker, device, and provider trust boundaries;
- authentication, authorization, tenant, and ownership model;
- data classification and persistence path;
- existing wrappers, validation libraries, tests, and project conventions;
- provider products and SDKs actually used.

If a fact is missing, choose a conservative reversible default or ask only when the choice would materially change the implementation.

## Secure defaults

- <Default and why it is safe>.
- <Default and why it is safe>.
- <Default and why it is safe>.
- Preserve the repository's established abstractions unless they weaken the required security property.
- Keep secrets and privileged credentials outside untrusted clients.
- Minimize collected, returned, persisted, and logged sensitive data.

## Implementation workflow

1. Map the requested data flow and trust boundary.
2. Select the smallest applicable recipe from `references/`.
3. Decide authorization, validation, secret handling, and failure behavior before writing the happy path.
4. Implement at the boundary that can enforce the decision reliably.
5. Add positive, negative, and abuse-oriented tests with the code change.
6. Check provider or deployment steps only when the feature depends on them.
7. Summarize the secure decisions, tests run, and any exact follow-up the user must perform.

## Implementation recipes

Use these focused recipes:

- [`references/<recipe>.md`](references/<recipe>.md) — <when to use it>.
- [`references/<recipe>.md`](references/<recipe>.md) — <when to use it>.

Each recipe must state supported versions or assumptions, imports/packages, trust boundaries, authorization, validation, secrets, persistence, failure behavior, tests, and direct official sources.

## Unsafe patterns to avoid

- <Unsafe shortcut> because <concrete failure mode>; use <safe alternative>.
- <Unsafe shortcut> because <concrete failure mode>; use <safe alternative>.
- <Unsafe shortcut> because <concrete failure mode>; use <safe alternative>.

Avoid generic warnings without an implementation consequence.

## Tests to add

Add the tests relevant to the changed behavior:

- expected authorized success;
- rejected unauthenticated or unauthorized access;
- malformed, oversized, replayed, or adversarial input as applicable;
- tenant or ownership isolation;
- timeout, retry, duplicate delivery, and partial-failure behavior as applicable;
- secret and sensitive-data absence from client bundles, responses, and logs;
- cleanup, rollback, revocation, or reconciliation behavior as applicable.

Prefer executable tests. If only a manual deployment check is possible, label it as a user action rather than implying it ran.

## Provider and deployment steps

Include this section only for settings outside repository code.

1. Name the exact console, configuration surface, or command.
2. State the secure value and why the implementation depends on it.
3. Give a concrete verification method.
4. If access is unavailable, say what was not inspected; do not convert that into a whole-project verdict.

## Official sources

Use [`references/sources.md`](references/sources.md). Prefer direct official documentation for the exact feature and version. Record an official documentation homepage and official `llms.txt`/`llms-full.txt` endpoint when the provider publishes one, but do not substitute an index file for the direct page supporting a recipe.

## Completion handoff

Report:

- what secure behavior was implemented;
- which files and trust boundaries changed;
- which tests were added and run;
- any provider/deployment action still required;
- any narrow assumption that materially affects the implementation.

Do not emit a mandatory findings table, risk score, pass/fail certification, or repository-wide security conclusion.
