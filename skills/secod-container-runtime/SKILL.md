---
name: secod-container-runtime
description: Review container images, Docker/Compose builds, Kubernetes/Helm/Terraform workload definitions, and runtime configuration so every deployed workload is traceable to a digest-pinned image, runs non-root with dropped capabilities, and is network- and resource-bounded. Triggers include `Dockerfile*`, `compose.yaml`/`docker-compose.*`, `.dockerignore`, Kubernetes manifests or `kustomization.yaml`, Helm `Chart.yaml`/`values*.yaml`, Terraform/OpenTofu container resources (`docker_*`, `kubernetes_*`), CI steps that build/push/deploy images, image registry references, and container runtime hardening requests; package presence alone is Candidate.
---

# Container Runtime Security

## Mission

Make each deployed containerized workload traceable to an immutable, scanned, digest-pinned
image; run it non-root with minimal capabilities; bound its network exposure and compute
consumption; and keep build-time and runtime secrets out of image layers.

Repository-only review cannot prove what actually runs in a cluster: enforced Pod Security
admission, live RBAC bindings, effective NetworkPolicy enforcement, node seccomp defaults,
registry scan results, admission-controller signature verification, or the deployed image
digest per environment. Those require cluster/Dashboard/API or human-supplied evidence.
`secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls: image identity/pinning/provenance wiring, image-scan integration at the
container layer, build-secret handling in layers, non-root execution, capability/filesystem/
seccomp containment, port/network restriction, per-workload resource bounds, runtime secret
injection mechanics, Kubernetes RBAC/ServiceAccount/Pod Security configuration, and
signed-image admission review where available (`PROVISIONAL-container-runtime-1` through
`PROVISIONAL-container-runtime-10` below).

Excluded controls (owned elsewhere):

- OS command/template injection inside containers and least-privilege process invocation:
  `secod-runtime-execution`; this skill owns only the container/Kubernetes privilege envelope.
- Secret values, classification, rotation, source/history hygiene: `secod-secrets-config`;
  this skill owns only how manifests and builds inject or leak them at the container layer.
- Scanner program governance, SBOM/provenance attestation lifecycle, triage SLAs:
  `secod-vulnerability-management`; this skill's image findings route there for triage.
- Registry trust, CI token minimization, Action pinning, artifact/release integrity mechanics:
  `secod-packages-delivery`.
- Request-level rate limits, quotas, cost ceilings per user/tenant: `secod-abuse-limits`;
  this skill owns per-workload CPU/memory/compute bounds only.
- Managed platform behavior (GKE/AKS/Cloud Run/Apps-class control planes):
  matching cloud/provider adapter; resolve exact slugs from the live `secod/catalog.json`.
- Launch verdict aggregation: `secod-ship-check`.

Direct dependencies (copied exactly from `secod/catalog.json`): `secod-core`.

Conditional routes (only when detected): cloud/container-platform adapters when their managed
runtime is Active or Likely; `secod-vulnerability-management` whenever image-scan findings
exist; `secod-secrets-config` when build/runtime secrets need value-lifecycle work;
`secod-runtime-execution` for process execution inside workloads. No skill conditionally
routes into this one beyond `secod-core`.

## Required inputs

Repository inputs: all `Dockerfile*` and `.dockerignore` files; Compose files including
overrides/profiles; Kubernetes YAML/JSON, `kustomization.yaml`, overlays; Helm charts,
`values*.yaml`, rendered templates where committed; Terraform/OpenTofu container resources;
CI workflows that build, tag, scan, push, or deploy images; registry/image references across
manifests and code; base-image names/tags; entrypoint/CMD/users declared in images; health
checks and probes; committed test fixtures.

Version/environment inputs: exact engine/orchestrator versions per environment; separate
development, preview, staging, and production inventories of images (digest, not tag),
workload definitions, and namespace/project boundaries.

Cluster/provider/dashboard/API evidence (commonly unavailable repository-only — label as such):
enforced namespace Pod Security labels; effective RBAC Role/RoleBinding contents; live
NetworkPolicy objects and CNI enforcement support; deployed pod security contexts as admitted;
node/default seccomp profile; registry vulnerability-scan results and image signatures;
admission controllers verifying signatures; actual running image digests.

Human-supplied evidence: authorized read-only cluster exports (`kubectl get ... -o yaml`),
Dashboard screenshots/exports, registry scan reports, admission policy configuration,
Helm render output from the deploy pipeline.

Absent, stale, conflicting, or inaccessible evidence is **Not verified**; never inferred from
package presence.

## Applicability and discovery

Group signals:

- Package/SDK: Docker/BuildKit usage in CI, `helm`, `kustomize`, compose CLIs, Terraform
  `docker_*`/`kubernetes_*` providers, operator/CRD controllers in manifests.
- Image references: `image:` fields, FROM lines, tags versus `sha256:` digests, `latest`
  or mutable tags, private registries.
- Configuration: securityContext blocks, resource requests/limits, probes, ports, volumes,
  ServiceAccounts, RBAC objects, NetworkPolicy objects, Secret references, namespace labels.
- Deployment/provider evidence: cluster API/dashboard state, registry metadata, deploy logs,
  GitOps repositories showing what is applied.

Classification:

- `Candidate`: Dockerfile present but never built/deployed, example manifest, commented-out
  Helm values, weak signal only.
- `Likely`: build/deploy pipeline or manifests exist and correlate with use, but deployed
  runtime/admission/enforcement state is unverified.
- `Active`: repository artifacts correlate with cluster, registry, Dashboard, or API evidence
  (applied manifests, live digests, enforced policies).

Maintain separate development, preview, staging, and production inventories. Conflicting or
shared environment signals (same credentials/namespace/image across environments) are
**Not verified** until reconciled.

## Review workflow

1. Inventory environments and trust boundaries: enumerate every image reference, build target,
   deploy target, namespace/project, and registry per environment. Parallelizable read-only.
2. Correlate active features and flows: map each workload to its manifest source, build
   pipeline, and deployment evidence; classify Candidate/Likely/Active. Parallelizable after
   step 1 completes for that root.
3. Verify applicable controls below in order, resolving platform adapters from the live catalog.
4. Run safe negative tests: local static checks on Dockerfiles/manifests, client-side dry-run
   rendering (`helm template`, `kubectl kustomize`, `terraform validate`) against committed
   files only. No cluster mutation without explicit authorization.
5. Classify evidence, emit one finding per applicable control, route findings, hand off to
   `secod-ship-check`.

## External evidence closure

When cluster or registry evidence is available, read
`references/external-evidence.md` and apply its collection matrix and acceptance rules. Use
only authorized read-only exports. Do not query Secret values, mutate cluster resources, start
test pods, or run server-side admission probes without explicit authorization.

Reconcile three layers per environment and workload: repository intent, admitted workload
configuration, and running state. Keep each affected control **Not verified** unless the supplied
bundle identifies the environment, cluster/registry, collection time, source, deployment
revision, and complete workload/namespace scope. A policy object proves configuration, not live
enforcement; an admission denial proves activity, not complete namespace coverage; a registry
report applies only to its exact digest; and a pod `imageID` proves only that pod's running
digest. Stale, partial, redacted-beyond-use, or conflicting bundles remain **Not verified** with
the missing field and next collection step named.

Never weaken repository findings because external evidence is absent. Apply the documented
thresholds to repository-confirmed unsafe configuration: baked secrets or production root plus
`cluster-admin` are `Do not ship`. Report blockers, but issue no launch verdict; always route that
decision to `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-container-runtime-N` and require catalog approval before promotion.

### `PROVISIONAL-container-runtime-1` — Traceable digest-pinned images

**Applicability:** Any built or referenced container image. Protected property: workload
integrity — what was reviewed/scanned is provably what runs.

**Inspect and verify:** Every `FROM` line and `image:` field across Dockerfiles, Compose,
Kubernetes/Helm/Kustomize/Terraform, and CI. Require immutable pinning by `sha256:` digest for
deployed images (base images pinned by digest or tracked via automated update tooling);
reject mutable tags (`latest`, branch tags) as deploy references; prefer minimal base images
containing only runtime dependencies needed by the workload. Verify CI builds record
provenance/attestation or SBOM linkage to the pushed digest, and the same digest is
referenced per environment inventory.

**Unsafe evidence:** Mutable-tag production references; untracked floating bases with no
update mechanism; no way to map a running workload to its built digest.

**Required negative test:** Fixture manifest referencing `latest` must be flagged
`Fix before launch` with digest-pin remediation; rerendered fixture with digest must pass.

**Passing / Not verified:** Pass requires digest pinning plus a recorded digest-to-environment
mapping. Deployed-digest confirmation without cluster/registry evidence is **Not verified**.

**Related skill routing:** Attestation/SBOM lifecycle and triage: `secod-vulnerability-management`;
registry/release integrity: `secod-packages-delivery`.

### `PROVISIONAL-container-runtime-2` — Images are vulnerability-scanned before deploy

**Applicability:** Any image build/push pipeline. Protected property: known-vulnerable image
layers do not reach deployment unreviewed.

**Inspect and verify:** CI/workflow steps or platform config that scan built images
(scanner CLI, registry scanning, CI job) gating or reporting on push/deploy; scan coverage of
the production image, not only dev targets. This control verifies scanning exists and covers
the right images; finding triage is owned elsewhere.

**Unsafe evidence:** Builds pushed with no scan step; scans limited to stale images;
scan failures ignored by pipeline logic.

**Required negative test:** Fixture pipeline whose scan step fails must not proceed to deploy;
the skill flags missing gate as `Fix before launch`.

**Passing / Not verified:** Pass requires scan wiring covering the deployed image lineage.
Live registry scan results without supplied evidence are **Not verified**.

**Related skill routing:** Scanner governance, severity triage, SLAs, rescan-after-fix:
`secod-vulnerability-management`.

### `PROVISIONAL-container-runtime-3` — Build secrets never enter image layers

**Applicability:** Every Dockerfile/build definition. Protected property: credential
confidentiality across image history and registries.

**Inspect and verify:** Reject secrets passed via `ARG` or `ENV`, copied from build context, or
present in any `RUN` chain that persists them — build arguments and environment variables
persist in the final image. Require BuildKit secret mounts
(`RUN --mount=type=secret,id=...[,target=...|env=...]`) or SSH mounts
(`RUN --mount=type=ssh`) fed from external sources (CI secret store, `--secret`/`--ssh`
flags), not literals. Check `.dockerignore` excludes secret-bearing paths; check committed
history/fixtures for baked credentials.

**Unsafe evidence:** `ARG API_KEY=...`-style patterns feeding authenticated `RUN` steps;
secrets echoed into files under `/`; `.dockerignore` missing while context contains
credential files.

**Required negative test:** Fixture Dockerfile passing a token via `ARG` into `curl` must be
flagged; rewritten with `--mount=type=secret` must pass local static check.

**Passing / Not verified:** Pass requires no persistent-secret pattern plus mount-based
handling. Values themselves are never read or quoted; name-level analysis only.

**Related skill routing:** Secret rotation if exposure suspected: `secod-secrets-config`;
CI secret delivery: `secod-packages-delivery`.

### `PROVISIONAL-container-runtime-4` — Workloads run non-root

**Applicability:** Every container image and workload spec. Protected property: host and
cluster blast radius on container compromise.

**Inspect and verify:** Image declares a non-root `USER`; workload sets
`spec.securityContext.runAsNonRoot: true` (pod level or per container), numeric non-zero
`runAsUser` where the platform needs it, and `allowPrivilegeEscalation: false` on all
containers (including init/ephemeral). These are restricted fields of the Kubernetes Pod
Security Standards `restricted` profile. For Compose/Terraform, require equivalent
`user:`/non-root settings.

**Unsafe evidence:** Root `USER`, unset `runAsNonRoot` on cluster workloads,
`allowPrivilegeEscalation: true`, images requiring root without documented compensating
containment.

**Required negative test:** Fixture pod omitting `runAsNonRoot` and setting
`allowPrivilegeEscalation: true` must fail this control; corrected fixture passes.

**Passing / Not verified:** Pass requires both image-level user and workload-level
security-context evidence. Enforced-at-admission proof without cluster evidence stays
**Not verified**, classified at least `Likely` from manifests.

**Related skill routing:** Process-level least privilege inside the container:
`secod-runtime-execution`. Platform-managed sandboxing: provider adapter.

### `PROVISIONAL-container-runtime-5` — Dropped capabilities, read-only filesystem, seccomp

**Applicability:** Linux containers on orchestrators. Protected property: kernel and
filesystem attack surface.

**Inspect and verify:** `capabilities.drop: ["ALL"]` with explicit minimal `add` list only
where justified; `privileged: false` and no host namespaces/devices/PID sharing unless
documented necessity; `readOnlyRootFilesystem: true` with writable `emptyDir` volumes where
the app writes; seccompProfile `RuntimeDefault` (or stricter Localhost profile) set pod or
container level — never `Unconfined`. Restricted-profile allowed-value rules apply.

**Unsafe evidence:** Added dangerous capabilities (`SYS_ADMIN`, `NET_ADMIN`, `DAC_OVERRIDE`)
without justification; `privileged: true`; `hostPID`/`hostNetwork`/`hostIPC` on untrusted
workloads; missing seccomp profile on clusters predating default-on behavior.

**Required negative test:** Fixture adding `SYS_ADMIN` with `Unconfined` seccomp must fail;
corrected fixture drops ALL and sets `RuntimeDefault`.

**Passing / Not verified:** Pass requires manifest evidence for every field; node-side
default seccomp claims without evidence stay **Not verified**.

**Related skill routing:** Kernel/host isolation depth on managed platforms: provider adapter;
syscall-dependent app behavior: `secod-runtime-execution`.

### `PROVISIONAL-container-runtime-6` — Ports and network restricted by policy

**Applicability:** Every exposed port, Service, Ingress/Gateway, and pod network. Protected
property: lateral movement and unintended exposure prevention.

**Inspect and verify:** Containers expose only required ports; Services select only their own
workload; no NodePort/hostPort/load-balancer exposure without documented need. Where the
platform supports NetworkPolicy (Kubernetes), require named policies with explicit
default-deny ingress and egress plus targeted allows for each workload's real flows;
"policy support exists" alone is insufficient — policy objects must exist and match pods.

**Unsafe evidence:** Broad `0.0.0.0/0` egress on sensitive workloads with no policy;
pods selectable across tenants by shared labels; published management ports.

**Required negative test:** Fixture workload with no NetworkPolicy selecting it must be
reported unprotected; added default-deny-plus-allows fixture must pass structural review.

**Passing / Not verified:** Pass requires manifest-level policy objects; CNI-level enforcement
confirmation without cluster evidence is **Not verified**.

**Related skill routing:** API/webhook boundary validation behind those ports:
`secod-inputs-apis`; SSRF/egress allowlists inside the app: `secod-inputs-apis`.

### `PROVISIONAL-container-runtime-7` — CPU and memory bounded per workload

**Applicability:** Every long-running workload and Job. Protected property: availability and
noisy-neighbor/no-exhaustion containment.

**Inspect and verify:** Explicit CPU/memory `requests` and `limits` per container (not
namespace-wide defaults alone); limits aligned to probe timeouts and expected load; Jobs and
CronJobs bounded too; no `limits: {}` unlimited workloads in multi-tenant namespaces.

**Unsafe evidence:** Missing limits on internet-facing workloads; requests far below limits
without capacity rationale; unbounded sidecar consuming the pod budget.

**Required negative test:** Fixture deployment without resource blocks must fail; fixture
with requests+limits passes.

**Passing / Not verified:** Pass requires manifest evidence. Cluster quota/limit-range
enforcement without evidence is **Not verified**.

**Related skill routing:** Request/user-level quotas and cost ceilings: `secod-abuse-limits`;
autoscaler/platform limits: provider adapter.

### `PROVISIONAL-container-runtime-8` — Runtime secrets injected, never baked

**Applicability:** Every workload consuming credentials. Protected property: secret values
absent from images, plain-text env blocks, and command lines.

**Inspect and verify:** Kubernetes workloads consume `secretKeyRef`/mounted Secrets (or a
named external secret operator), not literal env values; Compose uses `_FILE` patterns or
external secrets, not inline plaintext; Helm values carry references/placeholders, never
committed real values; no secrets in container command args or health-check URLs. Value
classification/rotation stays with the owner below.

**Unsafe evidence:** Literal credentials in ConfigMaps/env blocks/values files; secrets baked
into images (overlaps control 3); secret material in log/probe paths.

**Required negative test:** Fixture with plaintext password in an env block must fail;
converted `secretKeyRef` fixture passes.

**Passing / Not verified:** Pass requires injection-mechanism evidence in manifests. Deployed
Secret contents/encryption state without evidence is **Not verified**.

**Related skill routing:** Secret values, storage, rotation, revocation: `secod-secrets-config`.

### `PROVISIONAL-container-runtime-9` — Least-privilege ServiceAccounts, RBAC, Pod Security

**Applicability:** Kubernetes workloads and their service identities. Protected property:
compromised pod cannot abuse cluster API beyond its function.

**Inspect and verify:** Each workload uses a dedicated named ServiceAccount (not `default`);
`automountServiceAccountToken: false` wherever the API is unused; RBAC Roles grant minimal
verbs/resources actually used, bound via RoleBindings in the workload namespace; no
cluster-admin for application workloads; namespace carries Pod Security labels enforcing the
`restricted` (or documented `baseline`) standard in `enforce` mode.

**Unsafe evidence:** `default` SA with token automounted and wide RBAC;
`cluster-admin` binding on app SAs; audit/warn-only Pod Security where enforce is feasible.

**Required negative test:** Fixture using `default` SA + cluster-admin binding + no PSS label
must fail all three subchecks; corrected fixture names a scoped SA, disables automount, adds
enforce labels.

**Passing / Not verified:** Pass requires manifest/RBAC-object evidence. Live binding
verification without cluster export is **Not verified**.

**Related skill routing:** Human/admin identity and authz semantics: `secod-identity-access`;
managed-cluster IAM: provider adapter.

### `PROVISIONAL-container-runtime-10` — Signed-image admission where available

**Applicability:** Clusters/registries offering signature or policy verification (admission
controllers, policy frameworks, registry signature features). Protected property: only
verified, policy-conformant images schedule.

**Inspect and verify:** Detect policy-controller/admission-webhook configuration in-repo
(IaC, chart dependencies, cluster add-on declarations); verify a policy binds protected
namespaces to trusted signers/digests and fails closed on unverifiable images. If the platform
offers no such capability, document that determination instead of failing.

**Unsafe evidence:** Policy installed in audit-only mode on production namespaces with no
migration plan; policy absent where platform supports it and supply-chain risk is high;
policy allowing unsigned images by default.

**Required negative test:** Fixture admission policy permitting unsigned images must be
flagged; deny-by-default signer-bound policy passes structural review.

**Passing / Not verified:** Pass requires policy configuration plus evidence it is active.
Availability/enforcement without cluster evidence is **Not verified**.

**Related skill routing:** Signature key management: `secod-crypto-data-protection`;
attestation consumption lifecycle: `secod-vulnerability-management`.

## Exceptional and failure conditions

Fail closed on every path below; a failed checker, timed-out scan/render, or incomplete test
never counts as success:

- Tool timeout or dependency failure (scanner unreachable, registry auth failure, `helm
  template` error, kubectl/context unavailable): affected controls become **Not verified**
  with the exact failed step recorded; never substitute cached results.
- Partial operations: partially rendered charts or partial manifest sets are reviewed only for
  the rendered subset; unrendered/unreachable workloads are **Not verified** pending full
  render. Record the gap owner and next step.
- Rollout failure/reconciliation drift between repo manifests and cluster state: treat as
  **Conflicting** evidence; affected controls **Not verified** until reconciled.
- Retry/cancellation applies to the reviewer's own read-only commands only; never retry
  mutating operations against clusters or registries.
- Credential revocation/rotation events during review invalidate captured registry/cluster
  evidence; re-evidence required.
- No provider retry schedules or guarantees are invented; scanner/registry behavior claims
  cite current official documentation only.

## Dependency and routing rules

Direct dependency, exactly as in `secod/catalog.json`: `secod-core`.

If `secod-core` is not installed or cannot be invoked, every control below becomes
**Not verified**: detection/routing evidence cannot be established independently. Name the
missing owner/evidence in findings. Never invent replacement dependencies and never issue
launch readiness from this skill.

Conditional routes resolve slugs from the live catalog at run time; unresolved, malformed, or
missing routed owners make the affected controls **Not verified** with the missing owner named.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Thresholds:

- `Do not ship`: baked build/runtime secrets (controls 3/8) or root-privileged workloads with
  cluster-admin RBAC (controls 4/9) on production-targeted artifacts.
- `Fix before launch`: digest pinning absent on deployed references, missing scan gate,
  unrestricted privileged container settings, missing resource bounds or network policy on
  internet-facing workloads, unsigned-image admission absent where platform supports it.
- `Recommended hardening`: defense-in-depth gaps (read-only rootfs off, non-minimal capability
  adds, warn-mode Pod Security, baseline instead of restricted where restricted is feasible).
- `Passed with evidence`: manifest-level evidence plus corroborating build/deploy correlation
  for every applicable control.
- `Not verified`: required evidence missing, stale, conflicting, inaccessible, unsupported, or
  from a failed/incomplete test. Package presence alone never passes.

Never claim a control passed from package presence, documentation snapshots, inferred
configuration, or failed tests.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with:

- Applicability inventory (per-environment workloads/images with Candidate/Likely/Active)
- Test results (executed checks with outcomes; skipped checks with reasons)
- Requested external evidence (exact cluster/registry/Dashboard items needed from humans)
- `Not verified` items with next verification step each
- Launch blockers list

Route overall launch readiness to `secod-ship-check`; include routed_skills per finding.

Redact all secret values, tokens, and connection strings from evidence, commands, and reports;
record names, paths, and structure only.

## Negative fixtures and tests

Map maintained fixtures at `tests/` for this skill:

| Fixture case | Controls exercised | Executable? |
| --- | --- | --- |
| Clean workload (digest pins, non-root, caps dropped, seccomp, limits, policies, SA scoping) | 1, 4–9 | Documentation-only plan |
| Insecure fixture (latest tags, ARG secret, root, SYS_ADMIN, no policy/limits, default SA + cluster-admin, plaintext env secret) | 1, 3–9 | Documentation-only plan |
| Missing-evidence case (no cluster/registry access) | 1, 2, 10 | Documentation-only plan |
| Failure case (scan/render tool failure mid-review) | 2, all | Documentation-only plan |

Safe local checks when reviewing an arbitrary repository: static grep of Dockerfiles for
`ARG`/`ENV` secret patterns; `docker build --check`-class linting where available;
`helm template`/`kubectl kustomize`/`terraform validate` against committed files only.
Markdown fixture plans above are plans, not executed code — never report them executed.

Never run destructive, production-changing, cluster-mutating, image-deleting, key-rotating, or
dashboard-changing tests without explicit authorization.

## References

- Source register and review metadata: `references/sources.md`
- Cluster, registry, digest, and signature evidence collection:
  `references/external-evidence.md`
