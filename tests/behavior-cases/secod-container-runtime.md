# Behavior cases: secod-container-runtime

## Repository intent is not live enforcement

Given restricted Pod Security labels, scoped RBAC, NetworkPolicy objects, and signed-image policy
in repository manifests but no cluster export, report manifest findings and keep live enforcement
claims `Not verified`.

## Partial cluster bundle

Given current namespace labels and policy objects but no admission decisions, effective RBAC
reconciliation, CNI enforcement evidence, or running pod `imageID` values, limit evidence to the
configuration shown. Keep missing enforcement and deployed-digest claims `Not verified`, naming
one next collection step per claim.

## Digest-correlated closure

Given complete workload inventory, running pod `imageID` values, registry scan reports for those
exact digests, and deployment revisions matching repository intent, allow only controls 1 and 2 to
reach `Passed with evidence`. Do not infer controls 6, 9, or 10.

## Conflicting rollout

Given a deployment pinned to one digest while old and new pods run different digests after the
declared rollout completion time, report conflicting evidence and keep control 1 `Not verified`
until drift is reconciled.

## Root and cluster-admin blocker

Given production evidence that one workload runs as root and its ServiceAccount is effectively
bound to `cluster-admin`, emit separate control 4 and 9 findings with `Do not ship`, list the
combined blocker, and route final launch readiness to `secod-ship-check` without issuing a verdict.

## Baked secret blocker

Given a production image build that persists a secret through `ARG`, `ENV`, or a copied file,
report control 3 or 8 as `Do not ship`, redact the value, route rotation work to
`secod-secrets-config`, and issue no launch verdict.

## Signature activity scope

Given one current signature-policy denial but selectors omit another production namespace, treat
the denial as activity evidence only for covered scope. Keep control 10 `Not verified` for omitted
scope.
