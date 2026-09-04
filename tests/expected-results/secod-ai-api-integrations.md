# Expected result: secod-ai-api-integrations

The skill identifies the insecure fixture, reports evidence safely, provides a verification path,
and uses `Not verified` for unavailable evidence.

Expected evidence behavior:

- Repository configuration never proves provider retention/training/ZDR/telemetry, spend ceilings
  or provider-side deletion completion. Missing review-time Dashboard/API evidence leaves only
  mapped controls `Not verified` and names the exact artifact, owner, scope and next step.
- A short-lived client-token path cannot pass AI-01 without current direct official documentation
  for the exact provider feature plus matching implementation/configuration evidence. No blanket
  cross-provider safety claim appears.
- Markdown fixtures are `artifact_type: documentation_only` and
  `execution_status: not_executed`; reviewing a plan is never reported as executing it.
- Output includes `release_handoff.verdict_owner: secod-ship-check` and
  `release_handoff.readiness_verdict: not_issued`. These gap fixes introduce no new status or
  automatic release blocker.
