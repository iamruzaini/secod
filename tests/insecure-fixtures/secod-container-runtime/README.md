# Insecure fixture plan: secod-container-runtime

Create a minimal reproducible unsafe case containing a mutable production image tag, build secret
passed through `ARG`, root user, `SYS_ADMIN`, writable root filesystem, no seccomp profile, no
resource limits, no NetworkPolicy, plaintext runtime secret, default ServiceAccount, and a
`cluster-admin` binding. Expected blockers: baked secret and production root plus `cluster-admin`
are `Do not ship`; other applicable gaps use skill thresholds.

Add a clean manifest fixture with digest pins, non-root execution, dropped capabilities,
`RuntimeDefault`, read-only root filesystem, resource bounds, default-deny plus targeted network
allows, dedicated ServiceAccount, scoped RBAC, and enforced restricted Pod Security labels.

Add external-evidence cases:

- no cluster or registry bundle: live enforcement, scans, running digests, and signature activity
  remain `Not verified`;
- partial bundle containing policy objects but no activity/enforcement evidence: configuration is
  recorded, but affected live controls remain `Not verified`;
- conflicting rollout bundle with mixed running digests: control 1 remains `Not verified`;
- complete digest-correlated bundle: only directly covered controls may pass.

No fixture grants real cluster access or contains real credentials. Server-side admission and
connectivity tests remain documentation-only unless explicitly authorized.
