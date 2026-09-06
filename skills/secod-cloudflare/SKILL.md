---
name: secod-cloudflare
description: >-
  Route Cloudflare coding tasks to exact product adapters and apply shared account, token, environment, binding, domain, and origin defaults.
license: Apache-2.0
metadata:
  secod-category: "provider-family"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Cloudflare implementation router

## Purpose

Identify exact provider products used by current feature, apply only shared provider defaults, and route exact SDK work to applicable feature adapters. Do not perform account-wide audit.

## When to use

Use for Cloudflare Workers, Pages, Queues, Workflows, Hyperdrive, Vectorize, Workers AI, AI Gateway, Wrangler, bindings, zones, or Cloudflare domains. Package presence alone is possible context, not sufficient activation when current feature does not use provider.

## Context to inspect

Inspect current request, imports and SDK calls, manifest and lockfile versions, provider configuration names, IaC, runtime/deployment target, environment, trust boundaries, and tests. Never collect secret values.

## Secure defaults

- Use scoped API tokens; never default to Global API Key.
- Separate preview and production variables, secrets, bindings, routes, and domains.
- Treat bindings and request metadata as input; enforce application authorization independently.
- Protect origin reachability and keep privileged credentials out of client output.

## Implementation workflow

1. Identify exact provider products used by current feature from code and configuration evidence.
2. Classify each product as Confirmed, Possible, or Absent; route only Confirmed products.
3. Add applicable generalized skills and compute transitive dependency closure through secod-core.
4. Pass product, resolved version, environment, identity, data, boundaries, files, and assumptions to adapters.
5. Let adapters own exact SDK calls and product tests; retain shared defaults across adapters.

## Implementation recipes

- [Provider routing](references/provider-routing.md) — product signals, adapter map, exclusions, and shared context.

## Unsafe patterns to avoid

- Loading every adapter because provider package or account exists.
- Replacing feature implementation with account-wide settings inventory or findings report.
- Inventing SDK calls, product availability, plan behavior, or dashboard state.
- Treating provider authentication, edge controls, or IAM as application authorization.

## Tests to add

Test correct product activation, similar non-trigger, multiple applicable products, transitive dependencies, unused-provider exclusion, missing-version handling, secure generated boundary, and no account-audit output.

## Provider and deployment steps

- Workers selects secod-cloudflare-workers.
- Pages selects secod-cloudflare-pages.
- Queues selects secod-cloudflare-queues.
- Workflows selects secod-cloudflare-workflows.
- Hyperdrive selects secod-cloudflare-hyperdrive.
- Vectorize selects secod-cloudflare-vectorize.
- Workers AI selects secod-cloudflare-workers-ai.
- AI Gateway selects secod-cloudflare-ai-gateway.

If required console setting is inaccessible, provide exact official verification path without claiming it was checked.

## Official sources

Use [source register](references/sources.md). llms.txt indexes support page discovery only; direct product pages govern implementation.

## Completion handoff

State detected products, selected and excluded adapters, shared defaults applied, code/tests changed, and precise external step remaining. Never issue account-wide verdict, scanner report, certification, or whole-application security claim.
