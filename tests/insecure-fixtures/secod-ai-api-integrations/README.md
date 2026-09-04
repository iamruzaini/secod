# Insecure fixture plan: secod-ai-api-integrations

Create a minimal reproducible unsafe case for the control requirements in the skill contract. Include a missing-evidence case and, where applicable, a partial-failure or replay case.

Fixture status:

- `artifact_type: documentation_only`
- `execution_status: not_executed`
- No executable harness or application fixture exists in this directory.
- Reading or reviewing this Markdown plan never counts as execution.

Required planned cases:

- Repository-only AI integration with no Dashboard/API proof for provider retention, training use,
  ZDR, telemetry, spend ceilings or provider-side deletion completion.
- Realtime integration using a short-lived client token but lacking current direct official
  documentation for the exact provider mechanism.
- Partial deletion leaving provider/vector-store state pending or uncorrelated.
- Fallback provider with unverified retention/training/telemetry parity.
