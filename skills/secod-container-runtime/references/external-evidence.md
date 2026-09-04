# External evidence closure

Use this reference only when an authorized operator supplies evidence or grants read-only access.
Repository configuration remains useful evidence of intent, but it does not prove live cluster or
registry state.

## Bundle metadata

Require one bundle per environment and cluster/registry boundary. Record:

- environment name, cluster and registry identifiers, and namespace scope;
- UTC collection time, collector identity or role, and read-only method used;
- Kubernetes/server and policy-engine versions where applicable;
- deployment or GitOps revision and rollout time covered by the bundle;
- command/API source for every artifact, plus any omitted or redacted fields.

Do not collect Kubernetes Secret objects, decoded secret values, registry credentials, tokens,
connection strings, or full environment-variable blocks. Redact sensitive values before evidence
enters a report. Names, references, digests, rules, status fields, and policy decisions are enough.

## Evidence matrix

### Cluster-enforced admission and Pod Security

Collect namespace names and Pod Security labels; admitted pod security contexts; relevant
`ValidatingAdmissionPolicy`, bindings, and validating webhook configuration; policy-engine
version/configuration; and time-correlated allow/deny decisions for protected namespaces. A
namespace label or policy manifest alone proves desired configuration only. Active enforcement
needs a current decision record or an explicitly authorized server-side dry-run rejection. One
rejection does not prove all namespaces are covered; reconcile selectors and bindings against the
complete protected namespace inventory.

Supports controls 4, 5, 9, and 10.

### Live RBAC

Collect ServiceAccounts, Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings with names,
namespaces, rules, subjects, and role references. Map every workload ServiceAccount to effective
grants, including grants inherited through groups or cluster-scoped bindings. Where permitted,
include read-only `kubectl auth can-i --list --as=system:serviceaccount:<namespace>:<name>` output.
Absence from a namespace RoleBinding is not proof of least privilege until cluster-scoped and
aggregated grants are reconciled.

Supports control 9. Any production workload running as root and effectively bound to
`cluster-admin` is `Do not ship`.

### NetworkPolicy enforcement

Collect live NetworkPolicy objects, namespace and pod labels used by their selectors, workload
ports, and CNI/provider evidence that Kubernetes NetworkPolicy is enforced for the reviewed
cluster/version. Reconcile every selected pod against default-deny and required allow policies.
Policy objects without CNI enforcement evidence remain **Not verified**. Connectivity-test logs
may prove enforcement only when their source/destination, namespace, policy revision, timestamp,
and expected denied/allowed outcomes are recorded. Starting test pods requires explicit
authorization.

Supports control 6.

### Deployed image digests

Collect desired controller image references plus each admitted/running pod's `image`, `imageID`,
owner UID, pod UID, namespace, and rollout revision. Normalize runtime-specific `imageID` forms to
the `sha256:` digest without discarding the original value. Map build digest, registry artifact,
deployment reference, and running pod 1:1. Tag-only references, missing pod status, old ReplicaSet
pods, or mixed digests during an incomplete rollout keep affected workloads **Not verified**.

Supports control 1.

### Registry scan results

Collect the registry/repository, exact image digest, scan completion time, scanner and database
version, result status, severity counts, policy threshold, exception references, and deploy-gate
outcome. Reports keyed only by tag do not prove the deployed artifact was scanned. A scan wired in
CI proves integration; a current successful report for the exact running digest proves result
coverage. Route vulnerability disposition and exception quality to
`secod-vulnerability-management`.

Supports control 2.

### Signature-policy activity

Collect signer trust policy, namespace/workload selectors, failure mode, admission-controller
health/version, and time-correlated allow and deny decisions containing image digests and policy
revision. Redact identity or infrastructure details not needed for verification. Installed or
audit-only policy is not enforcement. Passing requires fail-closed policy configuration plus
activity evidence for protected scope; missing activity or incomplete selector coverage remains
**Not verified**.

Supports control 10.

## Read-only collection examples

Use a named context explicitly and capture stdout, stderr, command, exit status, and UTC time.
These commands avoid Secret reads but outputs still require operator review before sharing.

```sh
kubectl --context <context> version -o json
kubectl --context <context> get namespaces -o custom-columns='NAME:.metadata.name,LABELS:.metadata.labels'
kubectl --context <context> get serviceaccounts,roles,rolebindings,clusterroles,clusterrolebindings -A -o json
kubectl --context <context> get networkpolicies -A -o json
kubectl --context <context> get deployments,statefulsets,daemonsets,jobs,cronjobs -A -o custom-columns='KIND:.kind,NAMESPACE:.metadata.namespace,NAME:.metadata.name,GENERATION:.metadata.generation,IMAGES:.spec.template.spec.containers[*].image'
kubectl --context <context> get pods -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,UID:.metadata.uid,OWNER:.metadata.ownerReferences[0].uid,SA:.spec.serviceAccountName,IMAGES:.spec.containers[*].image,IMAGE_IDS:.status.containerStatuses[*].imageID'
kubectl --context <context> get validatingadmissionpolicies,validatingadmissionpolicybindings -o custom-columns='KIND:.kind,NAME:.metadata.name,GENERATION:.metadata.generation,POLICY:.spec.policyName,ACTIONS:.spec.validationActions'
kubectl --context <context> get validatingwebhookconfigurations -o custom-columns='NAME:.metadata.name,WEBHOOKS:.webhooks[*].name,FAILURE_POLICY:.webhooks[*].failurePolicy,NAMESPACE_SELECTOR:.webhooks[*].namespaceSelector'
kubectl --context <context> auth can-i --list --as=system:serviceaccount:<namespace>:<service-account> -n <namespace>
```

The examples collect identity and image correlation only. Collect admitted security contexts,
resources, ports, and selectors with similarly field-limited output or an operator-sanitized
export. Do not export full workload JSON: it can contain literal environment values, arguments,
commands, annotations, and unrelated status messages.

Registry and policy products differ. Prefer their authenticated read-only API or signed export;
record exact command/API endpoint and response status. Never invent a provider command. Route to
the matching provider adapter when live catalog discovery identifies one.

## Acceptance and reconciliation

For each artifact, verify provenance, freshness relative to the deployment/policy revision,
environment identity, complete scope, and internal consistency. Record hashes for retained exports
where practical. A screenshot must show the product, environment, scope, timestamp, and relevant
fields; otherwise request an API/CLI export.

Assign evidence only to the workloads and controls it directly covers. If repository intent and
live state differ, record `Conflicting`, keep the control **Not verified**, identify drift owner,
and request a post-reconciliation bundle. External evidence can close a control, never erase a
repository-confirmed blocker.
