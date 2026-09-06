---
name: secod-core
description: >-
  Route web and mobile implementation tasks to the smallest applicable set of
  SECOD secure-coding skills. Use when building or changing application features,
  frameworks, providers, authentication, data, APIs, files, payments, messaging,
  background work, deployment, or AI integrations.
license: Apache-2.0
metadata:
  secod-category: "router"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# SECOD secure implementation router

## Purpose

Understand the feature being built, identify its security-relevant boundaries, and load only
the SECOD skills needed to implement it securely. Combine generalized guidance with exact
framework and provider adapters, including their transitive dependencies.

Normal output is secure implementation work performed with selected skills. Do not replace the
user's coding task with unrelated review work. Output secure implementation context, not an
application-security certification.

## When to use

Use at the start of a web or mobile coding task when one or more of these change:

- authentication, authorization, accounts, roles, ownership, or tenants;
- API routes, server actions, webhooks, realtime channels, or external input;
- databases, storage, uploads, exports, caches, or sensitive data;
- provider SDKs, cloud services, payments, email, queues, scheduled jobs, or AI;
- framework, runtime, deployment, container, dependency, or secret handling.

Do not activate for prose-only, formatting-only, or unrelated repository maintenance. Do not
rerun routing when task context and selected skill set are already clear and unchanged.

## Context to inspect

Inspect the request first, then the smallest repository scope needed to resolve:

- requested feature and expected user-visible behavior;
- application type: web, API, worker, native mobile, React Native/Expo, or Flutter;
- language, runtime, framework, router, SDK, and resolved versions;
- provider products actually requested or used by the feature;
- server, browser, mobile device, worker, provider, and data-store trust boundaries;
- authentication, tenant, ownership, role, and privileged-operation model;
- sensitive data entering, leaving, stored, logged, or sent to third parties;
- files likely to change and existing wrappers, schemas, tests, and project conventions.

Read environment-variable names from source or committed schemas when useful. Never expose
secret values. Prefer lockfiles and imported APIs over package-range guesses for versions.

Classify routing evidence as:

- **Requested**: user explicitly asks to add or change the technology or feature.
- **Detected**: reachable code or active configuration uses it in task scope.
- **Possible**: package, dormant file, example variable, or weak signal exists without relevant
  use.
- **Not applicable**: no request or repository evidence connects it to the task.

Select skills for Requested and Detected items. A Possible signal alone does not activate a
provider skill unless the current task will use it.

## Secure defaults

- Route by current feature and trust boundaries, not by loading the full catalog.
- Select provider adapters only for Requested or Detected provider products.
- Include generalized skills only when their security invariant affects current implementation.
- Resolve every selected skill's transitive dependencies from `references/catalog.json`.
- Deduplicate selections; reject unknown slugs and dependency cycles.
- Preserve user scope and existing project architecture unless either prevents required secure
  behavior.
- Pass one consistent task-context record to every selected skill.
- Let selected skills produce code and tests; routing itself is not a security result.

## Implementation workflow

1. State the feature being built in one sentence.
2. Inspect relevant manifests, lockfiles, imports, configuration, routes, schemas, and tests.
3. Record stack, resolved versions, provider products, trust boundaries, data, and likely files.
4. Select directly applicable generalized, framework, provider-family, provider-feature, and
   mobile skills using `references/discovery-routing.md`.
5. Compute transitive dependency closure from `references/catalog.json`.
6. Remove duplicates and confirm no unrelated provider entered the closure.
7. Read each selected `SKILL.md`, then only references relevant to current implementation.
8. Give every selected skill the task context defined in `references/task-context.md`.
9. Implement secure code and tests following selected skills and repository conventions.
10. Summarize implementation decisions, tests run, narrow assumptions, and exact external
    configuration still required.

Ask a focused question only when missing context creates materially different architectures or
security outcomes. Otherwise choose a conservative, reversible default and continue.

## Implementation recipes

- [`references/discovery-routing.md`](references/discovery-routing.md) — use to detect task
  signals, select direct skills, exclude unused providers, and compute dependency closure.
- [`references/task-context.md`](references/task-context.md) — use to pass consistent feature,
  stack, version, boundary, data, and file context to selected skills.
- [`references/catalog.json`](references/catalog.json) — use as machine-readable skill and
  dependency inventory. Treat `recommendedBaseline` as legacy migration metadata, not an
  instruction to select every generalized skill.

## Unsafe patterns to avoid

- Loading all generalized skills for every task; select only invariants current work crosses.
- Selecting a provider because its package is installed but unrelated to the feature.
- Inferring deployed provider settings, plans, regions, or enabled services from source files.
- Guessing framework or SDK versions when lockfile or imported API evidence is available.
- Inferring dependencies from prose instead of reading catalog edges.
- Silently dropping unknown dependencies or breaking cycles by removing edges.
- Asking downstream skills to independently rediscover or audit the whole repository.
- Producing routing tables, findings, scores, or readiness decisions instead of doing requested
  implementation work.

## Tests to add

Maintain routing tests that prove:

- every release-visible skill has one positive and one similar negative activation case;
- requested providers are selected and unused providers are excluded;
- framework and provider versions come from repository evidence when available;
- generalized skills are selected from feature boundaries, not as an unconditional baseline;
- transitive dependencies are complete and duplicate-free;
- cycles, unknown slugs, and missing skill directories stop only affected branches;
- identical task context reaches every selected skill;
- ordinary coding tasks produce implementation and test changes, not audit output.

Use intentionally mixed-provider fixtures. For example, a repository containing Firebase and
Stripe must not select either when current task only changes static typography.

## Provider and deployment steps

`secod-core` does not configure provider accounts. Pass provider and deployment context to exact
selected adapters. Those adapters must name required external settings, secure values, and
verification steps.

If repository code cannot establish a deployment setting, state only that exact setting was not
inspected. Continue all supported local implementation work. Do not convert missing access into
a whole-application status or verdict.

## Official sources

Use [`references/sources.md`](references/sources.md). This router relies on Agent Skills
specification for skill discovery, metadata, references, and progressive disclosure. Provider
documentation belongs to provider adapters and should be read only after that provider is
selected.

## Completion handoff

Do not emit a mandatory routing report. When routing choices are useful to explain, state:

- feature and stack understood;
- directly selected and transitive skills;
- important trust boundaries and files passed downstream;
- secure implementation and tests completed by selected skills;
- exact external action or narrow assumption remaining.

Never claim SECOD proved the feature or application secure.
