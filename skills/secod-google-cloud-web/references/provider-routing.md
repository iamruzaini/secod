# Google Cloud Web product routing

## Selection rule

Require current-feature evidence: import or SDK call, provider configuration/IaC, runtime binding, route, or explicit user request. Package presence alone is Possible. Route only Confirmed products.

## Adapter map

- Cloud Storage selects secod-google-cloud-storage.
- Firebase products or Firestore Native-mode client Rules selects secod-firebase.
- Unrelated Google Cloud workloads do not select Firebase.

## Shared context

Pass exact product, resolved SDK/tool version, environment, resource/project/account identifiers without secrets, identity model, data classes, trust boundaries, likely files, tests, routing reason, and narrow assumptions.

## Shared defaults

- Use attached service identities or Workload Identity Federation instead of downloaded service-account keys.
- Give each workload dedicated least-privilege IAM scoped to project and resource.
- Separate production projects and locations from development where risk requires it.
- Keep secrets server-side and make public or cross-project access explicit.

## Exclusions

Do not select sibling adapters without product evidence. Do not inspect unrelated account settings. Do not guess plan, Region, deployment state, or APIs.
