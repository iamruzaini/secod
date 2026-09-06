# Cloudflare product routing

## Selection rule

Require current-feature evidence: import or SDK call, provider configuration/IaC, runtime binding, route, or explicit user request. Package presence alone is Possible. Route only Confirmed products.

## Adapter map

- Workers selects secod-cloudflare-workers.
- Pages selects secod-cloudflare-pages.
- Queues selects secod-cloudflare-queues.
- Workflows selects secod-cloudflare-workflows.
- Hyperdrive selects secod-cloudflare-hyperdrive.
- Vectorize selects secod-cloudflare-vectorize.
- Workers AI selects secod-cloudflare-workers-ai.
- AI Gateway selects secod-cloudflare-ai-gateway.

## Shared context

Pass exact product, resolved SDK/tool version, environment, resource/project/account identifiers without secrets, identity model, data classes, trust boundaries, likely files, tests, routing reason, and narrow assumptions.

## Shared defaults

- Use scoped API tokens; never default to Global API Key.
- Separate preview and production variables, secrets, bindings, routes, and domains.
- Treat bindings and request metadata as input; enforce application authorization independently.
- Protect origin reachability and keep privileged credentials out of client output.

## Exclusions

Do not select sibling adapters without product evidence. Do not inspect unrelated account settings. Do not guess plan, Region, deployment state, or APIs.
