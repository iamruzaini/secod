<!-- SECOD template for secod-core. Replace placeholders and remove comments. -->

---
name: secod-core
description: >-
  Route web and mobile coding tasks to the smallest applicable set of SECOD
  secure-implementation skills. Use when adding or changing application features,
  providers, data flows, authentication, storage, payments, messaging, or AI capabilities.
license: Apache-2.0
metadata:
  secod-category: "router"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# SECOD secure implementation router

## Purpose

Understand the current coding task and supply the agent with the generalized, framework, provider, and mobile guidance needed to implement that task securely. Routing should be precise and quiet: activate applicable skills, exclude unrelated providers, and avoid turning an ordinary feature task into a broad audit.

## When to use

Use at the beginning of a web or mobile implementation task when the relevant security skills have not already been selected.

Do not rerun routing repeatedly when the task context and active skill set have not changed.

## Context to inspect

Inspect the request and the smallest relevant part of the repository for:

- application type: web, API, worker, native mobile, React Native/Expo, or Flutter;
- languages, frameworks, runtimes, and versions;
- providers and SDKs present in code or explicitly requested;
- changed feature and data flow;
- authentication, authorization, tenants, ownership, and roles;
- external input, files, secrets, payments, messages, background work, or AI tools;
- deployment target only when it changes implementation choices.

Treat explicit user intent as **Requested**, repository evidence as **Detected**, and unrelated catalog entries as **Not applicable**. These are routing states, not security verdicts.

## Secure defaults

- Select from explicit request and repository evidence, never from provider-name guesswork.
- Choose the smallest skill set that covers the feature's trust boundaries.
- Include transitive prerequisites once and reject dependency cycles.
- Keep unrelated providers and broad audit behavior out of the task.
- Preserve the user's implementation scope while adding necessary secure defaults and tests.

## Implementation workflow

1. Restate the concrete feature being built in one sentence.
2. Identify the trust boundaries crossed by that feature.
3. Select the smallest generalized skill set needed for those boundaries.
4. Add one framework or mobile skill when its implementation model matters.
5. Add provider-family routing only when the provider family is requested or detected.
6. Add exact provider-feature skills for products actually used.
7. Include transitive prerequisites declared by selected skills.
8. Remove duplicates and unrelated providers.
9. Hand the selected skills the same task context; do not ask them to independently audit the entire repository.

## Implementation recipes

- [`references/catalog-routing.md`](references/catalog-routing.md) — canonical signals, exclusions, and dependencies for each release-visible skill.
- [`references/stack-detection.md`](references/stack-detection.md) — evidence rules for frameworks, providers, runtimes, and mobile platforms.

Routing references should stay declarative and testable. Provider implementation code belongs in the selected provider skill.

## Routing rules

| Task signal | Route to | Do not route when |
|---|---|---|
| Authentication, sessions, roles, ownership, tenants | `secod-identity-access` | No identity boundary exists |
| HTTP input, API handlers, webhooks | `secod-inputs-apis` | Purely local trusted computation |
| Files, objects, uploads, user data | `secod-data-files` | No data or file flow changes |
| Payments, subscriptions, entitlements | `secod-payments-billing` | No billing state is involved |
| AI model calls, retrieval, tool use | `secod-ai-api-integrations` | No AI feature is present |
| <framework signal> | `<framework-skill>` | A different framework owns the boundary |
| <provider signal> | `<provider-family-or-feature-skill>` | Provider is neither requested nor detected |

Maintain the complete catalog mapping in a focused routing reference rather than expanding this table indefinitely.

## Dependency closure

For every selected skill:

- include declared prerequisites;
- stop when all prerequisites are already selected;
- reject cycles during validation;
- never infer a provider solely from a generalized requirement;
- prefer a feature-specific provider skill over loading every skill from that provider family.

## Implementation handoff

Pass downstream skills:

- requested outcome;
- relevant stack and versions;
- provider products in scope;
- known trust boundaries and data classification;
- files likely to change;
- unresolved decisions that materially affect implementation.

The normal result is secure code and tests produced by the selected skills—not a routing report. Explain routing only when it helps the user understand a non-obvious choice.

## Unsafe patterns to avoid

- Selecting every provider skill because the request uses the word “cloud.”
- Treating installed but unused packages as conclusive feature evidence.
- Loading a provider family when an exact feature adapter and prerequisites are sufficient.
- Asking every selected skill to rescan the entire repository.
- Reporting routing states as security findings or pass/fail results.

## Tests to add

Test at least:

- a request that activates each catalog skill;
- a similar request that must not activate it;
- mixed-provider projects where only the used provider is selected;
- transitive dependency inclusion;
- duplicate suppression and cycle rejection;
- framework and mobile selection;
- a task with insufficient context that still permits a conservative reversible implementation.

## Provider and deployment steps

The router does not own provider configuration. It should pass implementation-relevant deployment context to selected adapters and let those adapters provide exact configuration and verification steps.

## Official sources

Use [`references/sources.md`](references/sources.md) for the Agent Skills specification and SECOD routing policy. Provider documentation belongs in the selected provider skill, not in the router.
