# Review-time external evidence gates

Apply this reference whenever repository evidence cannot prove provider or deployed state, or any
short-lived client-token mechanism is detected.

## External-evidence register

Create a requested-external-evidence register. For each item record provider, project/account,
environment, endpoint/feature, evidence owner, exact requested artifact, capture time, source URL
or Dashboard/API location, freshness/expiry, affected controls and next verification step.

Use these minimum mappings:

| External fact | Acceptable review-time evidence | Affected controls when absent |
| --- | --- | --- |
| Retention, training-use, ZDR eligibility, region and provider telemetry/payload logging | Current direct official documentation for capability plus matching Dashboard or Management API read for the reviewed project, environment and feature | AI-06; AI-09 for every fallback target; AI-11 for provider/gateway logging |
| Provider/account spend ceiling or alert | Matching Dashboard or Management API read showing amount, scope, currency, reset period and enforcement-versus-alert behavior | AI-02 |
| Provider-side file/vector-store deletion completion | Provider deletion status/result or audit event correlated to the application deletion request and object identifiers | AI-06 |

Official documentation proves provider capability or constraints, not reviewed-account
configuration. Repository configuration proves intent, not deployed provider state. Evidence that
is absent, stale, inaccessible, for another project/environment/feature, or missing correlation
keeps only affected controls `Not verified`. Never infer one provider endpoint's posture from
another.

## Short-lived client-token gate

Perform this provider-specific gate at review time:

1. Route to the matching provider skill and open current direct official documentation for the
   exact realtime/client-token feature. An index, blog, third-party summary or another provider's
   behavior is insufficient.
2. Record provider, feature, direct URL, reviewed date, SDK/API version where stated, token-minting
   authority, expiry/default/max lifetime, use-count or replay constraints, scope/audience and
   configurable session limits. Record `not documented` instead of inventing a value.
3. Compare repository minting code and supplied runtime/Dashboard evidence with every documented
   constraint. Verify long-lived credentials remain server-side and clients cannot broaden token
   scope or session configuration.
4. Mark AI-01 `Not verified` when current official documentation or matching configuration/runtime
   evidence is unavailable, stale, contradictory or does not cover the exact provider feature.

Never record a blanket claim that short-lived client tokens are safe across providers.
