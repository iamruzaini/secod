---
name: secod-openai
description: >-
  Help coding agents implement OpenAI API features with server-side credentials,
  authorized tools, validated structured output, tenant-isolated data, bounded usage,
  verified webhooks, and privacy-aware logging.
license: Apache-2.0
compatibility: "Requires OpenAI API; inspect current SDK, model, Responses API, tool, and data settings."
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure OpenAI implementation

## Purpose

Build OpenAI features where credentials stay trusted, users/tenants are authorized, model input is
minimized, output is validated, tools reauthorize every effect, and usage/failure is bounded.

## When to use

Use for OpenAI SDK/API, Responses API, structured outputs, tools/function calling, files, retrieval,
webhooks, streaming, realtime, batches, or background responses. Do not activate for other model providers.

## Context to inspect

Resolve SDK/API pattern, model capability, server/client boundary, user/tenant, input/data classes,
retention requirement, tools and effects, files/vector stores, streaming, webhook route, limits,
timeouts/retries, and logging.

## Secure defaults

- Keep project/service credentials server-side and scoped to correct environment/project.
- Authorize user, tenant, model, file, vector store, and tool access before API calls.
- Minimize prompts/files/metadata and keep secrets out of model input and logs.
- Prefer structured outputs with strict schema where application consumes fields.
- Treat model output and tool arguments as untrusted; validate and reauthorize at tool boundary.
- Bound model allowlist, input/output size, tools, timeout, concurrency, retries, and spend.
- Verify OpenAI webhooks with official SDK before processing events.

## Implementation workflow

1. Map user request, tenant data, OpenAI resources, model, tool effects, and returned output.
2. Create trusted server client and enforce access before request.
3. Use supported structured-output/tool API for installed SDK and chosen model.
4. Validate output/tool arguments and reauthorize each consequential action.
5. Add malformed output, prompt-injection, cross-tenant, tool abuse, timeout, and webhook tests.

## Implementation recipes

- [`references/openai-server-tools.md`](references/openai-server-tools.md) — server client,
  structured output, tool authorization, webhook verification, and usage bounds.

## Unsafe patterns to avoid

- Shipping API keys to browser/mobile client.
- Giving model direct unrestricted database, shell, payment, email, or admin access.
- Trusting model JSON because prompt requested a format.
- Mixing tenants in prompts, caches, files, vector stores, threads, or logs.
- Retrying consequential tool effects without idempotency.

## Tests to add

Test allowed request, unauthorized model/resource, schema-invalid output, injected tool argument,
cross-tenant retrieval, secret redaction, timeout/rate failure, duplicate tool effect, invalid webhook,
and bounded fallback behavior.

## Provider and deployment steps

Configure project-scoped credentials, allowed models, budgets/limits, webhook secret, and data controls
as required. State exact uninspected setting; do not claim provider configuration was checked.

## Official sources

Use [`references/sources.md`](references/sources.md); OpenAI `developers.openai.com/llms.txt` helps
discover current pages, while direct guides support APIs.

## Completion handoff

State credential boundary, model/resources, data minimization, validation/tool controls, tests run,
and provider configuration remaining. Never claim AI feature is secure or certified.
