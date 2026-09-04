# Trigger case: secod-ai-api-integrations

Positive prompt: `Use secod-ai-api-integrations to review this project.`

Negative prompt: a request outside this skill's stated applicability must not claim coverage.

Evidence-boundary case: review an AI integration with repository configuration but no provider
Dashboard/API export. Provider retention/training/ZDR/telemetry, spend ceiling and provider-side
deletion completion remain `Not verified` only for their mapped controls, with exact requested
artifacts and next steps.

Client-token case: review a realtime path using a short-lived client token. Require current direct
official documentation for the exact provider feature and matching implementation/configuration;
never generalize from another provider.

Fixture-reporting case: all referenced Markdown fixture plans must be reported as
`artifact_type: documentation_only`, `execution_status: not_executed`.
